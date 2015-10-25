#Report of Project 2: Word Sense Disambiguation

## Shibo Zang(sz428) Hongfei Li(hl963)
  
### 1. Approach

For our WSD system, we implement our idea propsed in the proposal， which is to use supervised learning algorithm -- Naive Bayes as the classifier of Word Sense Disambiguation and to use WordNet dictionary to select feature vectors.

We divided our system into several sub-functions:

1. Data cleaning and data preprocessing:  
We first eliminated punctuations and meaningless words in the corpus such as prepositions, conjunctions, articles, pronouns, interjections, quantifiers, auxillaries, etc., using part-of-speech tagging. The tagging type is shown below.  

```python
def construct_unwanted_tags():
    unwantedTags = set()
    l = ['$', '\'\'', '(', ')', ',', '--', '.', ':', 'CC', 'CD', 'DT', 'EX', 'IN', 'PDT', 'LS', 'MD', 'POS', 'PRP', 'PRP$', 'RP', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB', '``']

    for t in l:
        unwantedTags.add(t)
    return unwantedTags
```

From above codes, we see that 26 types of words are eliminated after preprocessing.  
Also we noticed that there are so many nonsense words suffix and prefix left after pos-tagging that we had to delete them specifically, like "n't", "'ll", "'s", "'re", etc.

     
Then we will look at previous 10 words and following 10 words around the target word. We will process these 20 words based on their definitions in the dictionary and reward those words (increase their weights in the feature vector) which have consecutive overlap with the definition of target word. And of course we also need to process the content of words in dictionary, which means to keep nouns, adjectives, verbs, and adverbs. Finally we would get the feature vectors we want and apply them to the Naive Bayes classifier.
