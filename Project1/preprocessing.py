import nltk
import sys
import os
import io
import operator
import random
# import pdb
# pdb.set_trace()

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    directory = '/Users/hongfeili/Documents/school/2015fall/CS4740 NLP/Project1/books/train_books/history/'

    files = os.listdir(directory)
    tokens = []
    for file in files:
        print "Scanning through " + file + "..."
        f = io.open(directory+file, 'r', encoding="utf-8")
        for line in f.readlines():
            tokens+=nltk.word_tokenize(line)

    seed = ""
    while(seed != "Exit!!"):
        seed = raw_input('Enter Seed: ')
        if seed == "GT":
            print good_turing_discounting(getWordCount(tokens))
        else:
            print bigram_sentence_generator(seed, tokens)


def getWordCount(tokens):
    counts = {}
    for token in tokens:
        if counts.has_key(token):
            counts[token] += 1
        else:
            counts[token] = 1
    return counts

def bigram(tokens):
    wordCount = getWordCount(tokens)

    #f = open('containsI.txt', 'w')
    bigram_counts = {}
    for i in range(len(tokens) - 1):
        bigram = tokens[i] + " " + tokens[i + 1]
        # if(tokens[i] == "I"):
        #     f.write(tokens[i+1]+"\n")

        if bigram_counts.has_key(bigram):
            bigram_counts[bigram] += 1
        else:
            bigram_counts[bigram] = 1

    prob = {}
    for bigram, count in bigram_counts.iteritems():
        wn_1_count = wordCount[bigram.split()[0]]
        prob[bigram] = count / float(wn_1_count)

    seeding = {}
    for i in range(len(tokens) - 1):
        if not seeding.has_key(tokens[i]):
            seeding[tokens[i]] = set()

        seeding[tokens[i]].add(tokens[i+1])
        
    return (prob, seeding)

def unigram(tokens):
    counts = getWordCount(tokens)
    total_words_number = float(len(tokens))

    for word,count in counts.iteritems():
        counts[word] = count / total_words_number

def good_turing_discounting(counts):
    numberOfCounts = {}

    # Get Nc
    for word, count in counts.iteritems():
        if str(count) not in numberOfCounts:
            numberOfCounts[str(count)] = 0
        numberOfCounts[str(count)] += count
    
    # Get c*
    goodTurningProbabilities = {}
    for word, count in counts.iteritems():
        if word not in goodTurningProbabilities:
            if count < 10:
                goodTurningProbabilities[word] = (count+1)* numberOfCounts[str(count+1)] / numberOfCounts[str(count)]

    return goodTurningProbabilities
    #return numberOfCounts



def bigram_sentence_generator(seed, tokens):
    prob, seeding = bigram(tokens)    
    
    returnString = seed.strip()
    
    while(not is_terminator(returnString[-1:])):  
        wordsInSeed =seed.split()
        lastWordInSeed = wordsInSeed[-1]

        if not seeding.has_key(lastWordInSeed):
            return returnString+".\n"

        possibleWordSet = seeding[lastWordInSeed]
        l = []
        for item in possibleWordSet:
            a = prob[lastWordInSeed + " " + item]
            l.append((item, a))

        l.sort(key=operator.itemgetter(1))

        randomNumber = random.random()

        #possibleWord -> (word, probability)
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

if __name__ == "__main__":
    main()

