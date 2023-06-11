import re
import urllib.parse as urllib_parse

import requests

path = r"C:\Users\konghaomin\CLionProjects\23nuist816\nuist816\6.TreeAndBTree\满k叉树.md"

ReplaceText = False
ReplaceText = True

directory = path[:path.rfind("\\")]
# print(directory)

file = open(path, encoding="utf-8")
fileCode = file.read()
file.close()

# fileCode = ""

testCode = \
    """
    ![3个节点的树和二叉树](img/3nodetree.png "3个节点的树和二叉树")
    ![](img/3nodetree.png)
    ![](img/3nodetree.png)
    ![img](https://img-blog.csdnimg.cn/20191030223222875.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MDY0NjUwOQ==,size_16,color_FFFFFF,t_70)
    
    """

if not ReplaceText:
    testCode = testCode + "\n" + fileCode
else:
    testCode = fileCode

regex_pattern = re.compile(r"!\[.*\]\(.+\)")
regex_url_pattern = re.compile(r"[a-zA-Z]+://[^\s]*")

allImgCode = regex_pattern.findall(testCode)

print(allImgCode)

count = 0
saveDir = directory + "\\img\\"

for img_code in allImgCode:
    url = img_code[img_code.find("(") + 1:img_code.rfind(")")]
    # print(url)

    urlList = regex_url_pattern \
        .findall(url)
    if len(urlList) == 1:
        url = urlList[0]
        # print(url)
        parseUrl = urllib_parse.urlparse(url)
        gUrl = parseUrl[0] + "://" + parseUrl[1] + "/" + parseUrl[2]
        # print(gUrl)
        file_name = gUrl[gUrl.rfind(r"/") + 1:]
        # print(file_name)
        savePath = saveDir + file_name

        r = requests.get(url)
        with open(savePath, "wb") as code:
            code.write(r.content)

        new_img_code = img_code.replace(url, "img/" + file_name)
        print(new_img_code)

        testCode = testCode.replace(img_code, new_img_code)

# print(testCode)

if ReplaceText:
    with open(path, 'w', encoding='utf-8') as file:
        file.write(testCode)
