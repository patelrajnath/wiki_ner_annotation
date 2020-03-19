import xml.etree.ElementTree as etree
import mwparserfromhell
import glob
import csv
import re
import os

###https://archive.org/search.php?query=2016%20portuguese&and[]=subject%3A%22dumps%22
###https://archive.org/download/ptwiki-20161001

def yield_wikipedia_dump_articles(dump_path):
    """
    Yields the articles in the wikipedia dump (namespace 0), ignores the rest
    """

    def strip_tag_name(t):
        idx = k = t.rfind("}")
        if idx != -1:
            t = t[idx + 1:]
        return t

    wiki_id = None
    title = ''
    in_revision = False
    name_space = -1

    for event, elem in etree.iterparse(dump_path, events=('start', 'end')):
        tag_name = strip_tag_name(elem.tag)
        
        if event == 'start': # start of the tag
            if tag_name == 'page':
                wiki_id = None
                title = ''
                in_revision = False
                name_space = -1

            elif tag_name == 'revision':
                in_revision = True
    
        else:
            if tag_name == 'title':
                title = elem.text

            elif tag_name == 'id' and not in_revision:
                wiki_id = int(elem.text)

            elif tag_name == 'ns':
                name_space = int(elem.text)

            elif tag_name == 'text':
                if name_space == 0: # the page is an article
                    yield {'wiki_id':wiki_id,
                           'title':title,
                           'wiki_text': elem.text,
                           'references_count': 0}

            elem.clear()

def parse_article_interlinks(wiki_text):
    raw_interlinks_str = [str(link) for link in mwparserfromhell.parse(wiki_text).filter_wikilinks()]
    inter_links = []

    for interlink in raw_interlinks_str:
        links_contents = re.findall(r"\[\[([^\[\]]+)\]\]", interlink)

        for content in links_contents:
            mention = None
            iri = None

            # Image or category...
            if ':' in content:
                continue

            parts = content.split('|')
            
            mention = parts[0]
            iri = mention if len(parts) == 1 else parts[1]
            inter_links.append((iri, mention))
            #interlinksObj.append(WikipediaInterLink(mention, iri, wikipedia_page.page_id))

    return inter_links

def get_article_sentences(article_wikitext, entities):
    # find and annotate the entities
    pass