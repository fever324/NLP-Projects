import nltk
import sys
import os
import io
import random
import math
import pprint
from bigram import Bigram
from trigram import Trigram
# import pdb
# pdb.set_trace()


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    seed = ""
    bigramModels = None
    mode = ""
    while(seed != "Exit!!"):
        if mode == "":
            mode = raw_input(
                'Select running mode: \n\tSentence generator - sg\n\tPerplexity - pp\n')
        elif mode == "pp":
            bigramModels = generate_bigram_models(True)
            book_analyse(bigramModels)

            seed = "Exit!!"
        else:
            if(bigramModels is None):
                bigramModels = generate_bigram_models(False)
            seed = raw_input('Enter Seed: ')
            print bigram_sentence_generator(seed, bigramModels["children"])


def generate_bigram_models(useUNK):

    currentDirectory = os.path.dirname(os.path.realpath(__file__))

    trainingDirectory = currentDirectory + "/books/train_books/"
    genres = os.listdir(trainingDirectory)

    bigramModels = {}
    for genre in genres:
        print "\nGenerating model for " + genre + " genre"
        tokens = get_tokens_from_directory(
            trainingDirectory + "/" + genre + "/", useUNK=useUNK)
        bigramModels[genre] = Bigram(tokens, usingGoodTuring=True)
    return bigramModels


def book_analyse(bigramModels):
    currentDirectory = os.path.dirname(os.path.realpath(__file__))

    trainingDirectory = currentDirectory + "/books/train_books/"
    genres = os.listdir(trainingDirectory)

    testDirectory = currentDirectory + "/books/test_books/"
    genres = os.listdir(testDirectory)
    testResults = {}
    for genre in genres:
        genreDirectory = testDirectory + genre
        for f in os.listdir(testDirectory + genre):
            print "\nAnalysing book " + f + " under genre " + genre
            fileDirectory = genreDirectory + "/" + f
            bookTokens = get_tokens_from_file(fileDirectory)
            minPP = sys.maxint
            resultGenre = ""
            for key, model in bigramModels.iteritems():
                pp = run_perplexity(model, bookTokens)
                print "Perplexity for " + key + " model is " + str(pp)
                if pp < minPP:
                    minPP = pp
                    resultGenre = key
            testResults[f] = resultGenre

    print "---------------------------------------"
    print "Here are the results"
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(testResults)


def get_tokens_from_file(fileDirectory, useUNK=False):
    seenTokens = set()
    tokens = []
    with io.open(fileDirectory, 'r', encoding='utf-8') as book:
        content = book.read()
        tokens = nltk.word_tokenize(content)
        if useUNK:
            for i in range(len(tokens)):
                token = tokens[i]
                if token not in seenTokens:
                    seenTokens.add(token)
                    tokens[i] = "<UNK>"
    return tokens


def get_tokens_from_directory(directory, useUNK=False):
    files = os.listdir(directory)
    tokens = []
    for file in files:
        print "Loading " + file + "..."
        fileDirectory = directory + file
        tokens += get_tokens_from_file(fileDirectory, useUNK)

    return tokens


def run_perplexity(model, testTokens):
    pp = 0
    for i in range(len(testTokens) - 2):
        bigram = testTokens[i] + " " + \
            testTokens[i + 1] + " " + testTokens[i + 2]
    for i in range(len(testTokens) - 1):
        bigram = testTokens[i] + " " + testTokens[i + 1]
        prob = model.get_probability(bigram)
        # print "Probability \t " + bigram + " \t " + str(prob)
        pp += -math.log(prob)
    pp /= (len(testTokens) - 1)
    # print "PP is " + str(pp)
    return math.exp(pp)


def bigram_sentence_generator(seed, bigram):
    bagOfSeeds = bigram.bagOfSeeds

    returnString = seed.strip()

    while(not is_terminator(returnString[-1:])):
        wordsInSeed = seed.split()
        lastWordInSeed = wordsInSeed[-1]

        if not lastWordInSeed in bagOfSeeds:
            return returnString + ".\n"

        possibleWordSet = bagOfSeeds[lastWordInSeed]
        l = []
        for item in possibleWordSet:
            a = bigram.get_probability(lastWordInSeed + " " + item)
            l.append((item, a))

        randomNumber = random.random()

        # possibleWord -> (word, probability)
        for possibleWord in l:
            if randomNumber < possibleWord[1]:
                returnString += (" " + possibleWord[0])
                seed = possibleWord[0]
                break
            else:
                randomNumber -= possibleWord[1]

    return returnString + "\n"


def is_terminator(str):
    return str == "." or str == "?" or str == "!"


def get_unigram_model(tokens):
    counts = get_word_count(tokens)
    total_words_number = float(len(tokens))

    for word, count in counts.iteritems():
        counts[word] = count / float(total_words_number)
    return counts

if __name__ == "__main__":
    main()
