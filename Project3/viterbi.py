import hmm


def decoding(wordTokens):
    wordLen = len(wordTokens)
    states = []
    for key in hmm.uniCount:
        states.append(key)
    states.remove('<s>')
    states.remove('<end>')
    stateNum = len(states)

    viterbi = [[0 for x in range(wordLen)] for x in range(stateNum+2)]
    backpointer = [[0 for x in range(wordLen)] for x in range(stateNum+2)]

    # Initialization step
    for s in range(1, stateNum+1):
        emissionEntry = states[s-1] + ' ' + wordTokens[0]
        if emissionEntry not in hmm.emissionP:
            viterbi[s][0] = 0
        else:
            viterbi[s][0] = hmm.biTransP['<s> '+states[s-1]] * hmm.emissionP[emissionEntry]
        backpointer[s][0] = 0

    # Recursion step
    for t in range(1, wordLen):
        for s in range(1, stateNum+1):
            maxProb = 0
            maxProbIndex = 0
            for u in range(1, stateNum+1):
                transEntry = states[u-1] + ' ' + states[s-1]
                if transEntry not in hmm.biTransP:
                    prob = 0
                else:
                    prob = viterbi[u][t-1] * hmm.biTransP[transEntry]
                if prob > maxProb:
                    maxProb = prob
                    maxProbIndex = u
            emissionEntry = states[s-1] + ' ' + wordTokens[0]
            if emissionEntry not in hmm.emissionP:
                viterbi[s][t] = 0
            else:
                viterbi[s][t] = maxProb * hmm.emissionP[emissionEntry]
            backpointer[s][t] = maxProbIndex

    # Termination step
    maxTProb = 0
    maxTProbIndex = 0
    for s in range(1, stateNum+1):
        transEntry = states[s-1] + ' <end>'
        if transEntry not in hmm.biTransP:
            TProb = 0
        else:
            TProb = viterbi[s][wordLen-1] * hmm.biTransP[transEntry]
        if TProb > maxTProb:
            maxTProb = TProb
            maxTProbIndex = s
    viterbi[stateNum+1][wordLen-1] = maxTProb
    backpointer[stateNum+1][wordLen-1] = maxTProbIndex

    # Backtrace step
    index = backpointer[stateNum+1][wordLen-1]
    for i in range(stateNum+2):
        for j in range(wordLen):
            print backpointer[i][j],
        print ''

    #  for i in range(wordLen-2, -1, -1):
        #  print states[index-1]
        #  index = backpointer[index][i]


if __name__ == "__main__":
    hmm.hmm()
    with open('validation.txt', 'r') as f:
        wordTokens = f.readline().strip().split()
        decoding(wordTokens)
