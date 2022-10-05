import re
import os

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


class MarkdownBlock():

    def __init__(self, title="", inner_text="", code="", depth=0, path=""):
        self.title = title
        self.inner_text = inner_text
        self.code = code
        self.depth = depth
        self.path = path
        self.son = []

    def parseSon(self):
        if len(self.code) == 0:
            return

        lines = self.code.split("\n")
        sonLevel = self.depth + 1
        sonCount = 0;
        levelList = parseTitle(lines, sonLevel)

        if len(levelList) == 0 or levelList[0] != 0:
            # 没有任何一个搜索级别的标签（考虑只有子标签）
            # 或者，有，但是在第一个之前还有内容，那肯定是字标签

            titleLine = -1
            if len(levelList) == 0:
                searchRange = len(lines)
            else:
                searchRange = levelList[0]

            for i in range(0, searchRange):
                if isTitle(lines[i]):
                    titleLine = i
                    break

            if titleLine >= 0:
                # 找到第一个标题行了
                title = ""
                InnerText = mkString(lines[0:titleLine])
                code = mkString(lines[titleLine:searchRange])
                sonCount += 1
                new_son = \
                    MarkdownBlock(title, InnerText, code, sonLevel, self.path + str(sonCount))
                self.son.append(new_son)
                new_son.parseSon()

        for i in range(0, len(levelList)):
            # 1,2
            title = lines[levelList[i]].strip()[sonLevel + 1:].strip()
            start = levelList[i] + 1
            if i == len(levelList) - 1:
                end = len(lines)
            else:
                end = levelList[i + 1]

            titleLine = -1
            for i in range(start, end):
                if isTitle(lines[i]):
                    titleLine = i
                    break

            if titleLine >= 0:
                InnerText = mkString(lines[start:titleLine])
                code = mkString(lines[titleLine:end])
            else:
                InnerText = mkString(lines[start: end])
                code = ""

            sonCount += 1
            new_son = \
                MarkdownBlock(title, InnerText, code, sonLevel, self.path + str(sonCount))
            self.son.append(new_son)
            new_son.parseSon()

        # code = mkString(lines[end:])

    def isLeaf(self):
        return len(self.son) == 0


def parseTitle(lines, depth):
    levelList = []
    if type(lines) == str:
        lines = lines.split('\n')

    for i in range(len(lines)):
        if isDepth(lines[i], depth):
            levelList.append(i)

    return levelList


def isTitle(text):
    text1 = text.strip()
    i = 0
    while i < len(text1) and text1[i] == '#':
        i += 1

    if 0 < i < len(text1) and text1[i] == " ":
        return i + 1 < len(text1)
    else:
        return False


def isDepth(text, depth=1):
    text1 = text.strip()
    if len(text1) < depth + 2:
        return False
    ok = True
    for i in range(depth):
        if text1[i] != "#":
            ok = False
            break

    if text1[depth] != " ":
        ok = False

    return ok


def mkString(lines):
    if len(lines) == 0:
        return ""

    text = ""
    for line in lines:
        text += "\n" + line
    return text.strip()


def pathAddDot(path):
    path = str(path).strip()
    re = ""
    for i in path:
        re += "." + i
    return re[1:]


def getRoot(text):
    lines = text.split("\n")

    innerTextEnd = 0
    for i in range(len(lines)):
        if isTitle(lines[i]):
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

    path = pathAddDot(node.path)

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
    spaces = " " * node.depth
    # jing = "#" * node.depth
    jing = "- []"

    title = node.title
    if len(title) == 0:
        title = "[空]"

    path = pathAddDot(node.path)

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


dir = "C:\\Users\\konghaomin\\CLionProjects\\23nuist816\\nuist816\\7.Graph图"
filename = "7.Graph图.md"
path = dir + "\\" + filename

with open(path, encoding='utf-8') as file_obj:
    contents = file_obj.read()
    md = contents.rstrip()

rootEle = getRoot(md)

rootEle.parseSon()

todoText = OutPutTitleTodoList(rootEle)
print(todoText)
f = open(dir + "\\" + filename + ".todo.md", "w", encoding='utf-8')
f.write(todoText)
f.close()


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
    structPath = pathAddDot(node.path) + "."
    blocks = node.inner_text.split("```C")

    if len(blocks) >= 1:
        title = node.title
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

            f = open(saveDir + "\\" + title + countStr + ".c"
                     , "w", encoding='utf-8')
            ccode = blockStr.strip()
            ccode = handleCCode(ccode)
            f.write(ccode)
            f.close()

    for i in node.son:
        findCCode(i)


findCCode(rootEle)

print()
