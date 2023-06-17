import os

import time


class MarkdownBlock:

    def __init__(self, title="", inner_text="", code="", depth=0, path=""):
        self.title = title
        self.inner_text = inner_text
        self.code = code
        self.depth = depth
        self.path = path
        self.sons = []

    def parse_son(self):
        if len(self.code) == 0:
            return

        lines = self.code.split("\n")
        son_level = self.depth + 1
        son_count = 0
        level_list = parse_title(lines, son_level)

        if len(level_list) == 0 or level_list[0] != 0:
            # 没有任何一个搜索级别的标签（考虑只有子标签）
            # 或者，有，但是在第一个之前还有内容，那肯定是字标签

            title_line = -1
            if len(level_list) == 0:
                search_range = len(lines)
            else:
                search_range = level_list[0]

            for i in range(0, search_range):
                if is_title(lines[i]):
                    title_line = i
                    break

            if title_line >= 0:
                # 找到第一个标题行了
                title = ""
                inner_text = restore_string_by_spilt_lines(lines[0:title_line])
                code = restore_string_by_spilt_lines(lines[title_line:search_range])
                son_count += 1
                new_son = \
                    MarkdownBlock(title, inner_text, code, son_level, self.path + str(son_count))
                self.sons.append(new_son)
                new_son.parse_son()

        for i in range(0, len(level_list)):
            # 1,2
            title = lines[level_list[i]].strip()[son_level + 1:].strip()
            start = level_list[i] + 1
            if i == len(level_list) - 1:
                end = len(lines)
            else:
                end = level_list[i + 1]

            title_line = -1
            for i in range(start, end):
                if is_title(lines[i]):
                    title_line = i
                    break

            if title_line >= 0:
                inner_text = restore_string_by_spilt_lines(lines[start:title_line])
                code = restore_string_by_spilt_lines(lines[title_line:end])
            else:
                inner_text = restore_string_by_spilt_lines(lines[start: end])
                code = ""

            son_count += 1
            new_son = \
                MarkdownBlock(title, inner_text, code, son_level, self.path + str(son_count))
            self.sons.append(new_son)
            new_son.parse_son()

        # code = mkString(lines[end:])

    def is_leaf(self):
        return len(self.sons) == 0

    def get_path_string(self):
        mypath = self.path.strip()
        re = ""
        for i in mypath:
            re += "." + i

        return re[1:]

    def get_struct_str(self):
        return output_struct(self)


def parse_title(lines, depth):
    level_list = []
    if type(lines) == str:
        lines = lines.split('\n')

    for i in range(len(lines)):
        if is_target_level_title(lines[i], depth):
            level_list.append(i)

    return level_list


def is_title(text):
    text1 = text.strip()
    i = 0
    while i < len(text1) and text1[i] == '#':
        i += 1

    if 0 < i < len(text1) and text1[i] == " ":
        return i + 1 < len(text1)
    else:
        return False


def is_target_level_title(text, level=1):
    text1 = text.strip()
    if len(text1) < level + 2:
        return False

    # level级标题会有level个#，以及下一个位置必定为空格！
    ok = True
    for i in range(level):
        if text1[i] != "#":
            ok = False
            break

    if text1[level] != " ":
        ok = False

    return ok


def restore_string_by_spilt_lines(lines):
    if len(lines) == 0:
        return ""

    text = ""
    for line in lines:
        text += "\n" + line
    return text.strip()


def make_root_node(text, title='', parse_son=True):
    lines = text.split("\n")

    inner_text_end = 0
    for i in range(len(lines)):
        if is_title(lines[i]):
            inner_text_end = i
            break

    inner_text = restore_string_by_spilt_lines(lines[:inner_text_end])
    code = restore_string_by_spilt_lines(lines[inner_text_end:])

    root_ele = MarkdownBlock("", inner_text, code, 0, "")

    root_ele.title = title
    if parse_son:
        root_ele.parse_son()

    return root_ele


def output_struct(node):
    if node is None:
        return ""

    spaces = " " * node.depth
    hashtags = "#" * node.depth
    title = node.title
    if len(title) == 0:
        title = "[空]"

    path = node.get_path_string()

    return_str = spaces + hashtags + " " + path + " " + title + "\n"

    # 遍历子节点DFS
    for i in node.son:
        return_str += output_struct(i)

    return return_str
