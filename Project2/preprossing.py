import xml.etree.ElementTree as ET
import utils

unwantedTags = utils.construct_unwanted_tags()


def main():
    tree = ET.parse('test-data.data')
    root = tree.getroot()
    contexts = root.findall("./lexelt/instance/context")

    for context in contexts:
        context.text = utils.process_string(context.text, unwantedTags)
        for head in context:
            head.tail = utils.process_string(head.tail, unwantedTags)
    tree.write('processed_test.xml')


if __name__ == "__main__":
    main()
