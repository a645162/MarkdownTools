# https://blog.csdn.net/lemonbit/article/details/122613185
# pip install xmind

import xmind


def OutPutTitleTodoList(node):
    re = ""
    spaces = "\t" * node.depth
    # jing = "#" * node.depth
    jing = "- [ ]"

    title = node.title
    if len(title) == 0:
        title = "[空]"

    path = node.get_path_string()

    re += spaces + jing + " " + path + " " + title + "\n"

    # 遍历子节点DFS
    for i in node.sons:
        re += OutPutTitleTodoList(i)

    return re


def output_xmind(node, xmind_path):
    pass
