import xml.etree.ElementTree as ET

tree = ET.parse('processed_training2.xml')
root = tree.getroot()

dic = {}

for lexelt in root:
    dic[lexelt.attrib['item']] = 'a'

for key in dic:
    print key
