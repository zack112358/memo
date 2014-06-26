"""
Simple Python memoization decorator.
Author Zachary McCord zjmccord@gmail.com.
This file is in the public domain.
"""

import functools
import unittest


def memoize(table_factory):
    """
    Memoization decorator.

    @memoize(dict)
    def fib(n):
        return 1 if n <= 1 else fib(n-1) + fib(n-2)

    Argument to decorator is a callable that produces a dict-like thing to
    memoize the function results with.

    Works on methods, too, but you have to put it *after* the @classmethod or
    @staticmethod decorators, if any.
    """
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

    def test_methods(self):
        global calls
        calls = 0
        class George(object):
            def __init__(self, n):
                self.n = n

            @memoize(dict)
            def fred(self):
                global calls
                calls += 1
                return self.n

            @classmethod
            @memoize(dict)
            def quux(cls):
                global calls
                calls += 1
                return "quux"
            
            @staticmethod
            @memoize(dict)
            def quuxley():
                global calls
                calls += 1
                return "quuxley"

        george_1 = George(1)
        george_2 = George(2)
        self.assertEqual(george_1.fred(), 1)
        self.assertEqual(george_2.fred(), 2)
        self.assertEqual(george_1.fred(), 1)
        self.assertEqual(george_2.fred(), 2)
        self.assertEqual(calls, 2)

        calls = 0
        self.assertEqual(George.quux(), "quux")
        self.assertEqual(george_1.quux(), "quux")
        self.assertEqual(george_2.quux(), "quux")
        self.assertEqual(calls, 1)

        calls = 0
        self.assertEqual(George.quuxley(), "quuxley")
        self.assertEqual(george_1.quuxley(), "quuxley")
        self.assertEqual(george_2.quuxley(), "quuxley")
        self.assertEqual(calls, 1)
