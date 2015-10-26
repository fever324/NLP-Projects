import xml.etree.ElementTree as ET
from generateWordMap import get_word_definition_overlap_count
import json
#  import pdb
#  pdb.set_trace()

# Feature range around target word
select_range = 6

# The number of features for a lexelt
feature_num = 5

# The training number for each lexelt
training_amount = 20


def naive_bayes_training(root):
    #  Compute P(senseid_i)
    prior_prob = {}

    trained = 0
    for lexelt in root:
        if trained == training_amount:
            break

        for instance in lexelt:
            for answer in instance:
                if answer.tag == 'context':
                    continue

                senseid = answer.attrib['senseid']
                if senseid == 'U':
                    continue

                #  item = lexelt.attrib['item'].strip().split('.')[0]
                item = lexelt.attrib['item']
                if item in prior_prob:
                    lexelt_dict = prior_prob[item]
                    if senseid in lexelt_dict:
                        lexelt_dict[senseid] += 1
                    else:
                        lexelt_dict[senseid] = 1

                else:
                    prior_prob[item] = {senseid: 1}

    senseid_amount = {}

    for lexelt in prior_prob:
        count = 0
        for senseid in prior_prob[lexelt]:
            count += prior_prob[lexelt][senseid]
        for senseid in prior_prob[lexelt]:
            senseid_amount[senseid] = prior_prob[lexelt][senseid]
            prior_prob[lexelt][senseid] /= float(count)

    print "Prior prob done"
    #  print prior_prob

    #  Compute P(feature_i|senseid_i)
    trained = 0
    feature_candidates_dict = {}
    for lexelt in root:
        if trained == training_amount:
            break

        lexelt_item = lexelt.attrib['item']
        #  lexelt_item = lexelt.attrib['item'].strip().split('.')[0]
        if lexelt_item not in feature_candidates_dict:
            feature_candidates_dict[lexelt_item] = {}

        for instance in lexelt:
            if instance[0].attrib['senseid'] == 'U':
                continue

            length = len(instance) - 1
            context = instance[length].text.strip().split()
            feature_candidates = context[-(select_range/2):]

            for head in instance[length]:
                if head.tail is None:
                    continue

                feature_candidates += head.tail.strip().split()
                if len(feature_candidates) > select_range:
                    break

            feature_candidates = feature_candidates[:select_range]

            for answer in instance[:length]:
                senseid = answer.attrib['senseid']
                if senseid == 'U':
                    continue

                for feature in feature_candidates:
                    if feature in feature_candidates_dict[lexelt_item]:
                        if senseid in feature_candidates_dict[lexelt_item][feature]:
                            feature_candidates_dict[lexelt_item][feature][senseid] += 1
                        else:
                            feature_candidates_dict[lexelt_item][feature][senseid] = 1
                    else:
                        feature_candidates_dict[lexelt_item][feature] = {senseid: 1}
        print lexelt_item + ": Feature candidates done"

    print "Feature candidates all done"
    #  print feature_candidates_dict

    feature_dict = {}
    for lexelt_item in feature_candidates_dict:
        feature_dict[lexelt_item] = {}

        for feature in feature_candidates_dict[lexelt_item]:
            feature_dict[lexelt_item][feature] = get_word_definition_overlap_count(feature, lexelt_item.split('.')[0])
            print feature + ' overlap ' + lexelt_item + ': ' + str(feature_dict[lexelt_item][feature])

        sorted_features = sorted(feature_dict[lexelt_item], key=feature_dict[lexelt_item].get, reverse=True)[:feature_num]

        print lexelt_item.split('.')[0] + ' selected features: ' + str(sorted_features)

        feature_dict[lexelt_item] = {}

        for feature in sorted_features:
            senseid_count_dict = feature_candidates_dict[lexelt_item][feature]

            for senseid in senseid_count_dict:
                if senseid not in feature_dict[lexelt_item]:
                    feature_dict[lexelt_item][senseid] = {}
                feature_dict[lexelt_item][senseid][feature] = senseid_count_dict[senseid] / float(senseid_amount[senseid])
                print feature + ' ' + str(senseid) + ' ' + str(senseid_count_dict[senseid]) + ' ' + str(senseid_amount[senseid])

        print lexelt_item + ": prob calc done"

    for lexelt_item in feature_dict:
        all_senseid_count = 0
        for senseid in feature_dict[lexelt_item]:
            all_senseid_count += senseid_amount[senseid]
        feature_dict[lexelt_item]['<unk>'] = 1 / float(all_senseid_count)

    with open('prior_prob.json', 'w') as f:
        f.write(json.dumps(prior_prob))
    with open('feature_dict.json', 'w') as f:
        f.write(json.dumps(feature_dict))

    return (prior_prob, feature_dict)


if __name__ == "__main__":
    tree = ET.parse('processed_training.xml')
    root = tree.getroot()
    naive_bayes_training(root)
