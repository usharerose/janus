#!/usr/bin/env python
"""
This module implements the analyzer of cyclomatic complexity
"""
from tree_sitter import Language, Parser


PY_LANGUAGE = Language('build-tree-sitter/my-languages.so', 'python')


class Janus(object):

    DECISION_TYPE = ['if_statement',
                     'elif_clause',
                     'for_statement',
                     'while_statement',
                     'except_clause',
                     'with_statement',
                     'assert_statement',
                     'list_comprehension']

    def __init__(self):
        self.parser = Parser()
        self.parser.set_language(PY_LANGUAGE)

    def process(self, f_path):  # NOQA
        with open(f_path, mode='rb') as f:
            tree = self.parser.parse(f.read())
        complexity = self._search_statement(tree.root_node)
        return {'data': [{'file_path': f_path,
                          'cyclomatic_complexity': complexity}]}

    def _search_statement(self, node):
        counter = 0
        queue = [node]
        while queue:
            _node = queue.pop(0)
            if _node.type in self.DECISION_TYPE:
                counter += 1
            for _child_node in _node.children:
                queue.append(_child_node)

        return counter + 1  # V(G) = P + 1
