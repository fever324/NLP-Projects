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
From above codes, we see that the unwanted set are turned into a set for better look up performance in the next steps. 


1.2 Once we have the unwanted word tags, we will start parsing the data file and remove words with unwanted tag, and transform the remaining words to their simplest form. The following codes are used to do so. Details of the following code will be discussed in section 2.0.

```python

def remove_unwanted_tags(string, unwantedTags):
    wordTagPairs = pos_tag(word_tokenize(string))
    returnTags = []
    for word in wordTagPairs:
        if(word[1] not in unwantedTags) and len(word[0]) != 0 
        	and len(word[0]) != 1 and word[0] != 'n\'t' 
        	and word[0] != '\'s' and word[0] != '\'ll':
            returnTags.append(word)
    return returnTags
    
def sentence_to_present_tense_and_single(tags):
    for i in range(len(tags)):
        wn_tag = penn_to_wn(tags[i][1])
        tags[i] = WordNetLemmatizer().lemmatize(tags[i][0], wn_tag)
    return tags
```

The input corpus are processed using the above methods and ```processed_trainig.xml``` is generated for training purpose.   


2. Training:




<!--Word definition overlap count-->
2.3 In order to use dictionary to help us pick feature words, a helper method ```get_word_definition_overlap_count``` is written. This method is used to calculate a score that represents how close two words' meanings are. The approach is that firstly we combines are definitions of two words into two large strings, then we calculate number of bigrams and unigrams that overlaps in the two large strings. Secondly, since it is highly possible that duplilcate words will exist in a large string, and number of occurences does not matter in our case, we used a set of words to represent the combined definitions of a word. Lastly, once we have bigram and ungram overlap counts, we used weight index alpha to calculate score. Current weight for unigram is 0.3 and for bigram is 0.7.

```python
# Unigram weight
alpha = 0.3


def get_word_definition_overlap_count(a, b):
    unwantedTags = utils.construct_unwanted_tags()
    defs_a = wn.synsets(a)
    defs_b = wn.synsets(b)

    # Unigram overlap count
    unigramOverlapCount = 0
    bigramOverlapCount = 0
    aUnigramSet = set()
    bUnigramSet = set()
    aBigramSet = set()
    bBigramSet = set()
    # Construct a ngram sets
    for d in defs_a:
        aUnigramArray = utils.process_string(
            d.definition().lower(), unwantedTags).split()

        # Unigram
        add_list_to_set(aUnigramSet, aUnigramArray)
        # Bigram
        for i in range(len(aUnigramArray) - 1):
            aBigramSet.add(aUnigramArray[i] + aUnigramArray[i + 1])

    # Construct b ngram sets
    for d in defs_b:
        bUnigramArray = utils.process_string(
            d.definition().lower(), unwantedTags).split()
        # Unigram
        add_list_to_set(bUnigramSet, bUnigramArray)

        # Bigram
        for i in range(len(bUnigramArray) - 1):
            bBigramSet.add(bUnigramArray[i] + bUnigramArray[i + 1])

    for word in bUnigramSet:
        if(word in aUnigramSet):
            unigramOverlapCount += 1
    for word in bBigramSet:
        if word in aBigramSet:
            bigramOverlapCount += 1
    return unigramOverlapCount * alpha + bigramOverlapCount * (1 - alpha)


def add_list_to_set(setS, l):
    for a in l:
        setS.add(a)
```





Then we will look at previous 10 words and following 10 words around the target word. We will process these 20 words based on their definitions in the dictionary and reward those words (increase their weights in the feature vector) which have consecutive overlap with the definition of target word. And of course we also need to process the content of words in dictionary, which means to keep nouns, adjectives, verbs, and adverbs. Finally we would get the feature vectors we want and apply them to the Naive Bayes classifier.

```python
def word_sense_disambiguation(featureProbabilityDictionary, priorProbabilityDictionary, context, instanceString):
    sense_ids = featureProbabilityDictionary[instanceString]
    sense_id_scores = {}
    surround_words = []
    if(context.text is not None):
        surround_words = context.text.strip().split()[-10:]

    for head in context:
        if(head.tail is None):
            continue
        surround_words += head.tail.strip().split()
        if len(surround_words) > 20:
            break
    surround_words = surround_words[:20]

    for sense_id, featureProbility in sense_ids.iteritems():
        if sense_id == '<unk>':
            continue

        sense_id_scores[sense_id] = priorProbabilityDictionary[
            instanceString][sense_id]

        for word in surround_words:
            if word in featureProbility:
                sense_id_scores[sense_id] *= featureProbility[word]
            else:
                sense_id_scores[sense_id] *= sense_ids['<unk>']


    # return the sense_id with max score
    return max(sense_id_scores.iteritems(), key=operator.itemgetter(1))[0]
```

In the above code, we calculated the score of each sense id in every given context, and use the sense id with highest score as the meaning of the word in given context. The scoring method is simply multiplying the probabiliy of occurence of the words that surrounds the target word. The probabily of feature words and unknow words are read from ```feature_dict.json``` and ```prior_prob.json``` which are calculated from the naive-bayes-trainng section.




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


