import hmm
import baseline
import os

Solution = {}


def initializationHelper(smooth, stateNum, states, viterbi, backpointer, wordTokens):
    smoothLater = True
    for s in range(stateNum):
        emissionEntry = states[s] + ' ' + wordTokens[0]
        if smooth:
            if emissionEntry not in hmm.emissionP:
                emissionEntry = states[s] + ' ' + hmm.categorize(wordTokens[0])

        if emissionEntry not in hmm.emissionP:
            viterbi[s][0] = 0
        else:
            transEntry = '<s> ' + states[s]
            if transEntry not in hmm.biTransP:
                viterbi[s][0] = 0
            else:
                viterbi[s][0] = hmm.biTransP[transEntry] * hmm.emissionP[emissionEntry]
                smoothLater = False
        backpointer[s][0] = 0

    return smoothLater


def recursionHelper(smooth, stateNum, states, viterbi, backpointer, wordTokens, t):
    smoothLater = True
    for s in range(stateNum):
        maxProb = 0
        maxProbIndex = 0
        for u in range(stateNum):
            transEntry = states[u] + ' ' + states[s]
            prob = 0
            if transEntry in hmm.biTransP:
                prob = viterbi[u][t - 1] * hmm.biTransP[transEntry]
            if prob > maxProb:
                maxProb = prob
                maxProbIndex = u

        emissionEntry = states[s] + ' ' + wordTokens[t]
        if smooth:
            if emissionEntry not in hmm.emissionP:
                emissionEntry = states[s] + ' ' + hmm.categorize(wordTokens[t])

        if emissionEntry not in hmm.emissionP:
            viterbi[s][t] = 0
        else:
            viterbi[s][t] = maxProb * hmm.emissionP[emissionEntry]
            smoothLater = False

        backpointer[s][t] = maxProbIndex

    return smoothLater


def decoding(wordTokens):
    wordLen = len(wordTokens)
    states = []
    for key in hmm.uniCount:
        states.append(key)
    states.remove('<s>')
    states.remove('<end>')
    stateNum = len(states)

    viterbi = [[0 for x in range(wordLen)] for x in range(stateNum + 1)]
    backpointer = [[0 for x in range(wordLen)] for x in range(stateNum + 1)]

    # Initialization step
    smooth = initializationHelper(False, stateNum, states, viterbi, backpointer, wordTokens)
    if smooth:
        initializationHelper(True, stateNum, states, viterbi, backpointer, wordTokens)

    # Recursion step
    for t in range(1, wordLen):  # 0 column has been taken care of in initialization
        smooth = recursionHelper(False, stateNum, states, viterbi, backpointer, wordTokens, t)
        if smooth:
            recursionHelper(True, stateNum, states, viterbi, backpointer, wordTokens, t)

    # Termination step
    maxTProb = 0
    maxTProbIndex = 0
    for s in range(stateNum):
        transEntry = states[s] + ' <end>'
        TProb = 0
        if transEntry in hmm.biTransP:
            TProb = viterbi[s][wordLen - 1] * hmm.biTransP[transEntry]
        if TProb > maxTProb:
            maxTProb = TProb
            maxTProbIndex = s
    viterbi[stateNum][wordLen - 1] = maxTProb
    backpointer[stateNum][wordLen - 1] = maxTProbIndex

    # Backtrace step
    index = backpointer[stateNum][wordLen - 1]

    result = []
    for t in range(wordLen - 1, -1, -1):
        result.insert(0, states[index])
        index = backpointer[index][t]

    with open('result.txt', 'a') as f:
        for r in result:
            f.write(r + ' ')
        f.write('\n')

    return result


def addToSolution(tag, begin, end):
    if tag not in Solution:
        Solution[tag] = []
    Solution[tag].append(str(begin) + '-' + str(end))


def main():
    if os.path.isfile('result.txt'):
        os.remove('result.txt')

    with open('test2.txt', 'r') as f:
        line_no = 0

        for line in f:
            if line_no == 0:
                wordTokens = line.strip().split()
                pred = decoding(wordTokens)

            if line_no == 2:
                indexes = line.split()
                begin = -1
                end = -1
                tag = ''
                for i in range(len(indexes)):
                    if pred[i][0] == 'B':
                        if begin != -1:
                            addToSolution(tag, begin, end)
                        begin = indexes[i]
                        tag = pred[i][2:]
                        end = indexes[i]

                    elif pred[i][0] == 'I':
                        end = indexes[i]

                    else:
                        if begin != -1:
                            addToSolution(tag, begin, end)
                        begin = -1
                        end = -1
                        tag = ''

                    if i == len(indexes) - 1:
                        if begin != -1:
                            addToSolution(tag, begin, end)
                            begin = -1
                            end = -1
                            tag = ''

            line_no = (line_no + 1) % 3


if __name__ == "__main__":
    hmm.smoothing()
    hmm.hmm()
    main()

    baseline.printSolution(Solution)
