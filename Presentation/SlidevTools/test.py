import slidev

s1 = slidev.SlidevMD()

s1.set_slidev_settings_md(r'H:\Prj\MarkdownTools\Presentation\SlidevTools\example\template\apple\slidev_settings.md')

s1.include_files(
    r'H:\Prj\MarkdownTools\Presentation\SlidevTools\example\workdir\home.md',
    r'H:\Prj\MarkdownTools\Presentation\SlidevTools\example\template\apple\home_page.md',
    []
)

s1.include_files(
    r'H:\Prj\MarkdownTools\Presentation\SlidevTools\example\workdir\page1.md',
    r'H:\Prj\MarkdownTools\Presentation\SlidevTools\example\template\apple\page_template1.md',
    []
)
s1.include_files(
    r'H:\Prj\MarkdownTools\Presentation\SlidevTools\example\workdir\page1.md',
    r'H:\Prj\MarkdownTools\Presentation\SlidevTools\example\template\apple\page_template1.md',
    [
        [1, '2']
    ]
)

s1.generate_code()
s1.save_to_file(r'H:\Prj\MarkdownTools\Presentation\SlidevTools\example\workdir\final.md')
