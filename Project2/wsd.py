import xml.etree.ElementTree as ET
import math
import operator
import utils


def word_sense_disambiguation(dic, context, instance):
    sense_ids = dic[instance]
    sense_id_scores = {}
    surround_words = context.text.strip().split()[-10:]
    headNumber = 0
    while(len(surround_words) < 20):
        numberToGrab = 20 - len(surround_words)
        surround_words += context[headNumber].tail.strip().split()[
            :numberToGrab]
        headNumber += 1

    # Turn array to dictionary with count
    surround_words_dic = {}
    for word in surround_words:
        if word not in surround_words_dic:
            surround_words_dic[word] = 0
        surround_words_dic += 1

    for sense_id, features in sense_ids.iteritems():
        sense_id_scores[sense_id] = 0
        for feature in features:
            if feature in surround_words_dic:
                # score is sum of exp(probability)
                sense_id_scores[sense_id] += math.exp(feature[1]) * surround_words_dic[feature[0]]

    # return the sense_id with max score
    return max(sense_id_scores.iteritems(), key=operator.itemgetter(1))[0]


# def parse_trainig_data(dic):
#     tree = ET.parse('test-data.data')
#     root = tree.getroot()
#     contexts = root.findall("./lexelt/instance/")
