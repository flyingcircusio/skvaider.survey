import argparse
import sys
import tomllib
from collections.abc import Callable
from pathlib import Path
from typing import cast

import skvaider.survey.web
from skvaider.survey.config import Config


class ConfigOptions:
    func: Callable
    config: Path

    def __contains__(self, key: str) -> bool: ...


def main():
    parser = argparse.ArgumentParser(
        prog="Skvaider Survey",
        description="Tools for evaluating AI models and manage model progression",
    )
    parser.add_argument("-c", "--config", default="config.toml", type=Path)

    subparsers = parser.add_subparsers()

    web = subparsers.add_parser("web")
    web.set_defaults(func=skvaider.survey.web.main)

    args = cast(ConfigOptions, parser.parse_args())

    if "func" not in args:
        parser.print_usage()
        sys.exit(1)

    config_data = tomllib.load(args.config.open("rb"))
    app_config = Config.model_validate(config_data)

    args.func(app_config)
