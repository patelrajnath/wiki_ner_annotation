from bson.objectid import ObjectId
from collections import OrderedDict, defaultdict
import pymongo as mongo
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
class DatasetStatistics():

    def __init__(self,
                 host,
                 port,
                 verbose):

        self._client = mongo.MongoClient(host, port)
        self._verbose = verbose

        self._sentences_stats = None
        self._articles_stats = None

    @property
    def df(self):
        return self._sentences_stats
    
    @df.setter
    def df(self, df):
        self._sentences_stats = df

    def load_sentences_stats(self, path):
        self._verbose_print('Loading sentences statistics to pickle')
        self._sentences_stats = pd.read_pickle(path)

    def load_articles_stats(self, path):
        self._verbose_print('Loading articles statistics to pickle')
        self._articles_stats = pd.read_pickle(path)
        
    def save_articles_stats(self, path):
        self._verbose_print('Writing articles statistics to pickle')
        self._sentences_stats.to_pickle(path)
    
    def save_sentences_stats(self, path):
        self._verbose_print('Writing sentences statistics to pickle')
        self._sentences_stats.to_pickle(path)

    #def total_sentences(self):
    #    if not self._total_sentences:
    #        self._total_sentences = self._count_sentences_from_db()
    #    return self._total_sentences

    # def _count_sentences_from_db(self):
    #     self._verbose_print('Counting sentences ...')
    #     total_sentences = 0
        
    #     for article in self.yield_sentences():
    #         total_sentences += len(article['sentences'])
    #     self._verbose_print('Found %d'%(total_sentences))
    #     return total_sentences

    def make_sent_stats_table(self):
        self._verbose_print('Building stats table...')

        # let the bodies hit the floor
        article = []
        nth_a = []
        nth_s = []
        word_count = []
        ORG_anot_length_count = []
        LOC_anot_length_count = []
        PER_anot_length_count = []
        ORG_pred_length_count = []
        LOC_pred_length_count = []
        PER_pred_length_count = []
        ORG_pred_count = []
        LOC_pred_count = []
        PER_pred_count = []
        ORG_anot_count = []
        LOC_anot_count = []
        PER_anot_count = []

        B_ORG_anot = []
        B_LOC_anot = []
        B_PER_anot = []
        I_ORG_anot = []
        I_LOC_anot = []
        I_PER_anot = []
        B_ORG_pred = []
        B_LOC_pred = []
        B_PER_pred = []
        I_ORG_pred = []
        I_LOC_pred = []
        I_PER_pred = []
        O = []



        sources = ['annotated','predicted']
        tags = ['PER','ORG','LOC']
        prefixes = ['I', 'B']

        article_columns = ['sentence_count', 'article_id']
        sentence_columns = ['nth_sentence','word_count']
        tokens_columns = []

        self._verbose_print('1/2 Building stats table...')
        for nth_article, (article_id, sentences) in enumerate(self.yield_sentences()):
            article_id = str(article_id)
            for nth_sent, sentence in enumerate(sentences):
                article.append(article_id)
                nth_a.append(nth_article)
                nth_s.append(nth_sent)
                word_count.append(len(sentence['tokens']))
                ORG_anot_length_count.append(self._get_mention_lengths('annotated', 'ORG', sentence))
                LOC_anot_length_count.append(self._get_mention_lengths('annotated', 'LOC', sentence))
                PER_anot_length_count.append(self._get_mention_lengths('annotated', 'PER', sentence))
                
                ORG_pred_length_count.append(self._get_mention_lengths('predicted', 'ORG', sentence))
                LOC_pred_length_count.append(self._get_mention_lengths('predicted', 'LOC', sentence))
                PER_pred_length_count.append(self._get_mention_lengths('predicted', 'PER', sentence))
                
                ORG_pred_count.append(self._get_sent_mention_count('predicted', 'ORG', sentence))
                LOC_pred_count.append(self._get_sent_mention_count('predicted', 'LOC', sentence))
                PER_pred_count.append(self._get_sent_mention_count('predicted', 'PER', sentence))
                ORG_anot_count.append(self._get_sent_mention_count('annotated', 'ORG', sentence))
                LOC_anot_count.append(self._get_sent_mention_count('annotated', 'LOC', sentence))
                PER_anot_count.append(self._get_sent_mention_count('annotated', 'PER', sentence))

                sent_tokens_stats = self.get_sent_stats(sentence)

                B_ORG_anot.append(sent_tokens_stats['B_ORG_annotated'])
                B_LOC_anot.append(sent_tokens_stats['B_LOC_annotated'])
                B_PER_anot.append(sent_tokens_stats['B_PER_annotated'])
                I_ORG_anot.append(sent_tokens_stats['I_ORG_annotated'])
                I_LOC_anot.append(sent_tokens_stats['I_LOC_annotated'])
                I_PER_anot.append(sent_tokens_stats['I_PER_annotated'])
                B_ORG_pred.append(sent_tokens_stats['B_ORG_predicted'])
                B_LOC_pred.append(sent_tokens_stats['B_LOC_predicted'])
                B_PER_pred.append(sent_tokens_stats['B_PER_predicted'])
                I_ORG_pred.append(sent_tokens_stats['I_ORG_predicted'])
                I_LOC_pred.append(sent_tokens_stats['I_LOC_predicted'])
                I_PER_pred.append(sent_tokens_stats['I_PER_predicted'])
                O.append(sent_tokens_stats['O'])


    
        # tokens count by tag
        

        self._verbose_print('2/2 Building stats data frame...')
        
        self._sentences_stats = pd.DataFrame()
        self._sentences_stats['article_id'] = article
        self._sentences_stats['nth_article'] = nth_a
        self._sentences_stats['nth_sentence'] = nth_s # TODO: Typo
        self._sentences_stats['word_count'] = word_count
        self._sentences_stats['ORG_anot_length_count'] = ORG_anot_length_count

        self._sentences_stats['LOC_anot_length_count'] = LOC_anot_length_count
        self._sentences_stats['PER_anot_length_count'] = PER_anot_length_count
        self._sentences_stats['ORG_pred_length_count'] = ORG_pred_length_count
        self._sentences_stats['LOC_pred_length_count'] = LOC_pred_length_count
        self._sentences_stats['PER_pred_length_count'] = PER_pred_length_count
        self._sentences_stats['ORG_pred_count'] = ORG_pred_count
        self._sentences_stats['LOC_pred_count'] = LOC_pred_count
        self._sentences_stats['PER_pred_count'] = PER_pred_count
        self._sentences_stats['ORG_anot_count'] = ORG_anot_count
        self._sentences_stats['LOC_anot_count'] = LOC_anot_count
        self._sentences_stats['PER_anot_count'] = PER_anot_count
        
        self._sentences_stats['B_ORG_anot'] = B_ORG_anot
        self._sentences_stats['B_LOC_anot'] = B_LOC_anot
        self._sentences_stats['B_PER_anot'] = B_PER_anot
        self._sentences_stats['I_ORG_anot'] = I_ORG_anot
        self._sentences_stats['I_LOC_anot'] = I_LOC_anot
        self._sentences_stats['I_PER_anot'] = I_PER_anot
        self._sentences_stats['B_ORG_pred'] = B_ORG_pred
        self._sentences_stats['B_LOC_pred'] = B_LOC_pred
        self._sentences_stats['B_PER_pred'] = B_PER_pred
        self._sentences_stats['I_ORG_pred'] = I_ORG_pred
        self._sentences_stats['I_LOC_pred'] = I_LOC_pred
        self._sentences_stats['I_PER_pred'] = I_PER_pred
        self._sentences_stats['O'] = O

        self._verbose_print('Done!')

    def get_sent_stats(self, sent):
        
        sources = ['annotated','predicted']        
        kinds = ['PER','ORG','LOC']
        prefixes = ['I', 'B']
        #tags = [p+'-'+k for k in kinds for p in prefixes]
        keys = ['_'.join([p,k,s]) for p in prefixes for s in sources for k in kinds] + ['O']
        infos = dict.fromkeys(keys, 0)

        for token in sent['tokens']:
            tag = token[1]
            if tag == 'O':
                infos[tag] += 1
                continue
                
            tag = tag.replace('-', '_')
            origin = token[2]
            key = tag + '_' + origin
            infos[key] += 1
        return infos

    def _get_mention_lengths(self, origin, tag, sentence):
        lengths_dict = sentence['infos'][origin]['lengths_by_type']
        return lengths_dict[tag] if tag in lengths_dict else []

    def _get_sent_mention_count(self, origin, tag, sentence):
        counts_dict = sentence['infos'][origin]['type_count']
        return counts_dict[tag] if tag in counts_dict else 0


    def describe_senteneces_len(self, min_sent_len = None, max_sent_len = None, x_tick = None, figsize = (10, 10)):
        # build a dictionary to be used in describing the sentences len
        # sentence length to number of occurences
        counts = self._sentences_stats['word_count'].value_counts().to_dict()
        counts = dict(OrderedDict(sorted(counts.items())))
        counts = {str(key):value for key, value in counts.items()}

        # pandas df and plot config
        df = pd.DataFrame(list(counts.items()))
        ax = df.plot(kind='bar', legend = False, figsize = figsize, color='#E24A33')#,xticks = [2,3])#["1","2","3","4"])

        # set the interval for the x axis
        min_x = min_sent_len if min_sent_len else 0
        max_x = max_sent_len if max_sent_len else max(map(lambda k: int(k), list(counts.keys())))
        
        ax.set_xlim(min_x, max_x)
        # set the tick for the x axis
        if x_tick:
            for i, tick in enumerate(ax.xaxis.get_major_ticks()):
                if i%x_tick == 0:
                    tick.set_visible(True)
                elif max_sent_len and i == max_sent_len:
                    tick.set_visible(True)
                elif min_sent_len and i == min_sent_len:
                    tick.set_visible(True)
                else:
                    tick.set_visible(False)
        

        # number size
        #plt.bar(x, y, color='#E24A33')
        ax.tick_params(axis = 'both', which = 'major', labelsize = 15)
        fig = ax.get_figure()


    def plot_token_class_proportion(self, classes = ['O','I-ORG','I-PER','I-LOC','B-ORG','B-PER','B-LOC'], figsize = (10,10)):
        # Plot the tags proportion
        for cls in classes:
            if cls == 'O':
                continue
            cls_aux = cls.replace('-','_')
            self._sentences_stats[cls] = self._sentences_stats[cls_aux+'_anot'] + self._sentences_stats[cls_aux+'_pred']


        series = self._sentences_stats[classes].sum()
        series.plot.pie(figsize = figsize, subplots=True, legend = True, labels = ['']*len(classes)) #, title = 'IOB labels distribution')
        plt.legend(classes, loc=3, fontsize = 15)
        plt.ylabel('')


    def print_sentences_to_iob(self, path, add_origin = False):

        with open(path, 'w') as iob_file:
            for art_id_str, article_group in self._sentences_stats.groupby(['article_id']):
                _id = ObjectId(art_id_str)
                article = self._client['wikipedia_ner_corpus']['wikipedia_article'].find_one({'_id':_id},projection = ['sentences'])
                sentences = [sentence['tokens'] for sentence in article['sentences']]

                for i in article_group['nth_sentence']:
                    iob_file.writelines(self._get_sentences_lines(sentences[i], add_origin))
                
    def _get_sentences_lines(self, tokens, add_origin):
        lines = None
        if add_origin:
            lines = [' '.join([token[0], token[1], token[2]]) + '\n' for token in tokens] + ['\n']
        else:
            lines = [' '.join([token[0], token[1]]) + '\n' for token in tokens] + ['\n']

        return lines
    
    def yield_sentences(self):
        debug_n_arts = None
        count = 0
        for article in self._client['wikipedia_ner_corpus']['wikipedia_article'].find(projection = ['sentences']):
            yield article['_id'], article['sentences']
            count += 1
            if debug_n_arts and debug_n_arts < count:
                print(count)
                break

    def _verbose_print(self, text):
        if self._verbose:
            print(text)

    def plot_entity_origin(self, figsize = (10, 10)):
        tags = ['ORG','LOC','PER']
        anot_keys = ['B_ORG_anot', 'B_LOC_anot', 'B_PER_anot']
        pred_keys = ['B_ORG_pred', 'B_LOC_pred', 'B_PER_pred']

        totals_pred = [self.df[key].sum() for key in pred_keys]
        totals_anot = [self.df[key].sum() for key in anot_keys]

        fig, ax = plt.subplots(figsize = figsize)
        index = np.arange(len(tags))
        bar_width = 0.35

        rects1 = ax.bar(index,
                        totals_pred,
                        bar_width,
                        color ='#8EBA42',
                        #yerr=std_men,
                        #error_kw = error_config,
                        label = 'Predicted')

        rects2 = ax.bar(index + bar_width,
                        totals_anot,
                        bar_width,
                        color='#E24A33',
                        #yerr=std_women,
                        #error_kw=error_config,
                        label= 'Annotated')

        plt.legend(tags,loc=3, fontsize = 15)
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(tags, fontsize = 15)
        matplotlib.rc('figure', figsize=(15, 15))
        ax.legend(loc = 1, fontsize = 15)
        # number size
        ax = plt.gca()
        ax.tick_params(axis = 'both', which = 'major', labelsize = 15)