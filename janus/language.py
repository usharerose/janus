#!/usr/bin/env python
import os

from tree_sitter import Language

from janus.settings import EXTENSION_LANG_NAME_MAPPING


TREE_SITTER_SO_FILE = os.path.join(os.path.dirname(__file__), 'build-tree-sitter/my-languages.so')


REGISTERED_TREE_SITTER_LANG = {extension: Language(TREE_SITTER_SO_FILE, lang_name)
                               for extension, lang_name in EXTENSION_LANG_NAME_MAPPING.items()}
