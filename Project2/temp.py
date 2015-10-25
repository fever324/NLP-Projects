import xml.etree.ElementTree as ET

tree = ET.parse('processed_training2.xml')
root = tree.getroot()

s = set()
for lexelt in root:
    word = lexelt.attrib['item'].split('.')[1]
    s.add(word)

print s
