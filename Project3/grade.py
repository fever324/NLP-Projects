fa = open('result.txt', 'r')
fb = open('validation.txt', 'r')

correct = 0
total = 0

count = 0

for line in fa:
    fb.readline()
    fb.readline()

    pred = line.strip().split()
    act = fb.readline().strip().split()

    print count
    assert len(act) == len(pred)

    for index in range(len(act)):
        if pred[index] == act[index]:
            correct += 1
        total += 1
    count += 1

fa.close()
fb.close()

print correct / float(total)
