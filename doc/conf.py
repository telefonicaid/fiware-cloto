# -*- coding: utf-8 -*-

import os

# The paths that contain custom static files (such as style sheets).
html_static_path = ['_static']

# Check whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# Only import and set the theme if we're building docs locally; otherwise,
# readthedocs.org uses their theme by default, so no need to specify it.
if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

    # Override default css to get a larger width for local build
    def setup(app):
        app.add_stylesheet('mystyle.css')
else:
    # Override default css to get a larger width for ReadTheDoc build
    html_context = {
        'css_files': [
            'https://media.readthedocs.org/css/sphinx_rtd_theme.css',
            'https://media.readthedocs.org/css/readthedocs-doc-embed.css',
            '_static/mystyle.css'
        ],
    }

# The suffix of source filenames
source_suffix = '.rst'

# The master toctree document
master_doc = 'index'

# General information about the project
title = u'FIWARE-Bosun'
subtitle = u'Bosun'
copyright = u'2016, Telefónica I+D'
project = u':\n '.join([title, subtitle])
version = ''
release = ''

# HTML configuration
html_title = title + ': ' + subtitle
html_favicon = '_static/favicon.ico'
html_show_sphinx = True
html_show_copyright = False

# Custom sidebar templates
html_sidebars = {
    '**': ['globaltoc.html', 'sourcelink.html', 'searchbox.html'],
    'using/windows': ['windowssidebar.html', 'searchbox.html'],
}
