#Project 2 Report: Word Sense Disambiguation

## Shibo Zang(sz428) Hongfei Li(hl963)
  
### 1. Approach

For our WSD system, we implement our idea described in the proposal， which is to use supervised learning algorithm -- Naive Bayes as the classifier of Word Sense Disambiguation and to use WordNet dictionary to select feature vectors.

We divide our system into several sub-functions:

1. Data cleaning and data preprocessing:  
1.1 We first eliminate punctuations and meaningless words in the corpus such as prepositions, conjunctions, articles, pronouns, interjections, quantifiers, auxillaries, etc., using part-of-speech tagging. The tagging type is showned below.  

```python
def construct_unwanted_tags():
    unwantedTags = set()
    l = ['$', '\'\'', '(', ')', ',', '--', '.', ':', 'CC', 'CD', 
    'DT', 'EX', 'IN', 'PDT', 'LS', 'MD', 'POS', 'PRP',
    'PRP$', 'RP', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB', '``']

    for t in l:
        unwantedTags.add(t)
    return unwantedTags
```

From above codes, we see that the unwanted are turned into a set for better look up performance in the next steps. 


Then we will look at previous 10 words and following 10 words around the target word. We will process these 20 words based on their definitions in the dictionary and reward those words (increase their weights in the feature vector) which have consecutive overlap with the definition of target word. And of course we also need to process the content of words in dictionary, which means to keep nouns, adjectives, verbs, and adverbs. Finally we would get the feature vectors we want and apply them to the Naive Bayes classifier.







### 2.Software

Python's ```xml.etree.ElementTree``` class to parse the given data file. However removing ```&``` from the data files and add a ```<root>``` to the beginning to the data files were necessary manual process in order to have ```ElementTree``` function correctly.

```python
tree = ET.parse('processed_training.xml')
root = tree.getroot()
lexelts = root.findall("./lexelt")
```

Python nltk library to was used to tokenize sentences and do POS tagging.

```python
wordTagPairs = pos_tag(word_tokenize(string))
```

The above line of code will return a list of word tag pairs such as   

```python
[('delicious','JJ')('apple','NN'),.....]
```
    
      
Using the word tags obtained above, nltk's ```WordNetLemmatizer``` function was used to transform words to their simple form for analysis optimization.  
For example, here is a table of words that were transformed. 

|Original Word | Transformed Word |
|:--------------:|:-----------------:|
|apples | apple  |
|happier | happy |
|runned | run 		|
|harder | hard	|

####Code example
```python
def sentence_to_present_tense_and_single(tags):
    for i in range(len(tags)):
        wn_tag = penn_to_wn(tags[i][1])
        tags[i] = WordNetLemmatizer().lemmatize(tags[i][0], wn_tag)
    return tags

def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']

def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']

def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']

def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return wn.NOUN
```


The wordnet corpus that was built within nltk was used to obtain definitions of words
####Code example
```python
from nltk.corpus import wordnet as wn

defs = wn.synsets('apple')

```


