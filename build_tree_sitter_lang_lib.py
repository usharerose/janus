#!/usr/bin/env python
import os

from tree_sitter import Language


TREE_SITTER_LANG_SRC_DIR_ROOT = 'vendor'


def build_library():
    Language.build_library(
        # Store the library in the `build` directory
        'janus/build-tree-sitter/my-languages.so',

        # Include one or more languages
        [os.path.join(TREE_SITTER_LANG_SRC_DIR_ROOT, dir_name)
         for dir_name in os.listdir(TREE_SITTER_LANG_SRC_DIR_ROOT)]
    )


if __name__ == '__main__':
    build_library()
