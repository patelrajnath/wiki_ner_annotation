# Building a Massive Corpus for Named Entity Recognition using Free Open Data Sources
This repository contains the code used for building the dataset presented in the article "Building a Massive Corpus for Named Entity Recognition using Free Open Data Sources"


> Specht Menezes, Daniel, Pedro Savarese, and Ruy Luiz Milidiú. "Building a Massive Corpus for Named Entity Recognition using Free Open Data Sources." arXiv preprint arXiv:1908.05758 (2019).

Each folder corresponds to a python module:
 
 - ```wikipedia_builder``` - Reads and builds part of the database unsing a wikipedia dump in xml.
 - ```wikipedia_cleaner``` - Functionalities for cleaning the undesired elements of wikitext in the portuguese language from the wikipedia articles.
 - ```ner_corpus_annotation_pipeline``` - Tokenization of sentences and words applying preprocessing rules preserving the already known entities and discovering new ones.
 - ```statistics``` - Functinalities for extracting some descriptive statistics from the dataset. 

 Notebooks:
  - ```Builder.ipynb``` - wraps it all up
 