################################################################################
# Natural Language Toolkit (NLTK) basics
#
# Notes
# - The nltk package lacks good documentation and comments
#
# References
# - Real Python : https://realpython.com/nltk-nlp-python/
# - NLP in Python by NLTK authors: http://www.nltk.org/book/ - not a concise coverage of just NLTK (see Chs. 1,5,7)
# - Offical Webpage : https://www.nltk.org/
################################################################################

import nltk
# Using NLTK requires download data files
# See https://www.nltk.org/data.html

################################################################################
# Text objects
################################################################################

# Creating a text object
#from nltk import book # Takes a couple seconds
tokens = ['Token1', 'Token2', '']
text = nltk.Text(tokens)
assert(type(text) == nltk.Text)

# Attributes
# text.name
# text.tokens

# Searching Text
# text.count
# text.index
# text.findall
# text.concordance
# assert( list(text.concordance()) == text.concordance_list() )
# text.similar
# text.common_contexts

# Bigrams and Collocations
bg1 = list(nltk.bigrams('ABCD'))
bg2 = list(nltk.bigrams(['A', 'B', 'C', 'D']))
assert(bg1 == bg2 == [('A', 'B'), ('B', 'C'), ('C', 'D')])
# text.collocations ()
# assert( list(text.collocations()) == text.collocation_list() )

# Visualization
# text.dispersion_plot
# text.plot

# Unsorted
# text.generate
# text.vocab / nltk.FreqDist / collections.Counter
# text.readability


################################################################################
# Tokenizing
################################################################################
# from nltk import tokenize

text = "And now, for something completely different"

# Split string into word and punctuation tokens
tokens = nltk.word_tokenize(text)
assert(type(tokens) == list)
assert(tokens[:3] == ['And', 'now', ','])

# nltk.sent_tokenize()

################################################################################
# Normalizing Text
################################################################################
# Stemming - reduce words to their root
# [x for x in dir(nltk) if 'Stemmer' in x]
# stemmer = nltk.PorterStemmer()
# stemmer = nltk.LancasterStemmer()
# other stemmers ...
# stemmed_token = stemmer.stem(token)

# Lemmatization
# lemmatizer = nltk.WordNetLemmatizer()
# lemmatized_token = lemmatizer.lemmatize(token)

################################################################################
# Part-of-Speech (POS) tagging
################################################################################
# Identifying parts of speech for word tokens
pos = nltk.pos_tag(tokens)

# tag = 'RB'
# nltk.help.upenn_tagset()
# nltk.help.upenn_tagset(tag)

################################################################################
# Chunking and Chinking
################################################################################

# Chunk grammar
# grammar = "NP: {<DT>?<JJ>*<NN>}"
# chunk_parser = nltk.RegexpParser(grammar)
# tree = chunk_parser.parse(tagged_tokens)

########################################
# Tree class
# - Children can be either leaves (i.e. token-tag tuples) or subtrees 
########################################

# Creating Trees
# nltk.Tree(label, [tuple, subtree])
# nltk.fromstring(s)

# Attributes
# tree.label()

# Viewing
# tree[1]
# tree.leaves() - all contained token-tag tuples
# tree.draw()

# Modifying
# tree.set_label()

################################################################################
# Named Entity Recognition (NER)
################################################################################
# nltk.ne_chunk(tagged_tokens)


################################################################################
# Helpful reference lists
################################################################################
# Stopwords - Very common words (e.g. in, is, an, etc.)
# stopwords = set(nltk.corpus.stopwords.words('english'))
# assert(len(stopwords) == 179)

################################################################################
# Other methods and classes
################################################################################
