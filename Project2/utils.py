from nltk import pos_tag, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import nltk
import en
import sys


def process_string(string, unwantedTags):
    # Remove irrelevent words such as 'and', 'the'
    tags = remove_unwanted_tags(string.lower(), unwantedTags)

    # Turn sentence to single and present tense for easier analysis
    tags = sentence_to_present_tense_and_single(tags)
    return turn_tags_to_string(tags)


def remove_unwanted_tags(string, unwantedTags):

    wordTagPairs = pos_tag(word_tokenize(string))
    returnTags = []
    for word in wordTagPairs:
        if(word[1] not in unwantedTags) and len(word[0]) != 1 and word[0] != 'n\'t' and word[0] != '\'s':
            returnTags += word
    return returnTags


def construct_unwanted_tags():

    unwantedTags = set()
    l = ['$', '\'\'', '(', ')', ',', '--', '.', ':', 'CC', 'CD', 'DT', 'EX', 'IN', 'PDT', 'LS',
         'MD', 'POS', 'PRP', 'PRP$', 'RP', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB', '``']

    for t in l:
        unwantedTags.add(t)
    return unwantedTags


def sentence_to_present_tense_and_single(tags):
    for i in range(len(tags)):
        wn_tag = penn_to_wn(tags[i][1])
        tags[i] = WordNetLemmatizer().lemmatize(tags[i][0], wn_tag)
    return tags


def turn_tags_to_string(tags):
    toReturn = ''
    for tag in tags:
        toReturn += tag[0]
    return toReturn

# def sentence_to_present_tense_and_single(string):
#     words = string.split()
#     returnString = ''
#     for word in words:
#         # Remove single letter word
#         if word == 'n\'t':
#             continue
#         if len(word) != 1:
#             try:
#                 if en.is_noun(word):
#                     returnString += ' ' + en.noun.singular(word)
#                 elif en.is_verb(word):
#                     returnString += ' ' + en.verb.present(word)
#                 else:
#                     returnString += ' ' + word
#             except:
#                 print 'cannot process word ' + word

#     return returnString.strip()


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
