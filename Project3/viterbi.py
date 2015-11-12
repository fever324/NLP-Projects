import hmm


def decoding(wordTokens):
    wordLen = len(wordTokens)
    states = []
    for key in hmm.uniCount:
        states.append(key)
    states.remove('<s>')
    states.remove('<end>')
    stateNum = len(states)

    viterbi = [[0 for x in range(wordLen)] for x in range(stateNum + 2)]
    backpointer = [[0 for x in range(wordLen)] for x in range(stateNum + 2)]

    # Initialization step
    for s in range(stateNum):
        emissionEntry = states[s] + ' ' + wordTokens[0]
        if emissionEntry not in hmm.emissionP:
            viterbi[s][0] = 0
        else:
            viterbi[s][0] = hmm.biTransP['<s> ' + states[s]] * \
                hmm.emissionP[emissionEntry]
        backpointer[s][0] = 0

    # Recursion step
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

            emissionEntry = states[s] + ' ' + wordTokens[t]
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
    viterbi[stateNum + 1][wordLen - 1] = maxTProb
    backpointer[stateNum + 1][wordLen - 1] = maxTProbIndex

    # Backtrace step
    index = backpointer[stateNum + 1][wordLen - 1]
    # for i in range(stateNum + 2):
    #     for j in range(wordLen):
    #         print backpointer[i][j],
    #     print ''

    for t in range(wordLen - 1, -1, -1):
        print states[index - 1] + " " + wordTokens[t]
        index = backpointer[index][t]


if __name__ == "__main__":
    hmm.hmm()
    with open('validation.txt', 'r') as f:
        wordTokens = f.readline().strip().split()
        decoding(wordTokens)
