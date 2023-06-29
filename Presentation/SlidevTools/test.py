import slidev

s1 = slidev.SlidevMD()

s1.set_slidev_settings_md(r'template\slidev_template\apple-basic\slidev_settings.md')

s1.include_files(
    r'example\workdir\home.md',
    r'template\slidev_template\apple-basic\home_page.md',
    []
)

s1.include_files(
    r'example\workdir\page1.md',
    r'template\slidev_template\apple-basic\page_template1.md',
    []
)
s1.include_files(
    r'example\workdir\page1.md',
    r'template\slidev_template\apple-basic\page_template1.md',
    [
        [1, '2']
    ]
)

s1.generate_code()
s1.save_to_file(r'example\workdir\final.md')
