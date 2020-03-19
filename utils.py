from wikipedia_cleaner import PTwikitextCleaner
from ner_corpus_annotation_pipeline import NerCorpusAnnotationPipeline, Entity
import logging
import string
import glob
import csv
import re
import os

def _yield_entities_from_folder(csv_folder):
    separator = ";;"
    
    id_col = "wikiPageID"
    url_col = "isPrimaryTopicOf"
    files =  glob.glob(os.path.join(csv_folder, '*.csv'))

    for file in files:
        for row in csv.DictReader(open(file, 'r')):
            
            article_id = int(row.pop(id_col))
            article_url = row.pop(url_col)
            names = {k:v.split(separator) for k, v in row.items()}
            iri = re.search("http://pt.wikipedia.org/wiki/(.+\Z)", article_url).group(1)

            yield {'iri': iri.replace('_',' '),
                   'article_url': article_url,
                   'article': article_id,
                   'tag': None,
                   'dbpedia_names': names,
                   'referenced_names_count': {},
                   'referenced_count': 0}

def clean_wikitext(wikitext):
    return PTwikitextCleaner(wikitext).clean()

def filter_names(names_dict):
    pass

def sentences_builder(entities, article, references, reference_text_validator = None):
    logging.basicConfig(filename='errors_sentence_builder.log',level=logging.ERROR)
    pipeline_entities = []

    # build entities
    for entity in entities:
        entity_references = [reference for reference in references if reference['entity'] == entity['_id']]

        names = [item for sublist in entity['dbpedia_names'].values() for item in sublist if item != '']
        for reference in entity_references:
            names.append(reference['text'])
        #print(names)
        names = fix_and_filter_names(names)

        #print(names)
        pipeline_entities.append(Entity(names = names, tag = entity['tag']))

    # process paragraph by paragraph in order to associate errors
    for paragraph in article['clean_wiki_text'].split('\n'):
        
        if not paragraph.strip(' '):
            continue

        try:
            annotator = NerCorpusAnnotationPipeline(paragraph, pipeline_entities)
            annotator.apply_processing_rules()

            for words, tags, types in annotator.get_sentences():
                
                infos = { "annotated": {'count':0, 'type_count':{}, 'lengths_by_type':{}},
                          "predicted": {'count':0, 'type_count':{}, 'lengths_by_type':{}}}

                curr_ent_source = '' # annotated or predicted
                curr_ent_token_count = 0
                curr_ent_tag = ''
                sentence = []
                has_annotated = False
                for i in range(len(tags)):
                    
                    token_tag = tags[i][0]
                    
                    if tags[i][0] in ['B', 'I']:
                        token_tag = token_tag + '-' + tags[i][1]

                    sentence.append([words[i], token_tag, types[i]])
                    if types[i] == 'annotated':
                        has_annotated = True

                    if tags[i][0] != 'I':
                        # end current entity if existent
                        if curr_ent_token_count > 0:
                            
                            # add total count
                            infos[curr_ent_source]['count'] += 1

                            # add entity type count
                            if curr_ent_tag not in infos[curr_ent_source]['type_count']:
                                infos[curr_ent_source]['type_count'][curr_ent_tag] = 0
                            infos[curr_ent_source]['type_count'][curr_ent_tag] += 1

                            # add entity length to lengths list
                            if curr_ent_tag not in infos[curr_ent_source]['lengths_by_type']:
                                infos[curr_ent_source]['lengths_by_type'][curr_ent_tag] = []
                            infos[curr_ent_source]['lengths_by_type'][curr_ent_tag].append(curr_ent_token_count)

                            curr_ent_source = '' # annotated or predicted
                            curr_ent_token_count = 0
                            curr_ent_tag = ''
                            
                        if tags[i][0] == 'B': # start new entity
                            curr_ent_tag = tags[i][1]
                            curr_ent_token_count = 1
                            curr_ent_source = types[i]

                    else:
                        if curr_ent_source:
                            curr_ent_token_count += 1

                sentence = {'tokens': sentence,
                            'infos': infos}

                if has_annotated:
                    yield sentence
        
        except Exception as e:
            message = 'paragraph: start>%s<end\ntitle:%s\nid:%s'%(paragraph, article['title'], article['_id'])
            logging.exception(message)
            raise e

def fix_and_filter_names(names):
    fixed_names = []
    strip_chars = list(string.punctuation) + [' ']

    for name in names:
        strip_left_char = 0
        strip_right_char = 0

        section = name
        section = re.sub('[(/].+[)/]','',section)
        #print('1',section)
        for char in section:
            if char not in strip_chars:
                break
            strip_left_char += 1

        section = section[strip_left_char:]
        if not section:
            continue
        #print('2',section)

        for char in reversed(section):
            if char not in strip_chars:
                break
            strip_right_char -= 1

        section = section[:len(section) + strip_right_char]
                
        if not section:
            continue

        if not section[0].isupper():
            continue
        

        fixed_names.append(section)

    return fixed_names

def entity_iterator():
    folders_tag = [('./resources/DBpedia_entities/Person', 'PER'),
                   ('./resources/DBpedia_entities/Organisation', 'ORG'),
                   ('./resources/DBpedia_entities/Place', 'LOC')]
    
    for folder, tag in folders_tag:
        for entity in _yield_entities_from_folder(folder):
            entity['tag'] = tag
            yield entity

#print(fix_and_filter_names(['*(())','--==não','---Sim}}----']))