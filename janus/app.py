#!/usr/bin/env python
"""
This module implements the analyzer of cyclomatic complexity
"""
from concurrent.futures import ProcessPoolExecutor
import os

from tree_sitter import Language, Parser


PY_LANGUAGE = Language('build-tree-sitter/my-languages.so', 'python')
CPU_COUNT = os.cpu_count()


class Janus(object):

    # refer to the value in https://github.com/tree-sitter/tree-sitter-python/blob/master/src/grammar.json
    DECISION_TYPES = [
        'if', 'elif', 'assert',  # condition
        'for', 'while',          # loop
        'except', 'with',        # try / except
        'and', 'or'              # logical operator
    ]

    def __init__(self, paths):
        """
        Args:
            paths (tuple): a tuple of strings, every item is the path of a file or directory
        """
        self._paths = paths

    def process(self):  # NOQA
        with ProcessPoolExecutor(max_workers=CPU_COUNT * 4) as executor:
            result = executor.map(self._calculate_file_complexity, self._visit_files())
        return {'data': [{'file': file_path, 'cyclomatic_complexity': complexity}
                         for file_path, complexity in result]}

    def _visit_files(self):
        for path in self._paths:
            if os.path.isfile(path):
                files_gen = (file_path for file_path in (path,))
            else:
                files_gen = (os.path.join(root, file_name)
                             for root, _, files in os.walk(path) for file_name in files)
            for _file_path in files_gen:
                yield os.path.abspath(_file_path)

    def _calculate_file_complexity(self, file_path):
        _parser = Parser()
        _parser.set_language(PY_LANGUAGE)
        with open(file_path, mode='rb') as f:
            tree = _parser.parse(f.read())
        decision_amount = self._search_decisions(tree.root_node)
        return file_path, decision_amount + 1  # V(G) = P + 1

    def _search_decisions(self, node):
        counter = 0
        queue = [node]
        while queue:
            _node = queue.pop(0)
            if _node.type in self.DECISION_TYPES:
                counter += 1
            queue.extend(_node.children)
        return counter
