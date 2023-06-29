import time
import datetime
import re as regex
import os
import getpass

replace_text_md_main = "<slidev_tool_text_main_body/>"

replace_text_username = "<slidev_tool_text_username/>"
replace_text_datetime = "<slidev_tool_text_date_time/>"

replace_dictionary = []
py_dir = os.path.dirname(os.path.abspath(__file__))


def read_file(path):
    if path is None:
        return ""

    path = path.strip()
    if not os.path.exists(path):
        return ""

    return_str = ""
    try:
        f = open(path, 'r', encoding='utf-8')
        return_str = f.read().strip()
        f.close()
    except IOError as e:
        e.print_exc()
    return return_str


def init_dictionary():
    replace_dictionary.clear()

    dictionary_path = os.path.join(py_dir, "Dictionary")
    dictionary_path = os.path.join(dictionary_path, "replace_text.txt")
    text = read_file(dictionary_path).strip().split("\n")
    for line in text:
        l = line.strip()

        t = l.split("=")
        t = [i.strip() for i in t]

        if len(t) == 2:
            replace_dictionary.append((t[0], t[1]))


init_dictionary()


def replace_hold_text(text, user_replace_list=None):
    user_name = getpass.getuser()
    date_time = time.strftime('%Y.%m.%d', time.localtime(time.time()))

    text = regex.sub(replace_text_username, user_name, text)
    text = regex.sub(replace_text_datetime, date_time, text)

    for replace_tuple in replace_dictionary:
        text = regex.sub(replace_tuple[0], replace_tuple[1], text)

    if user_replace_list is not None:
        for replace_tuple in user_replace_list:
            text = regex.sub(str(replace_tuple[0]), str(replace_tuple[1]), text)

    return text


class SlidevMD:

    def __init__(self, slidev_settings_md=None):
        self.MD_Code = ""

        self.slidev_settings = ""

        self.page_count = 0
        self.pages = []

        if slidev_settings_md is not None:
            self.slidev_settings_md_path = slidev_settings_md.strip()
            with open(self.slidev_settings_md_path) as f:
                self.MD_Code += f.read().strip() + "\n"
        else:
            self.slidev_settings_md_path = ""

    def set_slidev_settings_md(self, slidev_settings_md_path):
        slidev_settings = read_file(slidev_settings_md_path)

        slidev_settings = replace_hold_text(slidev_settings)

        self.slidev_settings = slidev_settings

    def add_page(self, md_code, template_code="", user_replace_list=None):
        template_code = template_code.strip()
        md_code = md_code.strip()

        if len(template_code) == 0:
            final_code = md_code
        else:
            final_code = template_code.replace(replace_text_md_main, md_code)

        final_code = replace_hold_text(final_code, user_replace_list)

        self.pages.append(final_code)
        self.page_count += 1

    def include_files(self, files_path, template_path=None, user_replace_list=None):

        if user_replace_list is None:
            user_replace_list = []

        if type(files_path) == str:
            files_path = [files_path]

        template_code = replace_text_md_main
        if template_path is not None:
            with open(template_path) as f:
                template_code = f.read().strip()

        for file in files_path:
            with open(file) as f:
                file_code = f.read().strip()

                self.add_page(file_code, template_code=template_code, user_replace_list=user_replace_list)

    def generate_code(self):
        self.MD_Code = ""

        if len(self.slidev_settings) > 0:
            page1 = self.pages[0].strip()
            if page1.startswith('---\n'):
                # 判断设置是否需要与第一页合并
                page1 = page1[4:].strip()
                settings_str = self.slidev_settings[:-3].strip()

                self.MD_Code += settings_str + "\n\n" + page1 + "\n"
            else:
                self.MD_Code += self.slidev_settings
                self.MD_Code += page1

        for i in range(1, len(self.pages)):
            page_code = self.pages[i].strip()

            if page_code.startswith('---\n'):
                self.MD_Code += '\n'
            else:
                self.MD_Code += "\n---\n\n"

            self.MD_Code += page_code + '\n'

    def copy_page(self, page_index=None):
        if page_index is None:
            page_index = len(self.pages) - 1

        self.pages.append(self.pages[page_index])

    def save_to_file(self, path, auto_run=False):
        f = open(path, 'w', encoding='utf-8')
        f.write(self.MD_Code.strip())
        f.close()

        if auto_run:
            # TODO: AUTORUN
            pass
