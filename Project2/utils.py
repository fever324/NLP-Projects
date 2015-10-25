from nltk import pos_tag, word_tokenize


def remove_unwanted_tags(string, unwantedTags):

    wordTagPairs = pos_tag(word_tokenize(string))
    returnString = ''
    for word in wordTagPairs:
        if(word[1] not in unwantedTags):
            returnString += word[0] + ' '
    return returnString


def construct_unwanted_tags():

    unwantedTags = set()
    l = ['$', '\'\'', '(', ')', ',', '--', '.', ':', 'CC', 'CD', 'DT', 'EX', 'IN', 'PDT', 'LS', 'MD', 'POS', 'PRP', 'PRP$', 'RP', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB', '``']

    for t in l:
        unwantedTags.add(t)
    return unwantedTags
