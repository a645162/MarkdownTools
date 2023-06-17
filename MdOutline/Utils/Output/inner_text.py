def get_inner_text(md_node, remove_blank_lines=True):
    re = ""

    if len(md_node.inner_text) > 0:
        lines = md_node.inner_text.split("\n")
        for line in lines:
            if (not remove_blank_lines) or len(line.strip()) > 0:
                re += line + "\n"

    return re
