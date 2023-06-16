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