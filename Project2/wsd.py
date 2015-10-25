import xml.etree.ElementTree as ET
import math
import operator
import utils
import training
import csv
import json
import accuracy

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

    for head in context:
        surround_words += head.tail.strip().split()
        if len(surround_words) > 20:
            break
    surround_words = surround_words[:20]

    for sense_id, featureProbility in sense_ids.iteritems():
        sense_id_scores[sense_id] = priorProbabilityDictionary[
            instanceString][sense_id]

        for word in surround_words:
            if word in featureProbility:
                sense_id_scores[sense_id] *= featureProbility[word]

    # return the sense_id with max score
    return max(sense_id_scores.iteritems(), key=operator.itemgetter(1))[0]


def parse_trainig_data(featureProbabilityDictionary, priorProbabilityDictionary):
    tree = ET.parse('processed_training2.xml')
    root = tree.getroot()
    lexelts = root.findall("./lexelt")
    results = {}
    for lexelt in lexelts:
        instanceString = lexelt.attrib['item']
        for instance in lexelt:
            #  context = instance[0]
            context = instance[len(instance)-1]
            results[instance.attrib['id']] = word_sense_disambiguation(
                featureProbabilityDictionary, priorProbabilityDictionary, context, instanceString)

    with open('test_result.csv', 'w') as csvfile:
        f = csv.writer(csvfile)
        for result, sense_id in results.items():
            f.writerow([result, sense_id])


if __name__ == "__main__":

    with open('prior_prob.json') as f:
        string = "".join(f.readlines())
        prior_prob = json.loads(string)
    with open('feature_dict.json') as f:
        string = "".join(f.readlines())
        feature_dict = json.loads(string)

    #  prior_prob, feature_dict = training.naive_bayes_training(root)

    parse_trainig_data(feature_dict, prior_prob)
    accuracy.run()
