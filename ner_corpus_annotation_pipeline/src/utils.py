from .text_token import TextToken
from polyglot.text import Text
import string
import nltk
import re

def get_word_tokens(text, tags_dict = {}):
    ordered_slices = nltk.word_tokenize(text, language = "portuguese")
    #ordered_slices = [s if s not in ["``","''"] else '"' for s in ordered_slices]
    tokens = []
    offset = 0
    for part in ordered_slices:
        #print(part)

        # specific for nltk word tokenizer
        if part in ["``","''"]:

            found_value = None
            found_value_offset = len(text)

            for value in ["``","''",'"']:
                value_offset = text.find(value, offset)

                if value_offset == -1:
                    continue
                
                if value_offset < found_value_offset:
                    found_value = value
                    found_value_offset = value_offset
            
            part = found_value
            
        offset = text.find(part, offset)
        tokens.append(TextToken(text = text,
                            start_index = offset,
                            end_index = offset + len(part) - 1,
                            tags_dict = tags_dict.copy()))

        offset += len(part)

    return sort_tokens(tokens)

def get_sentence_tokens(text, tags_dict = {}):
    return create_tokens_from_slices(text = text,
                                     tags_dict = tags_dict,
                                     ordered_slices = nltk.sent_tokenize(text, language = "portuguese"))

def sort_tokens(tokens):
    tokens.sort(key = lambda x: x.start_index)
    return tokens

def create_tokens_from_slices(text, ordered_slices, tags_dict, offset = 0):
    tokens = []

    # print('=== CREATING TOKENS FROM SLICES ===')
    # print('slices: %s'%(ordered_slices))
    for part in ordered_slices:
        offset = text.find(part, offset)
        tokens.append(TextToken(text = text,
                                start_index = offset,
                                end_index = offset + len(part) - 1,
                                tags_dict = tags_dict.copy()))
        offset += len(part)

    # print('=== // ===')
    return sort_tokens(tokens)

def trim_entity_tokens(tokens, text):
    strip_chars = list(string.punctuation) + [' ']
    trimmed = []
    for token in tokens:
    
        strip_left_char = 0
        strip_right_char = 0

        section = token.section
        #section = re.sub('[(/].+[)/]','',section)
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
        #print('3',section)
                
        if not section:
            continue

        if not section[0].isupper():
            continue

        t = TextToken(text = text,
                      start_index = token.start_index + strip_left_char,
                      end_index = token.end_index + strip_right_char,
                      tags_dict = token.tags_dictionary.copy())
        trimmed.append(t)
    
    return trimmed

def predict_entities_tokens(text, tags_dict = {}):
    if not text:
        return []

    def get_polyglot_entity_index_boundaries(polyglot_text, entity):
        start_index = -1
        end_index = -1
        offset = 0

        for i, word in enumerate(polyglot_text.words):
            offset = text.find(word, offset)
            if i == entity.start:
                start_index = offset

            offset += len(word)
            if i + 1 == entity.end:
                end_index = offset - 1
                break

        #print(start_index, end_index)
        return start_index, end_index
    
    entity_tokens = []
    polyglot_text = Text(text)
    polyglot_text.language = 'pt'
    for entity in polyglot_text.entities:
        #print(entity)
        e_tags_dict = tags_dict.copy()
        
        entity_tag = entity.tag.split('-')[1]

        e_tags_dict['tag'] = entity_tag

        start, end = get_polyglot_entity_index_boundaries(polyglot_text, entity)

        entity_tokens.append(TextToken(text = text,
                                       start_index = start,
                                       end_index = end,
                                       tags_dict = e_tags_dict))

    return entity_tokens