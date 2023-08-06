from argparse import ArgumentParser
from typing import Any, Dict

from pydantic import BaseModel

from clicasso.core import Command


class BaseCommand(BaseModel, Command):
    @classmethod
    def connect(cls, parser: ArgumentParser) -> None:
        super().connect(parser)
        for field in cls.__fields__.values():
            kwargs: Dict[str, Any] = {}
            if field.type_ == bool:
                kwargs["action"] = "store_true"
                kwargs["required"] = False
            parser.add_argument(f"--{field.name}", **kwargs)
