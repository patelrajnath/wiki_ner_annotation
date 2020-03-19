import nltk
from .entity import Entity
from .text_token import TextToken, check_intersect
from .utils import get_word_tokens, get_sentence_tokens, sort_tokens, create_tokens_from_slices, predict_entities_tokens, trim_entity_tokens
from .entity_okenization import tokenize_entities
import re

class NerCorpusAnnotationPipeline(object):
    
    def __init__(self, text, entities):
        self._text = re.sub( '\s+', ' ', text).strip()
        self.entities = entities

        self.annotated_entities_tokens = tokenize_entities(self.entities, self._text, tags_dict = {'type':'annotated'})
    
        self.predicted_entities_tokens = trim_entity_tokens(predict_entities_tokens(self._text, tags_dict = {'type':'predicted'}), self._text)
        self.sentences_tokens = get_sentence_tokens(self._text, tags_dict = {'type':'sentence'})
        
        self.word_tokens = get_word_tokens(self._text, tags_dict = {'type':'word','IOB':'O'})      

    def _print(self):
        print('annotated:', [a.section for a in self.annotated_entities_tokens])
        print('predicted:', [[a.section, a.start_index, a.end_index] for a in self.predicted_entities_tokens])
        print('n sentences:', [[a.section, a.start_index, a.end_index] for a in self.sentences_tokens])

    def apply_processing_rules(self):
        
        # remove the predicted entities that are in the same section as the annotated ones
        self.predicted_entities_tokens = self._filter_entities_tokens(self.predicted_entities_tokens, self.annotated_entities_tokens)
        
        # conflicting predicted tokens?
        self.predicted_entities_tokens = self._filter_entities_tokens(self.predicted_entities_tokens, self.predicted_entities_tokens)

        # ensure the sentences enclose the annotated tokens
        self.sentences_tokens = self._ensure_enclosing(self.annotated_entities_tokens, self.sentences_tokens)        
        # split on space character
        self.annotated_entities_tokens = self._split_tokens_applying_iob(self.annotated_entities_tokens)
        # fit on the words
        self.word_tokens = self._fit_tokens(self.annotated_entities_tokens, self.word_tokens)
        
        self.sentences_tokens = self._ensure_enclosing(self.predicted_entities_tokens, self.sentences_tokens)
        # split on space character
        self.predicted_entities_tokens = self._split_tokens_applying_iob(self.predicted_entities_tokens)
        # fit on the words
        self.word_tokens = self._fit_tokens(self.predicted_entities_tokens, self.word_tokens)


    def _filter_entities_tokens(self, predicted_entitiy_tokens, annotated_entity_tokens):
        for a_token in annotated_entity_tokens:
            p_span = self._get_tokens_span(predicted_entitiy_tokens, a_token)
            for p_token in p_span:
                if check_intersect(p_token, a_token):
                    predicted_entitiy_tokens.remove(p_token)

        # for p_token in predicted_entitiy_tokens:
        #     for a_token in annotated_entity_tokens:
        #         if a_token.encloses(p_token.start_index) or a_token.encloses(p_token.end_index):
        #             invalid_predicted.append(p_token)
        #             break
            
        # for i_token in invalid_predicted:
        #     predicted_entitiy_tokens.remove(i_token)
        
        return predicted_entitiy_tokens
            
    def _ensure_enclosing(self, tokens, chain_tokens):
        
        #print('------------')
        for token in tokens:
            t_start = [t for t in chain_tokens if t.encloses(token.start_index)]
            t_end = [t for t in chain_tokens if t.encloses(token.end_index)]


            # print('=== SEARCHING ==')
            # print(token.start_index, token.end_index)
            # print(token.section)
            # print(token.tags_dictionary['type'])
            # print('=== CHAIN ==')
            # for t in chain_tokens:
            #     print(t.start_index, t.end_index)

            #assert(len(t_start) == 1)
            #assert(len(t_end) == 1)

            t_start = t_start[0]
            t_end = t_end[0]

            # Ends in the same sentence it started?
            if t_start is t_end:
                enclosed = chain_tokens
                continue

            # Merge sentences
            merged_token = TextToken(text = self._text,
                                    start_index = t_start.start_index,
                                    end_index = t_end.end_index,
                                    tags_dict = {'type':'sentence'})

            inside_flag = False
            sentences = []
            for t in chain_tokens:
                # Jump sentences in between start - end
                if t is t_start:
                    inside_flag = True
                elif t is t_end:
                    inside_flag = False
                elif not inside_flag:
                    sentences.append(t)

            sentences.append(merged_token)

            chain_tokens = sort_tokens(sentences)

        return chain_tokens

    def _split_token(self, token, splitting_function):
        #print(splitting_function(token.section))
        parts = list(filter(lambda x: x!= '' ,splitting_function(token.section)))

        #print('>'+token.section+'<' ,' - Split ->', '>',parts,'<')
        #print('In text:' + self._text[token.start_index:token.end_index+1])
        #print(token.tags_dictionary['type'])
        return create_tokens_from_slices( text = self._text,
                                          tags_dict = token.tags_dictionary,
                                          ordered_slices = parts,
                                          offset = token.start_index)

    def _split_tokens_applying_iob(self, tokens):
        splitted_tokens = []
        
        
        #print('=== SPLITTING TOKENS ===')
        for k_token in tokens:
            splitted_token = self._split_token(k_token, lambda x: x.split(' '))
            #print(splitted_token)
            # IOB tagging
            splitted_token[0].set_tag_value('IOB', 'B')
            for token in splitted_token[1:]:
                token.set_tag_value('IOB', 'I')

            splitted_tokens += splitted_token

        return splitted_tokens

    def _get_tokens_span(self, token_chain, token):
        
        inside_flag = False
        token_span = []
        for t in token_chain:
            if t.encloses(token.start_index):
                inside_flag = True
                token_span.append(t)

                # The end and init of the token are inside the same token
                if t.encloses(token.end_index):
                    break
    
            elif t.encloses(token.end_index):
                inside_flag = False
                token_span.append(t)

            elif inside_flag:
                token_span.append(t)

        return token_span

    def _fit_tokens(self, tokens_to_fit ,token_chain):
        """
            Reserves the space of the known tokens by trimming out their regions in the words.
            E.i. if a word occupies the space of a known token 
        """
        
        for k_token in tokens_to_fit:
            token_span = self._get_tokens_span(token_chain, k_token)
            
            for token in token_span:
                token_chain.remove(token)

            for token in [self._trim_token(token, k_token.start_index, k_token.end_index) for token in token_span]:
                if token:
                    token_chain += token

        return sort_tokens(token_chain)

    def _trim_token(self, token, init, end, original_text = ""):
        """
            Trim out the region defined by init and end.
            Returns the subtokens if any is produced, an empty list if none is.
        """

        tokens = []
        if token.encloses(init) and init != token.start_index:
            
            left_token_start = token.start_index
            left_token_end = init

            if left_token_end != left_token_start:
                left_token = TextToken(text = self._text,
                                   start_index = left_token_start,
                                   end_index = left_token_end - 1,
                                   tags_dict = token.tags_dictionary)

                tokens.append(left_token)
        
        if token.encloses(end) and end != token.end_index:
            
            rigth_token_start = end
            rigth_token_end = token.end_index
            if rigth_token_end != rigth_token_start:
                rigth_token = TextToken(text = self._text,
                                    start_index = rigth_token_start + 1,
                                    end_index = rigth_token_end,
                                    tags_dict = token.tags_dictionary)

                tokens.append(rigth_token)

        return tokens

    def get_sentences(self):
        sentences = []

        #TODO: reduce complexity
        for i, sentence in enumerate(self.sentences_tokens):
            words = []
            tags = []
            entity_types = []

            for token in sort_tokens(self.word_tokens + self.annotated_entities_tokens + self.predicted_entities_tokens):
                if sentence.encloses(token.start_index):
                    words.append(token.section)
                    tags.append((token.get_tag_value('IOB'),token.get_tag_value('tag')))
                    entity_types.append(token.get_tag_value('type'))

            sentences.append((words, tags, entity_types))
        
        return sentences