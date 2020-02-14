#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for command_module.py
"""
import inspect
import unittest
from inspect import FrameInfo

from clippy import clippy

# noinspection PyProtectedMember
from clippy.command_module import CommandModule, _parse_ast, _get_parent_stack_frame, _get_module_impl

__version__ = "0.0.1"


@clippy
def example_method(arg1, arg2, arg3=None):
    return f"{arg1} {arg2} {arg3}"


class TestCommandModule(unittest.TestCase):
    def test_create(self):
        command_module = CommandModule(index=0)
        self.assertIsNotNone(command_module)

    def test_create_invalid1(self):
        def invalid():
            # noinspection PyTypeChecker
            _ = CommandModule(None)

        self.assertRaises(ValueError, invalid)

    def test_create_invalid2(self):
        def invalid():
            # noinspection PyTypeChecker
            _ = CommandModule("test")

        self.assertRaises(TypeError, invalid)

    def test_description(self):
        command_module = CommandModule(index=0)
        self.assertEqual("Tests for command_module.py", command_module.documentation)

    def test_name(self):
        command_module = CommandModule(index=0)
        self.assertEqual("test_command_module", command_module.name)

    def test_version(self):
        command_module = CommandModule(index=0)
        self.assertEqual("0.0.1", command_module.version)

    def test_has_version(self):
        command_module = CommandModule(index=0)
        self.assertTrue(command_module.has_version)

    def test_print_help(self):
        command_module = CommandModule(index=0)
        command_module.print_help()

    def test_longest(self):
        command_module = CommandModule(index=0)
        self.assertEqual(9, command_module.longest_param_name_length)

    def test_parse_ast_invalid_type(self):
        def invalid():
            # noinspection PyTypeChecker
            _ = _parse_ast(37)

        self.assertRaises(TypeError, invalid)

    def test_parse_ast_no_file(self):
        def invalid():
            _ = _parse_ast("does_not_exist.py")

        self.assertRaises(ValueError, invalid)

    def test_parse_ast_folder(self):
        def invalid():
            _ = _parse_ast("tests")

        self.assertRaises(ValueError, invalid)

    def test_parse_empty_file(self):
        def invalid():
            _ = _parse_ast("tests/empty_file.py")

        self.assertRaises(ValueError, invalid)

    def test_get_parent_stack_frame(self):
        stack_frame = _get_parent_stack_frame(1)
        self.assertIsNotNone(stack_frame)

    def test_get_parent_stack_frame_invalid_type(self):
        def invalid():
            # noinspection PyTypeChecker
            _ = _get_parent_stack_frame("1")

        self.assertRaises(TypeError, invalid)

    def test_get_parent_stack_frame_invalid_index(self):
        def invalid():
            # noinspection PyTypeChecker
            _ = _get_parent_stack_frame(64)

        self.assertRaises(ValueError, invalid)

    def test_empty_parent_stack_frame(self):
        def invalid():
            # noinspection PyTypeChecker
            _ = _get_parent_stack_frame(1, [])

        self.assertRaises(ValueError, invalid)

    def test_invalid_parent_stack_frame(self):
        def invalid():
            # noinspection PyTypeChecker
            _ = _get_parent_stack_frame(1, [None])

        self.assertRaises(TypeError, invalid)

    def test_invalid_parent_stack_frame_not_list(self):
        def invalid():
            # noinspection PyTypeChecker
            _ = _get_parent_stack_frame(1, dict())

        self.assertRaises(TypeError, invalid)

    def test_get_module_impl_type(self):
        def invalid():
            _ = _get_module_impl(12)

        self.assertRaises(TypeError, invalid)

    def test_get_module_impl_empty(self):
        def invalid():
            _ = _get_module_impl(FrameInfo(frame="test", filename="test", lineno=0, function="test", code_context="test", index=0))

        self.assertRaises(ValueError, invalid)

    def test_get_module_impl_none(self):
        def invalid():
            _ = _get_module_impl(None)

        self.assertRaises(ValueError, invalid)

    def test_get_module_impl_no_spec(self):
        def invalid():
            parent_stack_frame = _get_parent_stack_frame(1)
            parent_module = inspect.getmodule(parent_stack_frame[0])

            # this simulates the scenario where we try to get a module without a module in the stack
            setattr(parent_module, "__spec__", None)
            _ = _get_module_impl(parent_stack_frame)

        self.assertRaises(ValueError, invalid)


if __name__ == "__main__":
    unittest.main()
