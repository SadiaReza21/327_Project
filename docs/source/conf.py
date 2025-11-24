# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Bazar_Kori'
copyright = '2025, Fariha Tasnim Pragga'
author = 'Fariha Tasnim Pragga'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',     
    'sphinx_autoapi.extension',     
    'sphinxcontrib.openapi',       
    'sphinxcontrib.redoc',
]

autoapi_type = 'python'
autoapi_dirs = ['../../']  
autoapi_keep_files = True
autoapi_generate_api_docs = True

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
