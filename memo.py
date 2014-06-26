"""
Simple Python memoization decorator.
Author Zachary McCord zjmccord@gmail.com.
This file is in the public domain.
"""

import functools
import unittest


def memoize(table_factory):
    return functools.partial(_memoize, table_factory=table_factory)


def _memoize(f, table_factory):
    table = table_factory()
    def fprime(*args):
        try:
            return table[args]
        except (KeyError, IndexError):
            result = f(*args)
            table[args] = result
            return result

    functools.update_wrapper(fprime, f)
    fprime.table = table

    return fprime


class MemoizeTest(unittest.TestCase):
    def test_repeat(self):
        global called
        called = False
        @memoize(dict)
        def example_fun():
            global called
            self.assertFalse(called)
            called = True
            return "fred"
        
        self.assertEqual(example_fun(), "fred")
        self.assertEqual(example_fun(), "fred")

    def test_fib(self):
        global calls
        calls = 0
        @memoize(dict)
        def fib(n):
            global calls
            calls += 1
            return 1 if n <= 1 else fib(n-1) + fib(n-2)
        
        self.assertEqual(fib(5), 8)
        self.assertEqual(calls, 6)
