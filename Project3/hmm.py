uniCount = {}
biCount = {}
triCount = {}

uniTransP = {}
biTransP = {}
triTransP = {}

emissionCount = {}
emissionP = {}


def updateDict(dic, key):
    if key not in dic:
        dic[key] = 1
    else:
        dic[key] += 1


with open('train.txt', 'r') as f:
    line_no = 0

    for line in f:
        if line_no == 0:
            wordTokens = line.strip().split()

        if line_no == 2:
            labels = line.strip().split()
            labelsLen = len(labels)

            if labelsLen == 1:
                updateDict(uniCount, labels[0])
            elif labelsLen != 0:
                for index in range(labelsLen - 1):
                    updateDict(uniCount, labels[index])
                    updateDict(biCount, labels[index] + ' ' + labels[index+1])
                updateDict(uniCount, labels[-1])

            for index in range(labelsLen):
                updateDict(emissionCount, labels[index] + ' ' + wordTokens[index])

        line_no = (line_no + 1) % 3

for key in biCount:
    biTransP[key] = biCount[key] / float(uniCount[key.split()[0]])

for key in emissionCount:
    emissionP[key] = emissionCount[key] / float(uniCount[key.split()[0]])

print biTransP
print emissionP