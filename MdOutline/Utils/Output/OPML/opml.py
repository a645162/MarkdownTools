# !/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import datetime
# from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree

from xml.dom import minidom

from ..inner_text import get_inner_text
from MdUtils.Formater.xml import pretty_xml


def generate_opml_xmind_node(md_node, xml_parent_node):
    title = md_node.title.strip()
    path = md_node.get_path_string()

    this_xml_node = SubElement(xml_parent_node, 'outline')

    if len(title) > 0:
        title = " " + title
    this_xml_node.set('text', path + title)

    inner_text = get_inner_text(md_node=md_node, remove_blank_lines=True)
    if len(inner_text.strip()) > 0:
        this_xml_node.set('_note', inner_text)

    # 遍历子节点 DFS
    for i in md_node.sons:
        generate_opml_xmind_node(i, this_xml_node)


def output_opml_xmind(md_node, md_path=''):
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
    generate_opml_xmind_node(md_node, body)

    tree = ElementTree(opml_root)

    pretty_xml(opml_root)

    tree.write(save_path, encoding='utf-8', xml_declaration=True, short_empty_elements=True)
