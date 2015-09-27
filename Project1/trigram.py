class Trigram(object):

    def __init__(self, tokens, usingGoodTuring=False):
        self.tokens = tokens
        self.usingGoodTuring = usingGoodTuring
        self.probability = {}
        self.__generate_trigram_model(usingGoodTuring)

    def get_probability(self, string):

        numberOfAllTrigrams = len(
            self.bagOfSeeds) ** 3
        if string in self.probability:
            return self.probability[string]
        else:
            # This part handles unknown words
            if not self.usingGoodTuring:
                return 0
            else:
                N1 = self.numberOfCounts["1"]

                if 'numberOfSeenTrigram' not in locals():
                    self.numberOfSeenTrigram = len(self.trigramsCounts)
                N0 = numberOfAllTrigrams - \
                    self.numberOfSeenTrigram
                leadingWord = string.split()[0] + " " + string.split()[1]
                if leadingWord not in self.wordCount:
                    leadingWord = "<UNK> <UNK>"
                return N1 / float(N0) / float(self.wordCount[leadingWord])

    def __generate_trigram_model(self, usingGoodTuring=False):
        self.wordCount = self.__generate_word_count()
        self.trigramsCounts = self.__generate_trigram_counts()

        # Smooth the counting
        if usingGoodTuring:
            self.trigramsCounts = self.__good_turing_discounting(
                self.trigramsCounts)

        # Probability of trigrams
        self.probability = {}
        for trigram, count in self.trigramsCounts.iteritems():
            leadingWord = trigram.split()[0] + " " + trigram.split()[1]
            if leadingWord != "<UNK> <UNK>":
                wn_1_count = self.wordCount[
                    trigram.split()[0] + " " + trigram.split()[1]]
                self.probability[trigram] = count / float(wn_1_count)

        # Give a seed, water it, turn in to a tree of sentences
        self.bagOfSeeds = {}
        for i in range(len(self.tokens) - 2):
            leadingTwoWord = self.tokens[i] + " " + self.tokens[i + 1]
            if leadingTwoWord not in self.bagOfSeeds:
                self.bagOfSeeds[leadingTwoWord] = set()

            self.bagOfSeeds[leadingTwoWord].add(self.tokens[i + 2])

    def __generate_trigram_counts(self):
        self.trigramsCounts = {}
        for i in range(len(self.tokens) - 2):
            trigram = self.tokens[i] + " " + \
                self.tokens[i + 1] + " " + self.tokens[i + 2]

            if trigram in self.trigramsCounts:
                self.trigramsCounts[trigram] += 1
            else:
                self.trigramsCounts[trigram] = 1
        return self.trigramsCounts

    def __generate_word_count(self):
        counts = {}
        for i in range(len(self.tokens) - 1):
            leadingTwoWord = self.tokens[i] + " " + self.tokens[i + 1]

            if leadingTwoWord in counts:
                counts[leadingTwoWord] += 1
            else:
                counts[leadingTwoWord] = 1
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
