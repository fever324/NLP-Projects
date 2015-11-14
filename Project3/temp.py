fa = open('result.txt', 'r')
fb = open('test2.txt', 'r')

count = 0

for line in fa:
    pred = line.strip().split()
    act = fb.readline().strip().split()

    print count
    assert len(act) == len(pred)

    count += 1

    fb.readline()
    fb.readline()

fa.close()
fb.close()
