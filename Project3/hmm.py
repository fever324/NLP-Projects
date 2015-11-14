import re

uniCount = {}
biCount = {}
biCountForTri = {}
triCount = {}

uniTransP = {}
biTransP = {}
triTransP = {}
biForTriP = {}

emissionCount = {}
emissionP = {}

wordCount = {}
rexDict = {}
wordCategory = {}


def updateCountDict(dic, key):
    if key not in dic:
        dic[key] = 1
    else:
        dic[key] += 1


def hmm():
    with open('train2.txt', 'r') as f:
        line_no = 0

        for line in f:
            if line_no == 0:
                wordTokens = line.strip().split()

            if line_no == 2:
                labels = line.strip().split()
                labels.insert(0, '<s>')
                labels.append('<end>')

                for index in range(len(labels) - 1):
                    updateCountDict(uniCount, labels[index])
                    updateCountDict(biCount, labels[index] + ' ' + labels[index + 1])
                updateCountDict(uniCount, '<end>')

                labels.insert(0, '<s>')
                for index in range(len(labels) - 1):
                    updateCountDict(biCountForTri, labels[index] + ' ' + labels[index + 1])
                for index in range(len(labels) - 2):
                    updateCountDict(triCount, labels[index] + ' ' + labels[index + 1] + ' ' + labels[index + 2])

                labels.pop()
                labels.pop(0)
                labels.pop(0)

                for index in range(len(labels)):
                    word = wordTokens[index]
                    if word not in wordCategory:
                        updateCountDict(emissionCount, labels[index] + ' ' + word)
                    else:
                        updateCountDict(emissionCount, labels[index] + ' ' + wordCategory[word])

            line_no = (line_no + 1) % 3

    #  N = sum(uniCount.values())
    N = sum(wordCount.values())

    for key in uniCount:
        uniTransP[key] = uniCount[key] / float(N)

    for key in biCount:
        biTransP[key] = biCount[key] / float(uniCount[key.split()[0]])

    for key in biCountForTri:
        biForTriP[key] = biCountForTri[key] / float(uniCount[key.split()[0]])

    for key in triCount:
        a = key.split()
        firstTwoWord = a[0] + ' ' + a[1]
        triTransP[key] = triCount[key] / float(biCountForTri[firstTwoWord])

    for key in emissionCount:
        emissionP[key] = emissionCount[key] / float(uniCount[key.split()[0]])


def smoothing():

    rexDict['rex_twoDigitNum'] = re.compile("^\d{2}$")
    rexDict['rex_fourDigitNum'] = re.compile("^\d{4}$")
    rexDict['rex_containsDigitAndAlpha'] = re.compile("^[a-zA-Z]\d*$")
    rexDict['rex_containsDigitAndDash'] = re.compile("^\d*\-$\d")
    rexDict['rex_containsDigitAndSlash'] = re.compile("^\d*/\d*/\d*$")
    rexDict['rex_containsDigitAndComma'] = re.compile("^\d*,\d+\.\d+$")
    rexDict['rex_containsDigitAndPeriod'] = re.compile("^\d*\.\d*$")
    rexDict['rex_othernum'] = re.compile("^(\d|\d{3}|\d{5,})$")
    rexDict['rex_allCaps'] = re.compile("^[A-Z]+$")
    rexDict['rex_capPeriod'] = re.compile("^[A-Z]\.$")
    rexDict['rex_initCap'] = re.compile("^[A-Z][a-z]*$")
    rexDict['rex_lowercase'] = re.compile("^[a-z]+$")

    with open('train2.txt', 'r') as f:
        line_no = 0

        for line in f:
            if line_no == 0:
                words = line.strip().split()
                for word in words:
                    if word not in wordCount:
                        wordCount[word] = 1
                    else:
                        wordCount[word] += 1

            line_no = (line_no + 1) % 3

    for word in wordCount:
        if wordCount[word] <= 1:
            wordCategory[word] = categorize(word)


def categorize(word):
    for k, v in rexDict.iteritems():
        if v.match(word) != None:
            return k

    return 'rex_other'


def deleted_interpolation():
    lambda1 = 0
    lambda2 = 0
    lambda3 = 0

    for trigram in triCount:
        labels = trigram.split()
        assert len(labels) == 3

        temp = biCountForTri[labels[0]+' '+labels[1]] - 1
        case3 = 0
        if temp != 0:
            case3 = (triCount[trigram]-1) / float(temp)

        temp = uniCount[labels[1]] - 1
        case2 = 0
        if temp != 0:
            case2 = (biCountForTri[labels[1]+' '+labels[2]] - 1) / float(temp)

        temp = sum(wordCount.values())-1
        #  temp = sum(uniCount.values())-1
        case1 = 0
        if temp != 0:
            case1 = (uniCount[labels[2]]-1) / float(temp)

        maximum = max([case1, case2, case3])

        if maximum == case3:
            lambda3 += triCount[trigram]
        elif maximum == case2:
            lambda2 += triCount[trigram]
        else:
            lambda1 += triCount[trigram]

    total = lambda1 + lambda2 + lambda3
    lambda1 /= float(total)
    lambda2 /= float(total)
    lambda3 /= float(total)

    for k, v in triTransP.iteritems():
        labels = k.split()
        triTransP[k] = lambda3 * triTransP[k] + lambda2 * biForTriP[labels[1]+' '+labels[2]] + lambda1 * uniTransP[labels[2]]

    return lambda1, lambda2, lambda3
