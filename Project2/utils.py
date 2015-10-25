from nltk import pos_tag, word_tokenize
import en
import sys


def process_string(string, unwantedTags):
    # Remove irrelevent words such as 'and', 'the'
    string = remove_unwanted_tags(string, unwantedTags)

    # Turn sentence to single and present tense for easier analysis
    string = sentence_to_present_tense_and_single(string)
    return string


def remove_unwanted_tags(string, unwantedTags):

    wordTagPairs = pos_tag(word_tokenize(string))
    returnString = ''
    for word in wordTagPairs:
        if(word[1] not in unwantedTags):
            returnString += word[0] + ' '
    return returnString


def construct_unwanted_tags():

    unwantedTags = set()
    l = ['$', '\'\'', '(', ')', ',', '--', '.', ':', 'CC', 'CD', 'DT', 'EX', 'IN', 'PDT', 'LS',
         'MD', 'POS', 'PRP', 'PRP$', 'RP', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB', '``']

    for t in l:
        unwantedTags.add(t)
    return unwantedTags


def sentence_to_present_tense_and_single(string):
    words = string.split()
    returnString = ''
    for word in words:
        # Remove single letter word
        if len(word) != 1:
            try:
                if en.is_noun(word):
                    returnString += ' ' + en.noun.singular(word)
                elif en.is_verb(word):
                    returnString += ' ' + en.verb.present(word)
                else:
                    returnString += ' ' + word
            except:
                print 'cannot process word ' + word

    return returnString.strip()
