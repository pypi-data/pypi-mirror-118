from __future__ import annotations

import sys
from abc import ABC
from argparse import ArgumentParser
from typing import List, Optional, Type, Union

from inflection import dasherize, underscore
from pydantic import BaseModel, ValidationError


class ParseError(Exception):
    def __init__(self, cause):
        super().__init__(str(cause))
        self.cause = cause


class Command(ABC):
    @classmethod
    def slug(cls) -> str:
        return dasherize(underscore(cls.__name__))

    @classmethod
    def connect(cls, parser: ArgumentParser) -> None:
        parser.set_defaults(cls=cls)


class CommandParser:
    def __init__(self, internal: Optional[ArgumentParser] = None):
        self._internal = internal or ArgumentParser()
        self._subparsers = self._internal.add_subparsers()

    def add(self, command: Union[Type[Command], Type[BaseModel]]) -> None:
        if issubclass(command, Command):
            command.connect(self._subparsers.add_parser(command.slug()))

    def parse(self, args: Optional[List[str]] = None) -> Command:
        namespace, _ = self._internal.parse_known_args(args)
        m = vars(namespace)
        try:
            cls = m.pop("cls")
        except KeyError:
            self._internal.print_usage()
            sys.exit(1)
        try:
            return cls(**{k: v for (k, v) in m.items() if v is not None})  # type: ignore
        except ValidationError as exc:
            raise ParseError(cause=exc) from exc

    @classmethod
    def from_commands(cls, *commands: Type[Command]) -> CommandParser:
        parser = cls()
        for command_cls in commands:
            parser.add(command_cls)
        return parser
