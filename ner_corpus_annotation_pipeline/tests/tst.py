import os, sys
# get the code path in a cross platform way
code_path = os.path.abspath(os.pardir)
sys.path.insert(0,'/home/daniel/Repositories/Dissertação/final/ner_corpus_annotation_pipeline')
from src import  NerCorpusAnnotationPipeline, Entity

text = 'Olá, meu nome é Daniel Specht Menezes, mas alguns me cha . mam de José.^~ []123 Entendeu? I.B.M.BMBB . IBM'
text = 'kljsafdksfdklj klsajfd lçadjf lçsajdf çldkjf klçl'
text = ''
text = 'Daniel Specht Menezes Olá, meu nome é Daniel Specht Menezes. Vou ao Mercado da Índia com meu amigo Daniel Specht Menezes, Mercado.'

#text = 'Olá, meu nome é Daniel Specht Menezes, mas alguns me chamam de José.^~ []21[34] Entendeu? Amanhã vou na IBM.'
e2 = Entity(names = ['Mercado', 'José','cha . mam'], tag = 'LOC')
e1 = Entity(names = ['Daniel Specht Menezes', 'Daniel','cha . mam'], tag = 'PER')
#e2 = Entity(names = ['Mercado', 'José','cha . mam'], tag = 'PER')


entities = [e1, e2]
pipeline = NerCorpusAnnotationPipeline(text, entities)
pipeline.apply_processing_rules()
sentences = pipeline.get_sentences()
print(len(sentences))
for words, tags, types in sentences:
   for i in range(len(words)):
       print(words[i],'---',tags[i],'---',types[i])
   print('\n=====\n')