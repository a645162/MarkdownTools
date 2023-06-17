# !/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import datetime
# from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree

from xml.dom import minidom

from MdUtils.Formater.xml import pretty_xml


def generate_opml_node(md_node, xml_parent_node):
    title = md_node.title
    path = md_node.get_path_string()

    this_xml_node = SubElement(xml_parent_node, 'outline')
    this_xml_node.set('text', path + (" " + title).strip())

    # if len(node.inner_text) > 0:
    #     lines = node.inner_text.split("\n")
    #     for i in lines:
    #         print(spaces * 2 + " " + i)
    #     # print(node.inner_text)

    # 遍历子节点 DFS
    for i in md_node.sons:
        generate_opml_node(i, this_xml_node)


def output_opml(md_node, md_path=''):
    md_path = md_path.strip()

    if len(md_path) == 0:
        save_path = 'result.xml'
    else:
        save_path = md_path + ".opml.xml"

    # md_dir=os.path.dirname(md_path)

    # OPML 根节点
    opml_root = Element('opml')
    opml_root.set('version', '1.0')

    # OPML 的 head
    head = SubElement(opml_root, 'head')

    title = SubElement(head, 'title')

    title.text = md_node.title

    time_str = datetime.datetime.now().strftime("%a %b %Y %H:%M:%S")
    SubElement(head, 'dateCreated').text = time_str
    SubElement(head, 'dateModified').text = time_str

    # OPML 的 body
    body = SubElement(opml_root, 'body')
    generate_opml_node(md_node, body)

    tree = ElementTree(opml_root)

    pretty_xml(opml_root)

    tree.write(save_path, encoding='utf-8', xml_declaration=True, short_empty_elements=True)
