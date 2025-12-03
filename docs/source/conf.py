# docs/source/conf.py
import os
import sys
from datetime import datetime

# Add project root to path so Sphinx can import your modules
sys.path.insert(0, os.path.abspath('../..'))  # ../../ because docs/source/ → project root

# -- Project information -----------------------------------------------------
project = 'Bazar Kori'
copyright = f'{datetime.now().year}, Yasmin Sultana Emu'
author = 'Yasmin Sultana Emu'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',      # Auto-generate docs from docstrings
    'sphinx.ext.viewcode',     # Add source code links
    'sphinx.ext.napoleon',     # Support Google/NumPy style docstrings
    'sphinx.ext.autosummary',  # Generate summary tables
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'   # Beautiful ReadTheDocs theme
html_static_path = ['_static']

# Logo (optional - add later)
# html_logo = "_static/logo.png"

# Theme options
html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- autodoc settings --------------------------------------------------------
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'special-members': '__init__',
    'inherited-members': True,
    'show-inheritance': True,
}