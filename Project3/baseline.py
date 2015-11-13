
NER_dict = {}
Tag_dict = {}

Solution = {}


def main():
    training()
    testing()
    printSolution(Solution)


'''
NER_dict - This dictionary is for speed up looking process
Key - the first word in the Sequence,
Value - a set of string that has key as the first word

{
    'TORONTO': set(['TORONTO']),
    'SEATTLE': set(['SEATTLE']),
    'SAN': set(['SAN FRANCISCO']),
    'CHICAGO': set(['CHICAGO')]),
    'New': set(['New York']),
    'Boston': set([('Boston',)]),
    'National': set([('National League')])
}
'''

'''
Tag_dict - A dictionary that matches string to its name entities
Key - String
Value - A set of tags that the string's name entities may belong to
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


# Generate NER_dict and Tag_dict
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

                    # Edge case for last word
                    if i == len(labels) - 1:
                        if cur_B != '':
                            if cur_B not in NER_dict:
                                NER_dict[cur_B] = set()
                            addToTwoDicts(target, cur_B, cur_Tag)
                            target = ()
                            cur_B = ''
                            cur_Tag = ''

            # Make line number goes between [0, 1, 2]
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
                        # Find longest sequence length
                        maxLength = 0
                        for s in stringSet:
                            n = len(s.split())
                            if maxLength < n:
                                maxLength = n

                        # Look for longest sequence first
                        # This goes from maxLength to 1
                        for j in range(maxLength, -1, -1):
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

            # Make line number goes between [0, 1, 2]
            line_no = (line_no + 1) % 3


# Add named entity to NER_dict and Tag_dict
def addToTwoDicts(target, cur_B, cur_Tag):
    NER_dict[cur_B].add(target)
    if target not in Tag_dict:
        Tag_dict[target] = set()
    Tag_dict[target].add(cur_Tag)


def printSolution(s):
    with open('solution.txt', 'w') as f:
        f.write('Type,Prediction\n')
        for tag, answers in s.iteritems():
            string = tag + ','
            string += ' '.join(answers) + '\n'
            f.write(string)


if __name__ == "__main__":
    main()
