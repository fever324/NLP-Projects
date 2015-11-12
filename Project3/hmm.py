uniCount = {}
biCount = {}
triCount = {}

uniTransP = {}
biTransP = {}
triTransP = {}

emissionCount = {}
emissionP = {}


def updateCountDict(dic, key):
    if key not in dic:
        dic[key] = 1
    else:
        dic[key] += 1


def hmm():
    with open('train.txt', 'r') as f:
        line_no = 0

        for line in f:
            if line_no == 0:
                wordTokens = line.strip().split()

            if line_no == 2:
                labels = line.strip().split()
                labels.insert(0, '<s>')
                labels.append('<end>')
                labelsLen = len(labels)-1

                for index in range(labelsLen):
                    updateCountDict(uniCount, labels[index])
                    updateCountDict(biCount, labels[index] + ' ' + labels[index+1])
                updateCountDict(uniCount, '<end>')

                labels.pop()
                labels.pop(0)

                for index in range(len(labels)):
                    updateCountDict(emissionCount, labels[index] + ' ' + wordTokens[index])

            line_no = (line_no + 1) % 3

    for key in biCount:
        biTransP[key] = biCount[key] / float(uniCount[key.split()[0]])

    for key in emissionCount:
        emissionP[key] = emissionCount[key] / float(uniCount[key.split()[0]])
