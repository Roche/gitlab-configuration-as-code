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

# import sys
# sys.path.insert(0, os.path.abspath('.'))
from recommonmark.transform import AutoStructify

on_rtd = os.environ.get("READTHEDOCS", None) == "True"

# -- Project information -----------------------------------------------------

project = "GitLab Configuration as Code"
copyright = "2019, Hoffmann-La Roche"
author = "Hoffmann-La Roche"

# The full version, including alpha/beta/rc tags
release = "0.1"

# -- General configuration ---------------------------------------------------

# The master toctree document.
master_doc = "index"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_markdown_tables",
    "recommonmark",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "default"
if not on_rtd:  # only import and set the theme if we're building docs locally
    try:
        import sphinx_rtd_theme

        extensions.append("sphinx_rtd_theme")
        html_theme = "sphinx_rtd_theme"
    except ImportError:  # Theme not found, use default
        pass

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

highlight_language = "yaml"

source_suffix = [".rst", ".md"]


def setup(app):
    app.add_config_value(
        "recommonmark_config",
        {
            # 'enable_auto_toc_tree': True,
        },
        True,
    )
    app.add_transform(AutoStructify)
