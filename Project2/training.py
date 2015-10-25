import xml.etree.ElementTree as ET
from generateWordMap import get_word_definition_overlap_count
#  import pdb
#  pdb.set_trace()

# Feature range around target word
select_range = 6

# The number of features for a lexelt
feature_num = 20


def naive_bayes_training(root):
    #  Compute P(senseid_i)
    prior_prob = {}

    for lexelt in root:
        for instance in lexelt:
            for answer in instance:
                if answer.tag == 'context':
                    continue

                item = lexelt.attrib['item'].strip().split('.')[0]
                if item in prior_prob:
                    senseid = answer.attrib['senseid']
                    if senseid == 'U':
                        continue

                    lexelt_dict = prior_prob[item]
                    if senseid in lexelt_dict:
                        lexelt_dict[senseid] += 1
                    else:
                        lexelt_dict[senseid] = 1

                else:
                    prior_prob[item] = {answer.attrib['senseid']: 1}

    for lexelt in prior_prob:
        count = 0
        for senseid in prior_prob[lexelt]:
            count += prior_prob[lexelt][senseid]
        for senseid in prior_prob[lexelt]:
            prior_prob[lexelt][senseid] /= float(count)

    print "Prior prob done"

    #  Compute P(feature_i|senseid_i)
    feature_candidates_dict = {}
    for lexelt in root:
        lexelt_item = lexelt.attrib['item'].strip().split('.')[0]
        if lexelt_item not in feature_candidates_dict:
            feature_candidates_dict[lexelt_item] = {}

        for instance in lexelt:
            length = len(instance) - 1
            context = instance[length].text.strip().split()
            feature_candidates = context[-(select_range/2):]

            for head in instance[length]:
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
                        for senseid_count in feature_candidates_dict[lexelt_item][feature]:
                            if senseid == senseid_count[0]:
                                senseid_count[1] += 1
                                break
                            feature_candidates_dict[lexelt_item][feature].append([senseid, 1])
                    else:
                        feature_candidates_dict[lexelt_item][feature] = [[senseid, 1]]
        print lexelt_item + ": Feature candidates done"

    print "Feature candidates all done"

    feature_dict = {}
    for lexelt_item in feature_candidates_dict:
        if lexelt_item not in feature_dict:
            feature_dict[lexelt_item] = {}

        for feature in feature_candidates_dict[lexelt_item]:
            feature_dict[lexelt_item][feature] = get_word_definition_overlap_count(feature, lexelt_item)
            print feature + ' overlap ' + lexelt_item + ': ' + str(feature_dict[lexelt_item][feature])

        sorted_features = sorted(feature_dict[lexelt_item], key=feature_dict[lexelt_item].get, reverse=True)[:feature_num]

        print lexelt_item + ' selected features: ' + str(sorted_features)

        feature_dict[lexelt_item] = {}

        for feature in sorted_features:
            senseid_count_list = feature_candidates_dict[lexelt_item][feature]

            for senseid_count in senseid_count_list:
                if not senseid_count[0] in feature_dict[lexelt_item]:
                    feature_dict[lexelt_item][senseid_count[0]] = {}
                feature_dict[lexelt_item][senseid_count[0]][feature] = senseid_count[1] / prior_prob[lexelt_item][senseid_count[0]]

        print lexelt_item + ": prob calc done"

    return feature_dict


if __name__ == "__main__":
    tree = ET.parse('processed_training.xml')
    root = tree.getroot()
    print naive_bayes_training(root)
