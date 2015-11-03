
NER_dict = {}
Tag_dict = {}

Solution = {}


def main():
    training()
    testing()
    printSolution()


'''
NER_dict
{
    'TORONTO': set([('TORONTO',)]),
    'SEATTLE': set([('SEATTLE',)]),
    'SAN': set([('SAN', 'FRANCISCO')]),
    'CHICAGO': set([('CHICAGO',)]),
    'New': set([('New', 'York')]),
    'Boston': set([('Boston',)]),
    'National': set([('National', 'League')])
}
'''

'''
Tag_dict
{
    'TORONTO': set(['ORG']),
    'SEATTLE': set(['ORG']),
    'CHICAGO': set(['ORG']),
    'Boston': set(['ORG']),
    'Minnesota': set(['ORG']),
    'DETROIT': set(['ORG']),
    'Philadelphia': set(['ORG']),
    'SAN FRANCISCO': set(['ORG']),
    'New York': set(['ORG'])
}
'''


def training():
    with open('train2.txt', 'r') as f:
        line_no = 0

        for line in f:
            if line_no == 0:
                word_tokens = line.split()
            if line_no == 2:
                labels = line.split()
                cur_B = ''
                cur_Tag = ''
                target = ''

                for i in range(len(labels)):
                    if labels[i][0] == 'B':
                        if len(target) != 0:
                            addToTwoDicts(target, cur_B, cur_Tag)
                        cur_B = word_tokens[i]
                        cur_Tag = labels[i][2:]
                        target = cur_B

                        if cur_B not in NER_dict:
                            NER_dict[cur_B] = set()

                    if labels[i][0] == 'I':
                        target += ' ' + word_tokens[i]

                    if labels[i][0] == 'O':
                        if len(target) != 0:
                            addToTwoDicts(target, cur_B, cur_Tag)
                            target = ()
                            cur_B = ''
                            cur_Tag = ''

                    if i == len(labels) - 1:
                        if cur_B != '':
                            if cur_B not in NER_dict:
                                NER_dict[cur_B] = set()
                            addToTwoDicts(target, cur_B, cur_Tag)
                            target = ()
                            cur_B = ''
                            cur_Tag = ''

            line_no = (line_no + 1) % 3


def testing():
    with open('test2.txt', 'r') as f:
        line_no = 0

        for line in f:
            if line_no == 0:
                word_tokens = line.split()

            if line_no == 2:
                indexes = line.split()
                for i in range(len(word_tokens)):
                    word = word_tokens[i]
                    if word in NER_dict:
                        stringSet = NER_dict[word]
                        # Find longest tuple
                        maxLength = 0
                        for s in stringSet:
                            n = len(s.split())
                            if maxLength < n:
                                maxLength = n

                        for j in range(len(word_tokens), 0, -1):
                            strings = word_tokens[i:i + 1 + j]
                            # Handles not enough remaining words
                            if(len(strings) != j + 1):
                                continue

                            strings = ' '.join(strings).strip()
                            if strings in Tag_dict:
                                tags = Tag_dict[strings]
                                for tag in tags:
                                    if tag not in Solution:
                                        Solution[tag] = []
                                    Solution[tag].append(
                                        indexes[i] + '-' + indexes[i + j])
            line_no = (line_no + 1) % 3


def addToTwoDicts(target, cur_B, cur_Tag):
    NER_dict[cur_B].add(target)
    addToTagDict(target, cur_Tag)


def printSolution():
    with open('solution.txt', 'w') as f:
        f.write('Type,Prediction\n')
        for tag, answers in Solution.iteritems():
            string = tag + ','
            string += ' '.join(answers) + '\n'
            f.write(string)


def addToTagDict(string, tag):
    if string not in Tag_dict:
        Tag_dict[string] = set()
    Tag_dict[string].add(tag)

    #  with open ('test.txt', 'r') as f:
    #  line_no = 0

    #  for lin in f:
    #  if line_no == 0:

if __name__ == "__main__":
    main()
