# -*- coding: utf-8 -*-

import os

# The paths that contain custom static files (such as style sheets).
html_static_path = ['_static']

# Check whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# Only import and set the theme if we're building docs locally; otherwise,
# readthedocs.org uses their theme by default, so no need to specify it.
import sphinx_rtd_theme

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
#    html_context = {
#        'css_files': [
#            'https://media.readthedocs.org/css/sphinx_rtd_theme.css',
#            'https://media.readthedocs.org/css/readthedocs-doc-embed.css',
#            '_static/mystyle.css'
#        ],
#    }
    html_context = {
        'css_files': [
            'https://www.fiware.org/style/fiware_readthedocs.css',
            'https://www.fiware.org/style/monokai_sublime_.css',
            'https://media.readthedocs.org/css/readthedocs-doc-embed.css',
            'https://fiware-orion.readthedocs.io/en/develop/css/theme_extra.css',
            'https://fiware-orion.readthedocs.io/en/develop/css/theme.css'
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

html_sidebars = {
   '**': ['globaltoc.html', 'sourcelink.html', 'searchbox.html'],
   'using/windows': ['windowssidebar.html', 'searchbox.html'],
}

context = {
    'using_theme': True,
    'html_theme': html_theme,
    'current_version': "",
    'MEDIA_URL': "https://media.readthedocs.org/",
    'PRODUCTION_DOMAIN': "readthedocs.org",
    'versions': [
    ("latest", "/en/latest/"),
    ("stable", "/en/stable/"),
    ("v2.6.0", "/en/v2.6.0/"),
    ("v2.5.0", "/en/v2.5.0/"),
    ("v2.4.0", "/en/v2.4.0/"),
    ("v2.3.0", "/en/v2.3.0/"),
    ("v2.2.0", "/en/v2.2.0/"),
    ("v1.8.0", "/en/v1.8.0/"),
    ("readthedocs", "/en/readthedocs/"),
    ("feature-claudia-6224_readthedocs_problems", "/en/feature-claudia-6224_readthedocs_problems/"),
    ("develop", "/en/develop/"),
    ],
    'downloads': [
    ("pdf", "//readthedocs.org/projects/fiware-cloto/downloads/pdf/feature-claudia-6224_readthedocs_problems/"),
    ("htmlzip", "//readthedocs.org/projects/fiware-cloto/downloads/htmlzip/feature-claudia-6224_readthedocs_problems/"),
    ("epub", "//readthedocs.org/projects/fiware-cloto/downloads/epub/feature-claudia-6224_readthedocs_problems/"),
    ],
    'subprojects': [
    ],
    'slug': 'fiware-cloto',
    'name': u'FIWARE Bosun - Cloto',
    'rtd_language': u'en',
    'canonical_url': 'http://fiware-cloto.readthedocs.io/en/readthedocs/',
    'analytics_code': '',
    'single_version': False,
    'conf_py_path': '/doc/',
    'api_host': 'https://readthedocs.org',
    'github_user': 'telefonicaid',
    'github_repo': 'fiware-cloto',
    'github_version': 'feature-claudia-6224_ReadTheDocs_problems',
    'display_github': True,
    'bitbucket_user': 'None',
    'bitbucket_repo': 'None',
    'bitbucket_version': 'feature-claudia-6224_ReadTheDocs_problems',
    'display_bitbucket': False,
    'READTHEDOCS': True,
    'using_theme': (html_theme == "default"),
    'new_theme': (html_theme == "sphinx_rtd_theme"),
    'source_suffix': source_suffix,
    'user_analytics_code': '',
    'global_analytics_code': 'UA-17997319-1',

    'commit': '14419c12',

}

# Habría que saber el commit...