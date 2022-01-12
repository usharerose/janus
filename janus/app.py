#!/usr/bin/env python
"""
This module implements the analyzer of cyclomatic complexity
"""
from concurrent.futures import ProcessPoolExecutor
import os

from janus.analyzer import get_analyzer_by_extension


CPU_COUNT = os.cpu_count()


class Janus(object):

    def process(self, paths):  # NOQA
        with ProcessPoolExecutor(max_workers=CPU_COUNT * 4) as executor:
            result = executor.map(self._calculate_file_complexity, self._visit_files(paths))
        return {'data': [{'file': file_path, 'cyclomatic_complexity': complexity}
                         for file_path, complexity in result]}

    def _visit_files(self, paths):
        for path in paths:
            if os.path.isfile(path):
                files_gen = (file_path for file_path in (path,))
            else:
                files_gen = (os.path.join(root, file_name)
                             for root, _, files in os.walk(path) for file_name in files)
            for _file_path in files_gen:
                yield os.path.abspath(_file_path)

    def _calculate_file_complexity(self, file_path):
        _, extension = os.path.splitext(file_path)
        try:
            analyzer = get_analyzer_by_extension(extension)
            complexity = analyzer.analyze(file_path)
        except NotImplementedError:
            complexity = None
        return file_path, complexity
