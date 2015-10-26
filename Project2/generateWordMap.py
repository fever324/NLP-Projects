from nltk.corpus import wordnet as wn
import utils

# Unigram weight
alpha = 0.8


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
