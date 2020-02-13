#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ast import FunctionDef
from typing import Dict, List, Optional

from .command_param import CommandParam
from .command_return import CommandReturn


def _right_pad(string, count):
    return string + " " * (len(string) - count)


class CommandMethod(object):
    @property
    def name(self) -> str:
        return self._name

    @property
    def details(self) -> str:
        return self._main

    @property
    def params(self) -> Dict[str, CommandParam]:
        return self._params

    def __init__(self, name: str, main_doc: Optional[str], param_doc: Dict[str, CommandParam], return_doc: str, defn: FunctionDef, return_anno, impl):
        self._name = name

        if main_doc is None:
            self._main = "No documentation provided."
        else:
            self._main = main_doc

        self._params = param_doc
        self._return = CommandReturn(return_doc, return_anno)
        self._def = defn
        self._impl = impl

    def required_params(self) -> List[CommandParam]:
        result = list(filter(lambda x: not x.has_default, self._params.values()))
        result.sort(key=lambda x: x.index)
        return result

    def optional_params(self) -> List[CommandParam]:
        result = list(filter(lambda x: x.has_default, self._params.values()))
        result.sort(key=lambda x: x.index)
        return result

    def longest_param_name_length(self) -> int:
        if len(self.params) < 1:
            return 0

        return len(max(self.params.keys(), key=len))

    def call(self, args: Dict):
        return self._impl(**args)

    def short_params(self) -> str:
        result = ""

        for param in self.params.values():
            if param.has_default:
                if param.annotation is bool:
                    result += f"[--{param.name}] "
                elif param.annotation is None:
                    result += f"[--{param.name}=<{param.name[:2]}>] "
                else:
                    result += f"[--{param.name}=<{param.annotation.__name__}>] "
            else:
                result += f"<{param.name}> "

        return result

    def print_help(self, module_name):
        print(self.details)
        print("\nUsage:")
        print(f"\tpython -m {module_name} {self.name} {self.short_params()}")
        longest = self.longest_param_name_length()

        if len(self.params) > 0:
            print("\nPositional arguments:")

            for param in self.required_params():
                print("\t{}\t{}".format(_right_pad(param.name, longest), param.details))

        print("\nOptions:")
        print("\t--{}\t{}".format("help", "Show this screen."))

        for param in self.optional_params():
            print("\t--{}\t{}".format(_right_pad(param.name, longest), param.details))
