# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from disruptive import __version__
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'disruptive'
copyright = '2021, Disruptive Technologies Research AS'
author = 'Disruptive Technologies Research AS'

# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

html_theme_options = {
    'font_family': '"Open Sans", Roboto, sans-serif',
    'font_size': '15px',
    'head_font_family': '"Open Sans", Roboto, sans-serif',
    # toc
    'fixed_sidebar': True,
    'sidebar_collapse': False,
    'sidebar_header': False,
    'github_user': 'disruptive-technologies',
    'github_repo': 'disruptive-python',
    'github_button': True,
    'github_type': 'watch',
    'github_count': False,
    'logo': 'logo.svg',
    'show_powered_by': False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Napoleon Extension ------------------------------------------------------
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_ivar = True
napoleon_use_rtype = True
napoleon_use_param = True
napoleon_include_init_with_doc = False
