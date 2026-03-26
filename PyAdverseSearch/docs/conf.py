# Configuration Sphinx pour PyAdverseSearch
# docs/conf.py

import os
import sys

# Chemin vers le code source du projet
sys.path.insert(0, os.path.abspath('../..'))

# ---------------------------------------------------------------------------
# Informations du projet
# ---------------------------------------------------------------------------

project = 'PyAdverseSearch'
copyright = '2025-2026, Equipe PyAdverseSearch'
author = (
    'Anaïs Dariane Nikiema, Martin Queval, Thibault Stouls, Hugo Vicente, '
    'Benjamin Bouquet, Ewan Burasovitch, Mathys Lohézic, Axel Ozange, Mélissa Djenadi, '
    'James Genitrini, Lucas Hätet, Clément Hubert, Lucas Lablanche, '
    'Quentin Laparre, Benjamin Lecomte, Halim Luquet, Ilyes Zaidi'
)
release = '1.0'
version = '1.0'

# ---------------------------------------------------------------------------
# Extensions Sphinx
# ---------------------------------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',          # Génération auto depuis les docstrings
    'sphinx.ext.autosummary',      # Tableaux de résumé automatiques
    'sphinx.ext.napoleon',         # Support Google/NumPy style docstrings
    'sphinx.ext.viewcode',         # Lien vers le code source dans la doc
    'sphinx.ext.intersphinx',      # Liens croisés vers d'autres projets
    'sphinx.ext.todo',             # Support des directives .. todo::
    'sphinx.ext.coverage',         # Vérification de la couverture doc
    'sphinx_autodoc_typehints',    # Affichage des types depuis les annotations
]

# ---------------------------------------------------------------------------
# Configuration autodoc
# ---------------------------------------------------------------------------

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'special-members': '__init__',
    'inherited-members': False,
    'show-inheritance': True,
}

autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autosummary_generate = True

# ---------------------------------------------------------------------------
# Configuration Napoleon (docstrings style Sphinx/:param:)
# ---------------------------------------------------------------------------

napoleon_google_docstring = False
napoleon_numpy_docstring = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_ivar = True

# ---------------------------------------------------------------------------
# Configuration intersphinx
# ---------------------------------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# ---------------------------------------------------------------------------
# Todo
# ---------------------------------------------------------------------------

todo_include_todos = True

# ---------------------------------------------------------------------------
# Thème et HTML
# ---------------------------------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'navigation_depth': 4,
    'titles_only': False,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'logo_only': False,
}

html_static_path = ['_static']
html_css_files = ['custom.css']

html_title = 'PyAdverseSearch - Documentation'
html_short_title = 'PyAdverseSearch'

# ---------------------------------------------------------------------------
# Langue
# ---------------------------------------------------------------------------

language = 'fr'

# ---------------------------------------------------------------------------
# Autres
# ---------------------------------------------------------------------------

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'


