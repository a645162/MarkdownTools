# -*- coding:utf-8 -*-

from xml.etree import ElementTree  # 导入ElementTree模块


# element 为传进来的 Element 类，参数 indent 用于缩进，newline 用于换行
# 这段代码参考 https://zhuanlan.zhihu.com/p/54269963
def pretty_xml(element, indent='\t', newline='\n', level=0):
    # 判断element是否有子元素
    if element:
        # 如果element的text没有内容
        if element.text is None or str(element.text).isspace():
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + str(element.text).strip() + newline + indent * (level + 1)
            # 此处两行如果把注释去掉，Element的text也会另起一行
    # else:
    # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将 element 转成 list
    for sub_element in temp:
        # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
        if temp.index(sub_element) < (len(temp) - 1):
            sub_element.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            sub_element.tail = newline + indent * level
            # 对子元素进行递归操作
        pretty_xml(sub_element, indent, newline, level=level + 1)


def pretty_exist_xml_file(file_name):
    tree = ElementTree.parse(file_name)  # 解析test.xml这个文件，该文件内容如上文
    root = tree.getroot()  # 得到根元素，Element类
    pretty_xml(root, '\t', '\n')  # 执行美化方法

    # ElementTree.dump(root)                 #显示出美化后的XML内容

    tree.write(file_name, encoding='utf-8')
