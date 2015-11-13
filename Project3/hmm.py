import re

uniCount = {}
biCount = {}
triCount = {}

uniTransP = {}
biTransP = {}
triTransP = {}

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

                for index in range(len(labels)-1):
                    updateCountDict(uniCount, labels[index])
                    updateCountDict(biCount, labels[index] + ' ' + labels[index+1])
                updateCountDict(uniCount, '<end>')

                labels.pop()
                labels.pop(0)

                for index in range(len(labels)):
                    word = wordTokens[index]
                    if word not in wordCategory:
                        updateCountDict(emissionCount, labels[index] + ' ' + word)
                    else:
                        updateCountDict(emissionCount, labels[index] + ' ' + wordCategory[word])

            line_no = (line_no + 1) % 3

    for key in biCount:
        biTransP[key] = biCount[key] / float(uniCount[key.split()[0]])

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

    with open('train.txt', 'r') as f:
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
        if wordCount[word] <= 5:
            wordCategory[word] = categorize(word)


def categorize(word):
    for k, v in rexDict.iteritems():
        if v.match(word) != None:
            return k

    return 'rex_other'

smoothing()
hmm()
print wordCount['-']
