import zipfile

xml_code = \
    """
    '<?xml version="1.0" encoding="UTF-8" standalone="no"?><manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0" password-hint=""></manifest>'
    """


def repair_xmind_files(file_name):
    zip_file = zipfile.ZipFile(file_name, 'a')
    file_list = zip_file.filelist
    found = False
    target_file_name = 'META-INF/manifest.xml'
    for file in file_list:
        if file.filename == target_file_name:
            found = True
            break
    if not found:
        zip_file.writestr(target_file_name, xml_code.strip())
    zip_file.close()
