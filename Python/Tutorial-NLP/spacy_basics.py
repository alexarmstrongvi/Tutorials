################################################################################
# SpaCy
################################################################################

import spacy
nlp = spacy.load('en')

doc = nlp(my_doc_text)
#doc.sents
word = doc[0]
#dir(word)
word.text
word.pos_
word.tag_
word.lemma_

from spacy.lang.en.stop_words import STOP_WORDS
