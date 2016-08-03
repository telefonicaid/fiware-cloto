# -*- coding: utf-8 -*-

import os
import sphinx_rtd_theme

# The paths that contain custom static files (such as style sheets).
html_static_path = ['_static']

# Check whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# Only import and set the theme if we're building docs locally; otherwise,
# readthedocs.org uses their theme by default, so no need to specify it.
html_theme = 'sphinx_rtd_theme'
html_style = None
html_theme_options = {}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

if not on_rtd:
    # Override default css to get a larger width for local build
    def setup(app):
        app.add_stylesheet('mystyle.css')
else:
    # Override default css to get a larger width for ReadTheDoc build
    html_context = {
        'css_files': [
            'https://www.fiware.org/style/fiware_readthedocs.css',
            'https://www.fiware.org/style/monokai_sublime_.css',
            'https://media.readthedocs.org/css/readthedocs-doc-embed.css',
            'https://fiware-orion.readthedocs.io/en/develop/css/theme_extra.css',
            'https://fiware-orion.readthedocs.io/en/develop/css/theme.css',
            'https://fiware-orion.readthedocs.io/en/develop/css/highlight.css',
            'https://fonts.googleapis.com/css?family=Lato:400,700|Roboto+Slab:400,700|Inconsolata:400,700',
            'https://media.readthedocs.org//css/badge_only.css'
        ],
    }

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# Icon for tabs, windows and bookmarks
html_favicon = '_static/favicon.ico'

# General information about the project.
project = u'FIWARE-Bosun: Cloto'
copyright = u'2016, Telefónica I+D'
version = ''
release = ''

# The “title” for HTML documentation
html_title = u'FIWARE-Bosun: Cloto'
html_short_title = u'FIWARE-Bosun: Cloto'

# The div class version option
theme_display_version = False