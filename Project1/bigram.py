class Bigram(object):

    def __init__(self, tokens, usingGoodTuring=False):
        self.tokens = tokens
        self.usingGoodTuring = usingGoodTuring
        self.probability = {}
        self.__generate_bigram_model(usingGoodTuring)

    def get_probability(self, string):

        numberOfAllPossibleBigramCombination = len(
            self.bagOfSeeds) ** 2
        if string in self.probability:
            return self.probability[string]
        else:
            # This part handles unknown words
            if not self.usingGoodTuring:
                return 0
            else:
                N1 = self.numberOfCounts["1"]

                if 'numberOfSeenBigram' not in locals():
                    self.numberOfSeenBigram = len(self.bigramCounts)
                N0 = numberOfAllPossibleBigramCombination - \
                    self.numberOfSeenBigram
                leadingWord = string.split()[0]
                if leadingWord not in self.wordCount:
                    leadingWord = "<UNK>"
                return N1 / float(N0) / float(self.wordCount[leadingWord])

    def __generate_bigram_model(self, usingGoodTuring=False):
        self.wordCount = self.__generate_word_count()
        self.bigramCounts = self.__generate_bigram_counts()

        # Smooth the counting
        if usingGoodTuring:
            self.bigramCounts = self.__good_turing_discounting(
                self.bigramCounts)

        # Probability of bigrams
        self.probability = {}
        for bigram, count in self.bigramCounts.iteritems():
            leadingWord = bigram.split()[0]
            if leadingWord != "<UNK>":
                wn_1_count = self.wordCount[bigram.split()[0]]
                self.probability[bigram] = count / float(wn_1_count)

        # Give a seed, water it, turn in to a tree of sentences
        self.bagOfSeeds = {}
        for i in range(len(self.tokens) - 1):
            if not self.tokens[i] in self.bagOfSeeds:
                self.bagOfSeeds[self.tokens[i]] = set()

            self.bagOfSeeds[self.tokens[i]].add(self.tokens[i + 1])

    def __generate_bigram_counts(self):
        self.bigramCounts = {}
        for i in range(len(self.tokens) - 1):
            bigram = self.tokens[i] + " " + self.tokens[i + 1]

            if bigram in self.bigramCounts:
                self.bigramCounts[bigram] += 1
            else:
                self.bigramCounts[bigram] = 1
        return self.bigramCounts

    def __generate_word_count(self):
        counts = {}
        for token in self.tokens:
            if token in counts:
                counts[token] += 1
            else:
                counts[token] = 1
        return counts

    def __good_turing_discounting(self, counts):
        self.numberOfCounts = {}

        # Get Nc
        for word, count in counts.iteritems():
            if str(count) not in self.numberOfCounts:
                self.numberOfCounts[str(count)] = 0
            self.numberOfCounts[str(count)] += 1

        # Get c*
        smoothedCount = {}
        for word, count in counts.iteritems():
            if count < 5:
                smoothedCount[word] = (
                    count + 1) * self.numberOfCounts[str(count + 1)] / float(self.numberOfCounts[str(count)])

            else:
                smoothedCount[word] = counts[word]

        return smoothedCount
