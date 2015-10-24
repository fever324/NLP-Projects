import xml.etree.ElementTree as ET
import math
import operator
import utils

"""
featureProbabilityDictionary
{
    lexelt-item:
    {
        sense_id:
        {
            feature: probability
        }
    }
}

priorProbabilityDictionary
{
    lexelt-item:
    {
        sense_id: probability
    }
}
"""


def word_sense_disambiguation(featureProbabilityDictionary, priorProbabilityDictionary, context, instanceString):
    sense_ids = featureProbabilityDictionary[instanceString]
    sense_id_scores = {}
    surround_words = context.text.strip().split()[-10:]
    headNumber = 0
    while(len(surround_words) < 20):
        numberToGrab = 20 - len(surround_words)
        surround_words += context[headNumber].tail.strip().split()[
            :numberToGrab]
        headNumber += 1

    for sense_id, featureProbility in sense_ids.iteritems():
        sense_id_scores[sense_id] = priorProbabilityDictionary[
            instanceString][sense_id]

        for word in surround_words:
            if word in featureProbility:
                sense_id_scores[sense_id] *= featureProbility[word]

    # return the sense_id with max score
    return max(sense_id_scores.iteritems(), key=operator.itemgetter(1))[0]


def parse_trainig_data(featureProbabilityDictionary, priorProbabilityDictionary):
    tree = ET.parse('test-data.data')
    root = tree.getroot()
    lexelts = root.findall("./lexelt")
    results = {}
    for lexelt in lexelts:
        instanceString = lexelt.attrib['item']
        for instance in lexelt:
            context = instance[0]
            results[instance.attrib['id']] = word_sense_disambiguation(
                featureProbabilityDictionary, priorProbabilityDictionary, context, instanceString)
    f = open('test_result.txt', 'w')
    for result, sense_id in results.iteritems():
        f.write(result + "," + sense_id)
    f.close()
