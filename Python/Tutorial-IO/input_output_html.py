#!/usr/bin/env python3
################################################################################
# HTML
#
# Sources
# - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#     - https://realpython.com/beautiful-soup-web-scraper-python/
# - https://docs.python.org/3/library/html.parser.html
# - https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-read-html
################################################################################
print(f"\n===== Running {__file__} =====\n")
from bs4 import BeautifulSoup, element
import types

#filepath = 'input_output_files/test_input.html'

################################################################################
# Terminology
# - Element: root, parent, child, sub-child, ...
#   - Tags: start, end, empty
#   - Attributes and namespaces
#   - Value or subelement
#   - Text and tail

################################################################################
def print_dir(obj):
    print("Object:", obj)
    print("Object Type:", type(obj))
    print("Attributes:")
    print('\t'+"\n\t".join([x for x in dir(obj) if not x.startswith('_')]))

################################################################################
# Parsing HTML string or file object
#with open(filepath) as f:
#    #soup = BeautifulSoup(f,'html.parser')
#    html_str = f.read()
#soup = BeautifulSoup(html_str,'html.parser')
#print(soup.prettify())

example_html = '''
    <tag1 attr1="val1" attr2="val2">Text</tag1>
    
    <tag2 attr="val1 val2">Text</tag2>
    <tag3 class="body strikeout">Text</tag3>
    
    <tag4><!--Text--></tag4>
    <style>Text</style>
    <script>Text</script>
    <template>Text</template>
    
    <a>Link1</a>
    <a>Link2</a>
    
    <tag5>
        <tag5a></tag5a>
        <tag5b>
            <tag5b1></tag5b1>
        </tag5b>
        <tag5c></tag5c>
    </tag5>
'''
soup = BeautifulSoup(example_html, 'html.parser')
assert type(soup) == BeautifulSoup
assert soup.name == '[document]'
#print_dir(soup)

########################################
# Navigating elements
tag = soup.tag1
#print_dir(tag)
assert type(tag)  == element.Tag
assert str(tag)   == '<tag1 attr1="val1" attr2="val2">Text</tag1>'
assert tag.name   == 'tag1' and type(tag.name) == str
assert tag.string == 'Text' and type(tag.string) == element.NavigableString
# tag.text
#print_dir(tag.string)
assert tag.attrs == {'attr1':'val1','attr2':'val2'}
assert list(tag.attrs.keys()) == ['attr1','attr2']
assert tag['attr1'] == tag.get('attr1') == tag.attrs['attr1'] == 'val1'

# Multi-valued attributes
assert soup.tag2['attr'] == 'val1 val2'
assert soup.tag2.get_attribute_list('attr') == ['val1 val2']
assert soup.tag3['class'] == ['body', 'strikeout'] # recognized multi-valued attrs get split

# Subclasses of NavigableString
comment  = soup.tag4.string
style    = soup.style.string
script   = soup.script.string
template = soup.template.string
assert type(comment)  == element.Comment
assert type(style)    == element.Stylesheet
assert type(script)   == element.Script
assert type(template) == element.TemplateString

# Duplicate tags
assert soup.a.string == 'Link1' # grabs first occurance
assert [x.string for x in soup.find_all('a')] == ['Link1','Link2']

# Sub elements
assert soup.tag5.tag5b.tag5b1.name == 'tag5b1'
assert type(soup.contents) == list
assert type(soup.children) != list # == list_iterator
assert len(soup.contents) == len(list(soup.children))
assert type(soup.descendants) == types.GeneratorType
assert [str(x) for x in soup.tag5.tag5b.contents] == ['\n', '<tag5b1></tag5b1>', '\n']
assert [x.name for x in soup.tag5.descendants if x != '\n'] == ['tag5a','tag5b','tag5b1','tag5c']

# Accessing element strings
# .string, .strings, and .stripped_strings, 
# .string vs .text
# get_text()

# Parent elements
# .parent(s)

# Sibling elements
# .next_sibling(s), .previous_sibling(s)

# Parsing steps as elements
# .next_element(s), .previous_element(s)

# Searching
# find, find_all, 
# soup.find_all('tag')
# soup.find_all(name='tag')
# soup.find_all(attrs={'class' : 'my_class'})
# soup.find_all(class_ = 'my_class')

# find_next/previous, find_all_next/previous

# find_parent, find_parents

# find_next/previous_siblings

# Combining searches

# Filters: string, regex, list, custom function
# Filter on tag, attributes, strings

# CSS selector and SoupSieve (learn the syntax)

########################################
# Modifying elements
# tag['attr'] = 1
# tag['new_attr'] = 2
# del tag['new_attr']
# tag.string = "New Text"

# append(), extend(), insert()

# soup.new_tag()

# clear(), extract(), decompose(), unwrap()

# replace_with()

# wrap()

# smooth()

########################################
# Printing HTML
# prettify() vs. encode()

# Formatting prettify

########################################
# Alternative Parsers and Encodings

########################################
# Parser Customization




