import logging
import os
from dataclasses import dataclass, field
from logging import Logger
from typing import Optional, Dict

from dataclasses_json import dataclass_json

logger: Logger = logging.getLogger(__name__)

OUTLOOK_SYNCER_BASE_DIRECTORY = os.path.join(
    os.path.expanduser("~"), ".python-outlook-syncer"
)
WEEKS_FROM_NOW = 2


@dataclass_json
@dataclass(frozen=True)
class AccountConfiguration:
    client_id: str
    client_secret: str = field(repr=False)
    tenant_id: str
    redirect_uri: str
    event_prefix: str
    exclude_subjects: list[str] = field(default_factory=list)


@dataclass_json
@dataclass(frozen=True)
class DefaultConfiguration:
    source_account: Optional[str] = None
    target_account: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class Configuration:
    accounts: Dict[str, AccountConfiguration]
    defaults: DefaultConfiguration = DefaultConfiguration()


def read_configuration_file(path) -> Configuration:
    configuration_path = os.path.join(path, "configuration.json")
    try:
        with open(configuration_path, "r") as f_in:
            return Configuration.from_json("".join(f_in.readlines()))
    except:
        raise RuntimeError(f"Couldn't parse configuration at path {configuration_path}")


@dataclass
class CLiArguments:
    base_directory: str
    weeks_from_now_to_sync: int
    source_account: Optional[str]
    target_account: Optional[str]
    verbose: bool


def parse_cli_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        prog="outlookcalendarsyncer",
        description="Utility script for replicating calendar events"
        " from source outlook account into target outlook account.",
    )
    parser.add_argument(
        "--configuration-directory",
        "-cd",
        type=str,
        dest="base_directory",
        default=OUTLOOK_SYNCER_BASE_DIRECTORY,
    )
    parser.add_argument(
        "--weeks-from-now-to-sync",
        "-w",
        type=int,
        dest="weeks_from_now_to_sync",
        default=WEEKS_FROM_NOW,
    )
    parser.add_argument("--source", type=str, required=False, default=None)
    parser.add_argument("--target", type=str, required=False, default=None)
    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        action="store_true",
        default=False,
    )

    parsed_arguments = parser.parse_args()

    if parsed_arguments.weeks_from_now_to_sync < 1:
        logger.error(
            "'--weeks-from-now-to-sync' must be positive number."
            f" Currently configured value: {parsed_arguments.weeks_from_now_to_sync}"
        )
        raise ValueError

    if source_account := parsed_arguments.source:
        source_account = source_account.strip()
    else:
        source_account = None

    if target_account := parsed_arguments.target:
        target_account = target_account.strip()
    else:
        target_account = None

    if source_account is not None and source_account == target_account:
        logger.error(
            "'--source' and '--target' must have different values"
            f" Currently configured value: {parsed_arguments.weeks_from_now_to_sync}"
        )
        raise ValueError

    return CLiArguments(
        base_directory=parsed_arguments.base_directory,
        weeks_from_now_to_sync=parsed_arguments.weeks_from_now_to_sync,
        source_account=source_account,
        target_account=target_account,
        verbose=parsed_arguments.verbose,
    )
