#!/usr/bin/env python
"""
This is doc string
"""


# this is comment


# this is a class
class SampleClass(object):

    def __init__(self, a, b):
        assert isinstance(a, int) or isinstance(a, float)                    # 2 decisions
        assert isinstance(b, int) or isinstance(b, float)                    # 2 decisions
        self._a = a
        self._b = b

    def run(self):
        result = None
        try:
            result = self._a / self._b
        except ZeroDivisionError:                                            # 1 decision
            print('error')
        finally:
            return result


# this is a method
def hello_world():
    for i in range(10):                                                      # 1 decision
        while (isinstance(i, int) or isinstance(i, float)) and 0 <= i < 10:  # 3 decision
            print(i)
            i -= 1
