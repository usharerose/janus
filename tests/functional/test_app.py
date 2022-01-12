#!/usr/bin/env python
import os
from unittest import TestCase

from janus.app import Janus
from tests import ROOT


class GetAnalyzerTestCase(TestCase):

    def setUp(self):
        self.app = Janus()

    def test_analyze_file_complexity(self):
        paths = ('tests/data/sample_python/sample_file.py',)
        actual = self.app.process(paths)
        expected = {
            'data': [
                {'file': os.path.join(ROOT, 'data/sample_python/sample_file.py'),
                 'cyclomatic_complexity': 10}
            ]
        }
        self.assertTrue('data' in actual)
        self.assertEqual(actual['data'], expected['data'])

    def test_analyze_files_under_directory(self):
        paths = ('tests/data/sample_python/nesting_dir',)
        actual = self.app.process(paths)
        expected = {
            'data': [
                {'file': os.path.join(ROOT, 'data/sample_python/nesting_dir/sample_nesting_file.py'),
                 'cyclomatic_complexity': 2},
                {'file': os.path.join(ROOT, 'data/sample_python/nesting_dir/__init__.py'),
                 'cyclomatic_complexity': 1}
            ]
        }
        self.assertTrue('data' in actual)
        actual = actual['data']
        actual.sort(key=lambda item: item['file'])
        expected = expected['data']
        expected.sort(key=lambda item: item['file'])
        self.assertEqual(actual, expected)

    def test_analyze_with_multi_paths(self):
        paths = ('tests/data/sample_python/nesting_dir',
                 'tests/data/sample_python/sample_file.py')
        actual = self.app.process(paths)
        expected = {
            'data': [
                {'file': os.path.join(ROOT, 'data/sample_python/nesting_dir/sample_nesting_file.py'),
                 'cyclomatic_complexity': 2},
                {'file': os.path.join(ROOT, 'data/sample_python/nesting_dir/__init__.py'),
                 'cyclomatic_complexity': 1},
                {'file': os.path.join(ROOT, 'data/sample_python/sample_file.py'),
                 'cyclomatic_complexity': 10}
            ]
        }
        self.assertTrue('data' in actual)
        actual = actual['data']
        actual.sort(key=lambda item: item['file'])
        expected = expected['data']
        expected.sort(key=lambda item: item['file'])
        self.assertEqual(actual, expected)
