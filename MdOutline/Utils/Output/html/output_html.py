import os.path

import markdown
import time

import re

from dominate.tags import *
import dominate


# save as html file
# with open('test.html', 'w') as f:
#     f.write(doc.render())

def output_html(md_code, md_path=''):
    md_path = md_path.strip()

    if len(md_path) == 0:
        save_path = 'result.html'
    else:
        save_path = md_path + ".html"

    md_file_name = os.path.basename(md_path)

    html_document = html()

    html_head = head()
    html_body = body()

    html_document.add(html_head)
    html_document.add(html_body)

    html_head.add(title(md_file_name))
    html_head.add(style(
        """
        pre{
            overflow: auto;
            white-space: pre-wrap;
        }
        """
    ))

    meta_html_encoding = meta()
    meta_html_encoding['http-equiv'] = 'Content-Type'
    meta_html_encoding['content'] = 'text/html; charset=utf-8'

    html_head.add(meta_html_encoding)

    replace_text = '[]md2html_body{}]'.format(str(time.time()))

    md2html_body = div(replace_text)
    md2html_body['id'] = 'md2html_body'
    # md2html_body[0] = replace_text
    # print(md2html_body)

    html_body.add(md2html_body)

    html_body_text = markdown.markdown(md_code)

    final_html_code = html_document.render(pretty=True)
    final_html_code = final_html_code.replace(replace_text, "\n" + html_body_text + "\n")

    final_html_code = re.sub(r'<code>', '<pre><code>', final_html_code)
    final_html_code = re.sub(r'</code>', '</code></pre>', final_html_code)

    f = open(save_path, "w", encoding='utf-8')
    f.write(final_html_code)
    f.close()
