#!/usr/bin/env python
"""
This module implements the analyzer of cyclomatic complexity
"""
from tree_sitter import Language, Parser


PY_LANGUAGE = Language('build-tree-sitter/my-languages.so', 'python')


class Janus(object):

    # refer to the value in https://github.com/tree-sitter/tree-sitter-python/blob/master/src/grammar.json
    DECISION_TYPES = [
        'if', 'elif', 'assert',  # condition
        'for', 'while',          # loop
        'except', 'with',        # try / except
        'and', 'or'              # logical operator
    ]

    def __init__(self):
        self.parser = Parser()
        self.parser.set_language(PY_LANGUAGE)

    def process(self, f_path):  # NOQA
        with open(f_path, mode='rb') as f:
            tree = self.parser.parse(f.read())
        complexity = self._search_decisions(tree.root_node)
        return {'data': [{'file_path': f_path,
                          'cyclomatic_complexity': complexity}]}

    def _search_decisions(self, node):
        counter = 0
        queue = [node]
        while queue:
            _node = queue.pop(0)
            if _node.type in self.DECISION_TYPES:
                counter += 1
            queue.extend(_node.children)

        return counter + 1  # V(G) = P + 1
