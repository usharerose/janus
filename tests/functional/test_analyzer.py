#!/usr/bin/env python
from unittest import TestCase

from tree_sitter import Language, Parser

from janus.analyzer import get_analyzer_by_extension, PythonAnalyzer


LANG_PYTHON = Language('janus/build-tree-sitter/my-languages.so', 'python')


class GetAnalyzerTestCase(TestCase):

    def test_get_analyzer_by_extension(self):
        instance = get_analyzer_by_extension('.py')
        self.assertTrue(isinstance(instance, PythonAnalyzer))

    def test_unregistered_extension(self):
        with self.assertRaises(NotImplementedError):
            get_analyzer_by_extension('.txt')


class DecisionAnalyzerTestCase(TestCase):

    def test_python_if(self):
        sample_code = """
        if __name__ == '__main__':
            print('test if')
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 1
        self.assertEqual(actual, expected)

    def test_python_if_with_else(self):
        sample_code = """
        if True:
            print('go if')
        else:
            print('go else')
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 1
        self.assertEqual(actual, expected)

    def test_python_elif(self):
        sample_code = """
        variable = 12

        if variable >= 10:
            print('greater than 10')
        elif variable > 0:
            print('greater than 0, less than 10')
        else:
            print('non positive')
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 2
        self.assertEqual(actual, expected)

    def test_python_assert(self):
        sample_code = """
        assert isinstance(1, float)
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 1
        self.assertEqual(actual, expected)

    def test_python_for_loop(self):
        sample_code = """
        for i in range(10):
            print(i)
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 1
        self.assertEqual(actual, expected)

    def test_python_while_loop(self):
        sample_code = """
        import time


        while True:
            time.sleep(2)
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 1
        self.assertEqual(actual, expected)

    def test_python_for_and_while_loop(self):
        sample_code = """
        variable = 10

        while variable:
            for i in range(variable):
                print(i)
            variable -= 1
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 2
        self.assertEqual(actual, expected)

    def test_try_except(self):
        sample_code = """
        try:
            1 / 0
        except ZeroDivisionError:
            raise
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 1
        self.assertEqual(actual, expected)

    def test_try_except_with_finally(self):
        sample_code = """
        try:
            1 / 0
        except ZeroDivisionError:
            print('caught')
        finally:
            print('finally')
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 1
        self.assertEqual(actual, expected)

    def test_try_with_multi_except(self):
        sample_code = """
        from other_module import return_random_value


        variable = return_random_value()


        try:
            1 / variable
        except ZeroDivisionError:
            print('catch ZeroDivisionError')
        except TypeError:
            print('catch TypeError')
        finally:
            print('finally')
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 2
        self.assertEqual(actual, expected)

    def test_with_keyword(self):
        sample_code = """
        import json


        with open('foo.py', 'r') as f:
            data = json.load(f)
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 1
        self.assertEqual(actual, expected)

    def test_logical_operator_or(self):
        # the `sample code` is equal to
        #
        # variable = 10
        # if isinstance(variable, int):
        #     print('variable is numeric')
        # elif isinstance(variable, float):
        #     print('variable is numeric')
        # else:
        #     print('variable is non-numeric')
        sample_code = """
        variable = 10
        if isinstance(variable, int) or isinstance(variable, float):
            print('variable is numeric')
        else:
            print('variable is non-numeric')
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 2
        self.assertEqual(actual, expected)

    def test_logical_operator_and(self):
        # the `sample code` is equal to
        #
        # variable = 10
        # if isinstance(variable, int):
        #     if variable > 0:
        #         print('variable is numeric')
        # else:
        #     print('variable is non-numeric')
        sample_code = """
        variable = 10
        if isinstance(variable, int) and variable > 0:
            print('variable is numeric and positive')
        else:
            print('another situation')
        """
        analyzer = PythonAnalyzer()
        tree = analyzer._parser.parse(sample_code.encode('utf-8'))
        actual = analyzer._search_decisions(tree.root_node)
        expected = 2
        self.assertEqual(actual, expected)
