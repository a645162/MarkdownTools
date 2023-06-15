import os

import time

md = """
32
321
## 2a
1212
### 3a
22
    # 1a
    12
    123
    ## 2b
        ### 3c
    ## 2b
        ### 3c

# 1b
### 3a

"""


class MarkdownBlock:

    def __init__(self, title="", inner_text="", code="", depth=0, path=""):
        self.title = title
        self.inner_text = inner_text
        self.code = code
        self.depth = depth
        self.path = path
        self.son = []

    def parse_son(self):
        if len(self.code) == 0:
            return

        lines = self.code.split("\n")
        son_level = self.depth + 1
        son_count = 0
        level_list = parseTitle(lines, son_level)

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
                inner_text = mkString(lines[0:title_line])
                code = mkString(lines[title_line:search_range])
                son_count += 1
                new_son = \
                    MarkdownBlock(title, inner_text, code, son_level, self.path + str(son_count))
                self.son.append(new_son)
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
                inner_text = mkString(lines[start:title_line])
                code = mkString(lines[title_line:end])
            else:
                inner_text = mkString(lines[start: end])
                code = ""

            son_count += 1
            new_son = \
                MarkdownBlock(title, inner_text, code, son_level, self.path + str(son_count))
            self.son.append(new_son)
            new_son.parse_son()

        # code = mkString(lines[end:])

    def is_leaf(self):
        return len(self.son) == 0

    def get_path_string(self):
        mypath = self.path.strip()
        re = ""
        for i in mypath:
            re += "." + i

        return re[1:]


def parseTitle(lines, depth):
    levelList = []
    if type(lines) == str:
        lines = lines.split('\n')

    for i in range(len(lines)):
        if is_target_level_title(lines[i], depth):
            levelList.append(i)

    return levelList


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


def mkString(lines):
    if len(lines) == 0:
        return ""

    text = ""
    for line in lines:
        text += "\n" + line
    return text.strip()


def getRoot(text):
    lines = text.split("\n")

    innerTextEnd = 0
    for i in range(len(lines)):
        if is_title(lines[i]):
            innerTextEnd = i
            break

    InnerText = mkString(lines[:innerTextEnd])
    code = mkString(lines[innerTextEnd:])

    rootEle = MarkdownBlock("", InnerText, code, 0, "")

    return rootEle


def OutPutStruct(node):
    spaces = " " * node.depth
    jing = "#" * node.depth
    title = node.title
    if len(title) == 0:
        title = "[空]"

    path = node.get_path_string()

    print(spaces + jing + " " + path + " " + title)

    # if len(node.inner_text) > 0:
    #     lines = node.inner_text.split("\n")
    #     for i in lines:
    #         print(spaces * 2 + " " + i)
    #     # print(node.inner_text)

    # 遍历子节点DFS
    for i in node.son:
        OutPutStruct(i)


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

    # if len(node.inner_text) > 0:
    #     lines = node.inner_text.split("\n")
    #     for i in lines:
    #         print(spaces * 2 + " " + i)
    #     # print(node.inner_text)

    # 遍历子节点DFS
    for i in node.son:
        re += OutPutTitleTodoList(i)

    return re


path = r'H:\Prj\MarkdownTools\test\树.md'
dir = os.path.dirname(path)
filename = os.path.basename(path)


with open(path, encoding='utf-8') as file_obj:
    contents = file_obj.read()
    md = contents.rstrip()

rootEle = getRoot(md)
rootEle.title = filename
rootEle.parse_son()

todoText = OutPutTitleTodoList(rootEle)
print(todoText)

# todofilename = filename + ".todo.md"
# todoFilePath = dir + "\\" + todofilename




def handleCCode(codeText):
    lines = codeText.split("\n")
    re = ""
    for line in lines:

        if line.strip().find("//") > 0:
            index = line.find("//")
            lline = line[:index].rstrip()

            # 继承缩进
            lline1 = lline.strip()
            spaces = lline[:len(lline) - len(lline1)]

            rline = line[index:].strip()

            re += spaces + rline + "\n"
            # print()
        else:
            lline = line

        re += lline + "\n"

    return re


def findCCode(node):
    structPath = node.get_path_string() + "."
    blocks = node.inner_text.split("```C")

    if len(blocks) >= 1:
        title = node.title.replace("*", "")
        if len(title) == 0:
            title = "[空]"

        count = 0
        for i in blocks:
            blockStr = i
            index = blockStr.rfind("```")
            if index == -1:
                continue
            blockStr = blockStr[:index]

            countStr = ""

            count += 1

            if count > 1:
                countStr = str(count)

            saveDir = dir + "\\Algorithms"
            if not os.path.isdir(saveDir):
                os.makedirs(saveDir)

            filePath = saveDir + "\\" + title + countStr + ".c"
            if not os.path.isfile(filePath):
                f = open(filePath, "w", encoding='utf-8')
                ccode = blockStr.strip()
                ccode = handleCCode(ccode)
                f.write(ccode)
                f.close()
            else:
                pass

    for i in node.son:
        findCCode(i)


findCCode(rootEle)

print()
