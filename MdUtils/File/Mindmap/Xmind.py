import zipfile

xml_code = \
    """
    '<?xml version="1.0" encoding="UTF-8" standalone="no"?><manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0" password-hint=""></manifest>'
    """


def repair_xmind_files(file_name):
    zip_file = zipfile.ZipFile(file_name, 'a')
    zip_file.writestr('META-INF/manifest.xml', xml_code.strip())
    zip_file.close()
