# -*- coding: utf-8 -*-
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# In this part of the project, I am going to be exporting the .osm file to .json

#Import statements
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

# RE to deal with problem characters
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# RE to deal with street name replacements
startswithaddr = re.compile(r'\Aaddr:')
afteraddr = re.compile(r':.+$')
afteraddr2 = re.compile(r'[a-zA-Z+$]')
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_name_re = re.compile(r'.*?(?=[\wäöüß]+$)', re.IGNORECASE)

# The created array stores information about the creation of the way or node.
CREATED = ["version", "changeset", "timestamp", "user", "uid"]
pos = []

# This is used to replace bad street types
mapping = {"Ave": "Avenue",
           "Pl": "Place",
           "St": "Street",
           "St.": "Street",
           "Steet": "Street",
           "ave": "Avenue",
           "Ct": "Court",
           "Dr": "Drive",
           "Blvd": "Boulevard",
           "ST": "Street",
           "Dri": "Drive"
           }

# Checks to see if the element is a street name
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


# This function will update the street name if necessary to the correct one.
def update_name(name, mapping):
    firstname = ""
    m = street_type_re.search(name)
    o = street_name_re.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping.keys():
            name = mapping[street_type]
            if o:
                firstname = o.group()

    return firstname + " " + name


# This processes the file
def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


# This function shapes each element in the .json file
def shape_element(element):
    node = {}

    if element.tag == "node" or element.tag == "way":
        node['type'] = element.tag
        if 'lon' in element.attrib:
            # treat geo attribs values
            node.update({'pos': [element.attrib['lon'], element.attrib['lat']]})

        for attr in element.attrib:

            if attr in ['lat', 'lon']:
                pass  # already treated
            elif attr in CREATED:
                node.setdefault('created', {})[attr] = element.attrib[attr]
            else:
                node[attr] = element.attrib[attr]

        for tag in element.iter("tag"):
            # treat child tags
            if is_street_name(tag):
                input1 = update_name(tag.attrib['v'], mapping)
                node.update({"Address": input1})
            else:
                node.update({tag.attrib['k']: tag.attrib['v']})

        for tag in element.iter("nd"):
            # treat nd childs
            node.update({'node_ref': [tag.attrib['ref']]})

        print(node)
        # here you can print your element to check if it is ok
        return node
    else:
        return None



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    process_map('TriCities2.xml')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
