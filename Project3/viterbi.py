import hmm
import baseline
import os

Solution = {}


def decoding(wordTokens):
    wordLen = len(wordTokens)
    states = []
    for key in hmm.uniCount:
        states.append(key)
    states.remove('<s>')
    states.remove('<end>')
    stateNum = len(states)
    print states

    viterbi = [[0 for x in range(wordLen)] for x in range(stateNum + 1)]
    backpointer = [[0 for x in range(wordLen)] for x in range(stateNum + 1)]

    # Initialization step
    print 'Initialization!!!!!!!!'
    for s in range(stateNum):
        emissionEntry = states[s] + ' ' + wordTokens[0]
        if emissionEntry not in hmm.emissionP:
            emissionEntry = states[s] + ' ' + hmm.categorize(wordTokens[0])
            print emissionEntry

        if emissionEntry not in hmm.emissionP:
            viterbi[s][0] = 0
        else:
            transEntry = '<s> ' + states[s]
            if transEntry not in hmm.biTransP:
                viterbi[s][0] = 0
            else:
                viterbi[s][0] = hmm.biTransP['<s> ' + states[s]] * hmm.emissionP[emissionEntry]
        backpointer[s][0] = 0
        #  print s, viterbi[s][0]

    # Recursion step
    print 'Recursion!!!!!!!!'
    for t in range(1, wordLen):  # 0 column has been taken care of in initialization
        for s in range(stateNum):
            maxProb = 0
            maxProbIndex = 0
            for u in range(stateNum):
                transEntry = states[u] + ' ' + states[s]
                # Smooth prob here!!!!
                prob = 0
                if transEntry in hmm.biTransP:
                    prob = viterbi[u][t - 1] * hmm.biTransP[transEntry]
                if prob > maxProb:
                    maxProb = prob
                    maxProbIndex = u
            #  print s, t, maxProb, maxProbIndex

            emissionEntry = states[s] + ' ' + wordTokens[t]
            if emissionEntry not in hmm.emissionP:
                emissionEntry = states[s] + ' ' + hmm.categorize(wordTokens[t])

            if emissionEntry not in hmm.emissionP:
                # Smoothing here!!!!
                viterbi[s][t] = 0
            else:
                viterbi[s][t] = maxProb * hmm.emissionP[emissionEntry]

            backpointer[s][t] = maxProbIndex

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
    #  print 'Temination'
    #  print maxTProb
    #  print maxTProbIndex
    #  print states

    # Backtrace step
    index = backpointer[stateNum][wordLen - 1]
    # for i in range(stateNum + 2):
    #     for j in range(wordLen):
    #         print backpointer[i][j],
    #     print ''

    result = []
    for t in range(wordLen - 1, -1, -1):
        #  print states[index] + " " + wordTokens[t]
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

    with open('test.txt', 'r') as f:
        line_no = 0
        count = 0

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

                count += 1
                if count == 1:
                    break

            line_no = (line_no + 1) % 3


if __name__ == "__main__":
    hmm.smoothing()
    hmm.hmm()
    main()

    baseline.printSolution(Solution)
