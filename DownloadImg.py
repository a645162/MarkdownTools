import re
import requests

path = r"C:\Users\konghaomin\CLionProjects\23nuist816\nuist816\6.TreeAndBTree\满k叉树.md"
directory = path[:path.rfind("\\")]
print(directory)

file = open(path, encoding="utf-8")
fileCode = file.read()
file.close()

testCode = \
    """
    ![3个节点的树和二叉树](img/3nodetree.png "3个节点的树和二叉树")
    ![](img/3nodetree.png)
    
    """

testCode = fileCode
# testCode = testCode + "\n" + fileCode

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
        print(url)
        file_name = url[url.rfind(r"/") + 1:]
        savePath = saveDir + file_name
        # print(file_name)

        r = requests.get(url)
        with open(savePath, "wb") as code:
            code.write(r.content)

        new_img_code = img_code.replace(url, "img/" + file_name)
        print(new_img_code)

        testCode.replace(img_code, new_img_code)

print(testCode)

with open(path, 'w', encoding='utf-8') as file:
    file.write(testCode)
