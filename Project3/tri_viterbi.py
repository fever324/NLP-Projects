import hmm
import baseline
import os

Solution = {}


def firstInitializationHelper(smooth, stateNum, states, viterbi, backpointer, wordTokens):
    smoothLater = True
    # First time -- * * s
    for s in range(stateNum):
        emissionEntry = states[s] + ' ' + wordTokens[0]
        if smooth and emissionEntry not in hmm.emissionP:
            emissionEntry = states[s] + ' ' + hmm.categorize(wordTokens[0])

        if emissionEntry not in hmm.emissionP:
            for u in range(stateNum):
                viterbi[u][s][0] = 0
        else:
            transEntry = '<s> <s> ' + states[s]
            if transEntry not in hmm.triTransP:
                for u in range(stateNum):
                    viterbi[u][s][0] = 0
            else:
                prob = hmm.triTransP[transEntry] * hmm.emissionP[emissionEntry]
                for u in range(stateNum):
                    viterbi[u][s][0] = prob
                smoothLater = False

        for u in range(stateNum):
            backpointer[u][s][0] = -1
            #  print viterbi[u][s][0],
        #  print ''

    return smoothLater


def secondInitializationHelper(smooth, stateNum, states, viterbi, backpointer, wordTokens):
    smoothLater = True
    # Second Time  -- * u s
    for s in range(stateNum):
        emissionEntry = states[s] + ' ' + wordTokens[1]
        if smooth and emissionEntry not in hmm.emissionP:
            emissionEntry = states[s] + ' ' + hmm.categorize(wordTokens[1])

        if emissionEntry not in hmm.emissionP:
            for u in range(stateNum):
                viterbi[u][s][1] = 0
        else:
            for u in range(stateNum):
                transEntry = '<s> ' + states[u] + ' ' + states[s]
                if transEntry not in hmm.triTransP:
                    viterbi[u][s][1] = 0
                else:
                    viterbi[u][s][1] = viterbi[0][u][0] * hmm.triTransP[transEntry] * hmm.emissionP[emissionEntry]
                    smoothLater = False

        for u in range(stateNum):
            backpointer[u][s][1] = -1

    #  print '-------------------'
    #  for u in range(stateNum):
        #  for s in range(stateNum):
            #  print viterbi[u][s][1],
        #  print ''
    #  print '-------------------'

    return smoothLater


def recursionHelper(smooth, stateNum, states, viterbi, backpointer, wordTokens, t):
    smoothLater = True
    # v u s
    for s in range(stateNum):
        emissionEntry = states[s] + ' ' + wordTokens[t]
        if smooth and emissionEntry not in hmm.emissionP:
            emissionEntry = states[s] + ' ' + hmm.categorize(wordTokens[t])

        if emissionEntry not in hmm.emissionP:
            for u in range(stateNum):
                viterbi[u][s][t] = 0
        else:
            for u in range(stateNum):
                maxProb = 0
                maxProbIndex = 0

                for w in range(stateNum):
                    transEntry = states[w] + ' ' + states[u] + ' ' + states[s]
                    if transEntry in hmm.triTransP:
                        prob = viterbi[w][u][t-1] * hmm.triTransP[transEntry]
                        if prob > maxProb:
                            maxProb = prob
                            maxProbIndex = w

                viterbi[u][s][t] = maxProb * hmm.emissionP[emissionEntry]
                backpointer[u][s][t] = maxProbIndex

            smoothLater = False

    #  print '-------------------' + str(t)
    #  for u in range(stateNum):
        #  for s in range(stateNum):
            #  print viterbi[u][s][t],
        #  print ''
    #  print '-------------------' + str(t)

    #  print '-------------------' + str(t)
    #  for u in range(stateNum):
        #  for s in range(stateNum):
            #  print backpointer[u][s][t],
        #  print ''
    #  print '-------------------' + str(t)

    return smoothLater


def decoding(wordTokens):
    wordLen = len(wordTokens)
    states = []
    for key in hmm.uniCount:
        states.append(key)
    states.remove('<s>')
    states.remove('<end>')
    stateNum = len(states)

    viterbi = [[[0 for x in range(wordLen)] for x in range(stateNum)] for x in range(stateNum)]
    backpointer = [[[0 for x in range(wordLen)] for x in range(stateNum)] for x in range(stateNum)]

    # Initialization step
    smooth = firstInitializationHelper(False, stateNum, states, viterbi, backpointer, wordTokens)
    if smooth:
        firstInitializationHelper(True, stateNum, states, viterbi, backpointer, wordTokens)

    smooth = secondInitializationHelper(False, stateNum, states, viterbi, backpointer, wordTokens)
    if smooth:
        secondInitializationHelper(True, stateNum, states, viterbi, backpointer, wordTokens)

    # Recursion step
    for t in range(2, wordLen):  # 0 and1 column has been taken care of in initialization
        smooth = recursionHelper(False, stateNum, states, viterbi, backpointer, wordTokens, t)
        if smooth:
            recursionHelper(True, stateNum, states, viterbi, backpointer, wordTokens, t)

    # Termination step
    maxTProb = 0
    maxTProbIndexS = 0
    maxTProbIndexU = 0
    for s in range(stateNum):
        for u in range(stateNum):
            transEntry = states[u] + ' ' + states[s] + ' <end>'
            TProb = 0
            if transEntry in hmm.triTransP:
                TProb = viterbi[u][s][wordLen - 1] * hmm.triTransP[transEntry]
            if TProb > maxTProb:
                maxTProb = TProb
                maxTProbIndexS = s
                maxTProbIndexU = u

    result = []
    result.append(states[maxTProbIndexU])
    result.append(states[maxTProbIndexS])
    print 'here'
    print maxTProbIndexU, maxTProbIndexS
    #  print states

    # Backtrace step
    for k in range(wordLen-3, -1, -1):
        yk = backpointer[maxTProbIndexU][maxTProbIndexS][k+2]
        result.insert(0, states[yk])

    with open('result.txt', 'a') as f:
        for r in result:
            f.write(r + ' ')
        f.write('\n')

    print result
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
                length = len(wordTokens)
                if length == 1:
                    pred = ['O']
                    with open('result.txt', 'a') as f:
                        f.write('O')
                        f.write('\n')
                else:
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

                #  count += 1
                #  if count == 1:
                    #  break

            line_no = (line_no + 1) % 3


if __name__ == "__main__":
    hmm.smoothing()
    hmm.hmm()
    main()

    baseline.printSolution(Solution)
