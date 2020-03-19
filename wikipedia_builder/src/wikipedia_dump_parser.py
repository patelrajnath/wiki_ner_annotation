# coding: utf-8
import pymongo 
import datetime
from pprint import pprint
from .utils import yield_wikipedia_dump_articles, parse_article_interlinks

class WikipediaParser(object):
    
    def __init__(self, wiki_dump_pages, mongo_host, mongo_port, db_name):
        self._dump_pages = wiki_dump_pages
        self._mongo_host = mongo_host
        self._port = mongo_port
        self._db_name = db_name
        self._client = None
        self._DB = None
        self._open_conn()
        self._mappings = {'wiki_page':'wikipedia_article',
                          'tag':'tag',
                          'entity':'entity',
                          'entity_references':'entity_references'}

    def add_dump_wikipedia_articles(self, bulk_size = 10000, verbose = False):
        bulk = []

        if verbose:
            print('Adding to %s.%s'%(self._db_name, self._mappings['wiki_page']))

        for i, article in enumerate(yield_wikipedia_dump_articles(self._dump_pages)):
            bulk.append(article)
            if (i+1)%bulk_size == 0 and bulk:
                self._add_wrapper(self._mappings['wiki_page'], bulk, verbose)
                bulk = []

        if bulk:
            self._add_wrapper(self._mappings['wiki_page'], bulk, verbose)
            bulk = []

        # Creating index
        self._indexer_wrapper(self._mappings['wiki_page'], 'wiki_id', verbose = verbose)
        self._indexer_wrapper(self._mappings['wiki_page'], 'title', verbose = verbose)

    def add_entities(self, entities_iterator, bulk_size = 10000, verbose = False, no_article_ignore = False):
        article_collection = self._DB[self._mappings['wiki_page']]
        tag_collection = self._DB[self._mappings['tag']]

        bulk_entities = []

        # TODO: verbose
        for i, entity in enumerate(entities_iterator):   
            # associates entity with its article
            entity_article = article_collection.find_one({'wiki_id': entity['article']})
            if entity_article:
                entity['article'] = entity_article['_id']

            elif no_article_ignore:
                continue

            # associates the entity with its tag if it does not exist, create
            tag = tag_collection.find_one({'name': entity['tag']})

            if not tag:
                tag = {'name':entity['tag']}
                tag_id = tag_collection.insert_one(tag).inserted_id
                tag['_id'] = tag_id
            
            entity['tag'] = tag['_id']

            bulk_entities.append(entity)

            if bulk_entities and (i+1)%bulk_size == 0:
                self._add_wrapper(self._mappings['entity'], bulk_entities, verbose = verbose)
                bulk_entities = []

        if bulk_entities:
            self._add_wrapper(self._mappings['entity'], bulk_entities, verbose = verbose)
            bulk_entities = []
        
        self._indexer_wrapper(self._mappings['entity'], 'iri', verbose = verbose)
        self._indexer_wrapper(self._mappings['entity'], 'article', verbose = verbose)

    def add_references(self, bulk_size = 10000, verbose = False):
        article_collection = self._DB[self._mappings['wiki_page']]
        entity_collection = self._DB[self._mappings['entity']]
        
        # Create lookup table for entity iris to id
        print('Creating lookup table for entities iris to id...')
        iri2id = {}
        for entity in entity_collection.find():
            iri2id[entity['iri']] = entity['_id']

        print('Creating lookup table for articles ...')
        title2count = {}
        for article in article_collection.find():
            title2count[article['title']]  = [article['_id'], 0]

        bulk_references = []
        for i, article in enumerate(article_collection.find()):
            
            wikilinks = parse_article_interlinks(article['wiki_text'])

            for wikilink in wikilinks:
                wikilink_text = wikilink[0]
                wikilink_iri = wikilink[1]
                
                # Is entity
                if wikilink_iri in iri2id:
                    reference = {'article': article['_id'],
                                'entity': iri2id[wikilink_iri],
                                'text': wikilink_text}

                    bulk_references.append(reference)

                # Is an article
                if wikilink_iri in title2count:
                    title2count[wikilink_iri][1] += 1

            if bulk_references and (i+1)%bulk_size == 0:
                self._add_wrapper(self._mappings['entity_references'], bulk_references, verbose=verbose)
                bulk_references = []

        if bulk_references:
            self._add_wrapper(self._mappings['entity_references'], bulk_references, verbose=verbose)
            bulk_references = []
        
        self._indexer_wrapper(self._mappings['entity_references'], 'article', verbose = verbose, unique = False)
        self._indexer_wrapper(self._mappings['entity_references'], 'entity', verbose = verbose, unique = False)

        if verbose:
            print('Updating the articles references count')
        # TODO: use aux method for writing
        if title2count:
            bulk_update_count = []
            for i, title in enumerate(title2count):
                bulk_update_count.append(pymongo.UpdateOne({'_id':title2count[title][0]}, {'$set':{'reference_count':title2count[title][1]}}))
                if bulk_update_count and (i+1)%bulk_size == 0:
                    article_collection.bulk_write(bulk_update_count)
                    bulk_update_count = []

            if bulk_update_count:
                article_collection.bulk_write(bulk_update_count)
                bulk_update_count = []

    def clean_wikitext(self, cleaner_function, bulk_size = 10000, verbose = False):
        article_collection = self._DB[self._mappings['wiki_page']]
        bulk_write = []
        for i, article in enumerate(article_collection.find()):
            bulk_write.append(pymongo.UpdateOne({'_id':article['_id']},
                                                {'$set':{'clean_wiki_text':cleaner_function(article['wiki_text'])}}))
            
            if bulk_write and (i+1)%bulk_size == 0:
                self._bulk_write_wrapper(bulk_write, self._mappings['wiki_page'], verbose = True)
                bulk_write = []

        if bulk_write:
            self._bulk_write_wrapper(bulk_write, self._mappings['wiki_page'], verbose = True)
            bulk_write = []

    def add_articles_sentences(self, build_function, bulk_size = 10000, verbose = False):
        article_collection = self._DB[self._mappings['wiki_page']]
        references_collection = self._DB[self._mappings['entity_references']]
        entities_collection = self._DB[self._mappings['entity']]
        tags_collection = self._DB[self._mappings['tag']]

        tags_lookup = {tag['_id']:tag for tag in tags_collection.find()}

        bulk_write = []       

        for i, article in enumerate(article_collection.find()):
            #print('===== %s ====='%(article['title']))
            references = references_collection.find({'article':article['_id']})
            entities = list(entities_collection.find({'_id':{'$in':[ref['entity'] for ref in references]}}))
            entities += entities_collection.find({'article':article['_id']})

            for entity in entities:
                entity['tag'] = tags_lookup[entity['tag']]['name']

            sentences = list(build_function(entities, article, references, reference_text_validator = None))
            bulk_write.append(pymongo.UpdateOne({'_id':article['_id']},
                                                {'$set':{'sentences':sentences}}))

            if bulk_write and (i+1)%bulk_size == 0:
                self._bulk_write_wrapper(bulk_write, self._mappings['wiki_page'], verbose = True)
                #article_collection.bulk_write(bulk_write)
                bulk_write = []

        if bulk_write:
            self._bulk_write_wrapper(bulk_write, self._mappings['wiki_page'], verbose = True)
            bulk_write = []

    def copy_DB(self, copy_name):
        self._client.admin.command('copydb',
                                    fromdb= self._db_name,
                                    todb= copy_name)

    def _add_wrapper(self, collection, documents, verbose = False):
        if verbose:
            print('Adding %s documets in %s.%s'%(len(documents), self._db_name, collection))
        self._DB[collection].insert_many(documents)

    def _indexer_wrapper(self, collection, attribute, verbose, unique = True):
        if verbose:
            print('Indexing %s.%s.%s'%(self._db_name, collection, attribute))
        self._DB[collection].create_index([(attribute, pymongo.ASCENDING)], unique = unique)

    def _bulk_write_wrapper(self, operations, collection, verbose = False):
        if verbose:
            print('Performing %s write operations on %s.%s'%(len(operations), self._db_name, collection))
        result = self._DB[collection].bulk_write(operations)
        pprint(result.bulk_api_result)

    def _open_conn(self):
        self._client = pymongo.MongoClient(self._mongo_host, self._port)
        self._DB = self._client[self._db_name]