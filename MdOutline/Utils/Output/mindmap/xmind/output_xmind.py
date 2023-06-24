# https://blog.csdn.net/lemonbit/article/details/122613185
# pip install xmind

import os
import xmind

from ...html.output_html import markdown2html_body
from MdUtils.File.Mindmap.Xmind import repair_xmind_files


def mk_xmind_node(md_node, xmind_parent_node):
    sub_xmind_node = xmind_parent_node.addSubTopic()
    sub_xmind_node.setTitle(md_node.get_path_title())

    if not md_node.is_inner_text_empty():
        inner_md_code = md_node.inner_text

        inner_html_code = markdown2html_body(inner_md_code)

        sub_xmind_node.setPlainNotes(inner_html_code)

    for i in md_node.sons:
        mk_xmind_node(md_node=i, xmind_parent_node=sub_xmind_node)


def output_xmind(md_node, md_path, xmind_path="", new_file=True):
    md_path = md_path.strip()

    if len(md_path) > 0:
        xmind_path = md_path + ".xmind"
    else:
        xmind_path = "result.xmind"

    if new_file:
        if os.path.exists(xmind_path):
            os.remove(xmind_path)

    w = xmind.load(xmind_path)
    work_sheet = w.getPrimarySheet()
    work_sheet.setTitle(md_node.title)

    xmind_node = work_sheet.getRootTopic()  # 获取此工作表的根主题
    xmind_node.setTitle(md_node.title)  # 设置标题

    for i in md_node.sons:
        mk_xmind_node(md_node=i, xmind_parent_node=xmind_node)

    xmind.save(w, xmind_path)
    repair_xmind_files(xmind_path)
