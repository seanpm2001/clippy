#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for clip.py
"""

import unittest

from clippy import begin_clippy


__version__ = "0.0.1"


class TestClip(unittest.TestCase):
    def test_begin_version(self):
        def valid():
            begin_clippy(["--version"])

        self.assertRaises(SystemExit, valid)


if __name__ == "__main__":
    unittest.main()
