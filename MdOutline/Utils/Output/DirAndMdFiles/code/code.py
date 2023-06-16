import os


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
