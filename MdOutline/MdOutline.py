import os
import sys

from Utils.Output.mindmap.freemind.freemind import output_freemind
from Utils.Output.opml.opml import output_opml_xmind

from MdUtils.File.FilesUtils import read_file
from MdUtils.File.Mindmap.Xmind import repair_xmind_files

from MdUtils.Parser.Struct.MdStruct import *
from Utils.Output.todolist.MdTodoList import *


def doall(md_path):
    print("\n\n\n开始", md_path)

    dir_path = os.path.dirname(md_path)
    filename = os.path.basename(md_path)

    md_code = read_file(md_path)

    root_node = make_root_node(md_code, filename)

    print(output_md_todolist(root_node))

    # output_opml(md_node=root_node, md_path=md_path)
    output_freemind(md_node=root_node, md_path=md_path)

    # print(root_node.get_struct_str())


if __name__ == '__main__':

    files_list = sys.argv[1:]

    if len(files_list) == 0:
        print("请将路径作为参数传入！")

    for md_path in files_list:
        print(md_path)
        if os.path.exists(md_path):
            doall(md_path)
