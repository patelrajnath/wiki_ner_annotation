from .text_token import check_intersect, TextToken
from string import punctuation
import ahocorasick

def tokenize_entities(entities, text, tags_dict = None):
    if tags_dict == None: tags_dict = {}

    A = ahocorasick.Automaton()
    names_inserted = False
    # Add the terms of the entity to the disctionary
    for entity in entities:
        for name in entity.names:
            A.add_word(name, (len(name),entity.tag))
            names_inserted = True
    
    if not names_inserted:
        return []
    A.make_automaton() # Builds the automaton
    tokens = []

    for end_index, (length, tag) in A.iter(text):
        start_index = end_index - length + 1
        
        if _token_has_word_boundaries(text,start_index, end_index):
            current_token = TextToken(text, start_index, end_index, tags_dict)
            current_token.set_tag_value('tag', tag)

            if not tokens: # First token, no need to compare with previous
                tokens.append(current_token)
                continue

            previous_token = tokens[len(tokens)-1]

            # If there is a conflict, prioritize the largest token
            if check_intersect(current_token, previous_token):
                #print(current_token.section,'-->', previous_token.section)
                #print(current_token.start_index,'-->', previous_token.start_index)
                #print('conflict')
                # The current token is the largest
                if len(current_token.section) >= len(previous_token.section):
                    #print('choose',current_token.section)
                    del tokens[-1]
                    tokens.append(current_token)

            else: # No conflict found
                tokens.append(current_token)

    return tokens

def _token_has_word_boundaries(text, start_index, end_index):
    """ 
        Defines if the token presents itself as a word
        i.e. not in the middle of a sequence of characters, must be enclosed in 
        spaces or punctuation 
    """

    is_valid_to_the_left = False
    is_valid_to_the_right = False
    
    # start of the string
    if start_index == 0: # start of the string
        is_valid_to_the_left = True
    elif text[start_index - 1] == ' ': # is a space
        is_valid_to_the_left = True
    elif text[start_index - 1] in punctuation:
        is_valid_to_the_left = True

    if end_index == len(text) - 1: # end of string
        is_valid_to_the_right = True
    elif text[end_index + 1] == ' ': # is a space
        is_valid_to_the_right = True
    elif text[end_index + 1] in punctuation:
        is_valid_to_the_right = True

    return is_valid_to_the_left and is_valid_to_the_right