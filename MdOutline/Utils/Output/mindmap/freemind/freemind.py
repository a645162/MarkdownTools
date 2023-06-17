import time
import uuid

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree

from MdUtils.Formater.xml import pretty_xml


def get_freemind_time_now_str():
    return get_freemind_time_str(time.time())


def get_freemind_time_str(target_time):
    return str(target_time).replace('.', '')[:13]


def generate_freemind_node(md_node, xml_parent_node, time_str):
    title = md_node.title.strip()
    path = md_node.get_path_string()

    this_xml_node = SubElement(xml_parent_node, 'node')

    this_xml_node.set('CREATED', time_str)

    this_xml_node.set('ID', str(uuid.uuid1()))

    this_xml_node.set('MODIFIED', time_str)

    if len(title) > 0:
        title = " " + title
    this_xml_node.set('TEXT', path + title)

    # inner_text = get_inner_text(md_node=md_node, remove_blank_lines=True)
    # if len(inner_text.strip()) > 0:
    #     this_xml_node.set('_note', inner_text)

    # 遍历子节点 DFS
    for i in md_node.sons:
        generate_freemind_node(i, this_xml_node, time_str)


def output_freemind(md_node, md_path=''):
    md_path = md_path.strip()

    if len(md_path) == 0:
        save_path = 'result.mm'
    else:
        save_path = md_path + ".mm"

    # md_dir=os.path.dirname(md_path)

    # OPML 根节点
    opml_root = Element('map')
    opml_root.set('version', '1.0.1')

    time_str = get_freemind_time_now_str()
    generate_freemind_node(md_node, opml_root, time_str)

    tree = ElementTree(opml_root)

    pretty_xml(opml_root)

    tree.write(save_path, encoding='utf-8', xml_declaration=True, short_empty_elements=True)
