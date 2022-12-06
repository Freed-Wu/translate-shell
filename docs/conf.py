"""Configure the Sphinx documentation builder.

https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
import os
from datetime import datetime

from setuptools_scm import get_version

from translate_shell.utils.output import ICON_FILE

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# -- Project information -----------------------------------------------------
language = "en"
copyright = "2022-" + str(datetime.now().year)
version = get_version("..").partition(".dev")[0]

PROJECT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "pyproject.toml"
)

with open(PROJECT_FILE, "rb") as f:
    data = tomllib.load(f)["project"]
    author = data["authors"][0]["name"]
    project = data["name"]

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "myst_parser",
]

myst_heading_anchors = 3
myst_title_to_header = True

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

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]
html_favicon = ICON_FILE
