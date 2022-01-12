#!/usr/bin/env python
from tree_sitter import Parser

from janus.language import REGISTERED_TREE_SITTER_LANG


class BaseComplexityAnalyzer(object):

    EXTENSION = None
    DECISION_TYPES = []

    def __init__(self):
        self._parser = Parser()
        assert self.EXTENSION in REGISTERED_TREE_SITTER_LANG, f'Unregistered language extension: {self.EXTENSION}'
        self._parser.set_language(REGISTERED_TREE_SITTER_LANG[self.EXTENSION])

    def _search_decisions(self, node):
        counter = 0
        queue = [node]
        while queue:
            _node = queue.pop(0)
            if _node.type in self.DECISION_TYPES:
                counter += 1
            queue.extend(_node.children)
        return counter

    def analyze(self, file_path):
        with open(file_path, mode='rb') as f:
            tree = self._parser.parse(f.read())
        decision_amount = self._search_decisions(tree.root_node)
        return decision_amount + 1  # V(G) = P + 1


class PythonAnalyzer(BaseComplexityAnalyzer):

    EXTENSION = '.py'

    # refer to the value in https://github.com/tree-sitter/tree-sitter-python/blob/master/src/grammar.json
    DECISION_TYPES = [
        'if', 'elif', 'assert',  # condition
        'for', 'while',          # loop
        'except', 'with',        # try / except
        'and', 'or'              # logical operator
    ]


class GoAnalyzer(BaseComplexityAnalyzer):

    EXTENSION = '.go'

    # refer to the value in https://github.com/tree-sitter/tree-sitter-go/blob/master/src/grammar.json
    DECISION_TYPES = [
        'if', 'case',  # condition
        'for',         # loop
        '&&', '||'     # logical operator
    ]


def _get_registered_lang_analyzer_mapping():
    analyzer_mapping = {subklass.EXTENSION: subklass
                        for subklass in BaseComplexityAnalyzer.__subclasses__()}
    analyzer_ext_set = set(analyzer_mapping.keys())
    registered_ext_set = set(REGISTERED_TREE_SITTER_LANG.keys())
    assert analyzer_ext_set.issuperset(registered_ext_set), \
        'Please make sure that the languages of implemented Analyzers are registered in settings'
    return {extension: klass for extension, klass in analyzer_mapping.items()
            if extension in registered_ext_set}


ANALYZER_MAPPING = _get_registered_lang_analyzer_mapping()


def get_analyzer_by_extension(extension):
    if extension not in ANALYZER_MAPPING:
        raise NotImplementedError(f'Unsupported extension: {extension}')
    analyzer_klass = ANALYZER_MAPPING[extension]
    return analyzer_klass()
