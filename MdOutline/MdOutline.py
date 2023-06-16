import os

from MdUtils.File.FilesUtils import read_file

path = r'H:\Prj\MarkdownTools\test\树.md'
dir = os.path.dirname(path)
filename = os.path.basename(path)

md_code = read_file(filename)
