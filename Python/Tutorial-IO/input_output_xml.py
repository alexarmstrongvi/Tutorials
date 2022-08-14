#!/usr/bin/env python3
################################################################################
# XML
#
# Sources
# - https://docs.python.org/3/library/xml.html
# - https://docs.python.org/3/library/xml.etree.elementtree.html
# - https://www.datacamp.com/community/tutorials/python-xml-elementtree
################################################################################
print(f"\n===== Running {__file__} =====\n")

import xml.etree.ElementTree as ET
#import xml.dom.minidom as minidom

filepath = 'input_output_files/output.xml'

################################################################################
# Terminology
# - Element: root, parent, child, sub-child, ...
#   - Tags: start, end, empty
#   - Attributes and namespaces
#   - Value or subelement
#   - Text and tail

################################################################################
def summarize_element(e):
    if type(e) == str:
        e = ET.fromstring(e)
    print("Tag     :", e.tag)
    print("Keys    :", e.keys())
    print("Attrib  :", e.attrib)
    print("Text    :", e.text.strip() if e.text else "")
    print("nChilds :", len(e))
    print("Tail    :", e.tail.strip() if e.tail else "")
    print()

def elements_equal(e1, e2, strip=False):
    if strip:
        e1.text = e1.text.strip() if e1.text else None
        e1.tail = e1.tail.strip() if e1.tail else None
        e2.text = e2.text.strip() if e2.text else None
        e2.tail = e2.tail.strip() if e2.tail else None
    
    if e1.tag != e2.tag:        return False
    if e1.text != e2.text:      return False
    if e1.tail != e2.tail:      return False
    if e1.attrib != e2.attrib:  return False
    if len(e1) != len(e2):      return False
    return all(elements_equal(c1, c2, strip) for c1, c2 in zip(e1, e2))

################################################################################
# Convert XML string into Element
s = '<tag key="val">text</tag>'
e = ET.fromstring(s)
assert e.tag    == 'tag'
assert e.keys() == ['key']
assert e.attrib == {'key':'val'}
assert len(e)   == 0
assert e.tail   == None
assert e.text   == 'text'

s = '''
<tag key1="val1" key2="val2">
    text
    <child_tag>
        child_text
    </child_tag>
    child_tail
</tag>
'''
root = ET.fromstring(s)
assert root.tag    == 'tag'
assert root.keys() == ['key1','key2']
assert root.attrib == {'key1':'val1','key2':'val2'}
assert len(root)   == 1
assert root.tail   == None
assert root.text.strip() == 'text'

for child in root:
    assert child.tag    == 'child_tag'
    assert child.keys() == []
    assert child.attrib == {}
    assert len(child)   == 0
    assert child.tail.strip() == 'child_tail'
    assert child.text.strip() == 'child_text'

assert root[0].tag == 'child_tag'

#ET.fromstringlist
#ET.XML
#ET.XMLID

################################################################################
# Create Element
root2 = ET.Element('tag', {'key1':'val1'}, key2='val2')
root2.text = 'text'
child = ET.SubElement(root2, 'child_tag')
child.text = 'child_text'
child.tail = 'child_tail'

assert elements_equal(root, root2, strip=True)

################################################################################
# Write Element to XML file
etree = ET.ElementTree(root)
etree.write(filepath)

#with open(filepath, 'w') as f:
#    byte_str = ET.tostring(root2)
#    s = byte_str.decode('utf8')
#    f.write(s)

#ET.tostringlist

################################################################################
# Import XML file into ElementTree
tree = ET.parse(filepath)
root = tree.getroot()
assert elements_equal(root2, root)

################################################################################
# Explore element attributes
# root[0]
# get()
# items()
# keys()

# Modify attributes
# set

################################################################################
# Explore children
# find
# findall
# findtext
# iter
# iterfind
# itertext

# Modify children
# append
# extend
# insert
# remove
# clear

################################################################################
# XPath

################################################################################
# Namespaces
#ET.registoer_namespace
#ET.QName

################################################################################
# Read data streaming in incrementally
#XMLPullParser
#ET.iterparse

################################################################################
# Comments, processing instructions, and document type declarations
#ET.Comment
#ET.ProcessingInstruction

################################################################################
# XInclude

################################################################################
# Canonicalization
#ET.canonicalize

################################################################################
# Other
################################################################################
#ET.dump
#ET.indent
#ET.iselement
#ET.TreeBuilder
#ET.XMLParser
