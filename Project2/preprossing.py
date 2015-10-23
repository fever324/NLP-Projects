import xml.etree.ElementTree as ET
import utils

if __name__ == "__main__":
    tree = ET.parse('test-data.data')
    root = tree.getroot()
    contexts = root.findall("./lexelt/instance/context")

    unwantedTags = utils.construct_unwanted_tags()

    for context in contexts:
        preString = context.text
        context.text = utils.remove_unwanted_tags(preString, unwantedTags)
        for head in context:
            head.tail = utils.remove_unwanted_tags(head.tail, unwantedTags)
    tree.write('processed_test.xml')
