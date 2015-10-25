import xml.etree.ElementTree as ET
import csv


def run():
    tree = ET.parse('processed_training.xml')
    root = tree.getroot()

    prediction = []
    with open('test_result.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            prediction.append(row[1])

    truth = []
    for lexelt in root:
        for instance in lexelt:
            answer = instance[0].attrib['senseid']
            truth.append(answer)

    correct = 0
    for i in range(len(prediction)):
        if prediction[i] == truth[i]:
            correct += 1

    print float(correct) / len(prediction)
