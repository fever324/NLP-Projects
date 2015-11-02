NER_dict = {}

with open('train2.txt', 'r') as f:
    line_no = 0

    for line in f:
        if line_no == 0:
            word_tokens = line.split()
        if line_no == 2:
            labels = line.split()
            cur_B = ''
            target = ()

            for i in range(len(labels)):
                if labels[i][0] == 'B':
                    if len(target) != 0:
                        NER_dict[cur_B].add(target)
                        target = ()
                    cur_B = word_tokens[i]
                    if cur_B not in NER_dict:
                        NER_dict[cur_B] = set()
                if labels[i][0] == 'I':
                    target += (word_tokens[i],)
                if labels[i] == 'O':
                    if len(target) != 0:
                        NER_dict[cur_B].add(target)
                        target = ()
                        cur_B = ''

        line_no = (line_no + 1) % 3

print NER_dict

#  with open ('test.txt', 'r') as f:
    #  line_no = 0

    #  for lin in f:
        #  if line_no == 0:
