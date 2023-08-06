import json
import logging
import os
import pathlib
import readline
from logging import Logger

from outlookcalendarsyncer.configuration import (
    read_configuration_file,
    parse_cli_arguments,
    AccountConfiguration,
    Configuration,
    DefaultConfiguration,
)
from outlookcalendarsyncer.loggingutils import setup_console_logging, setup_file_logging
from outlookcalendarsyncer.outlook import OfficeAccount
from outlookcalendarsyncer.synchronizer import synchronize_calendars

logger: Logger = logging.getLogger(__name__)


def create_outlook_account(
        account_names: list[str],
        account_configurations: dict[str, AccountConfiguration],
        configuration_base_directory: str,
        debug_name: str,
) -> OfficeAccount:
    def first_not_none(values: list[str], default: str = None):
        return next((value for value in values if value is not None), default)

    account_name = first_not_none(account_names)

    if not account_name:
        logger.error(
            f"{debug_name} account name should be configured either through CLI or through 'configuration.json'"
        )
        raise ValueError

    if account_configuration := account_configurations.get(account_name):
        return OfficeAccount(
            name=account_name,
            configuration=account_configuration,
            configuration_base_directory=configuration_base_directory,
        )
    else:
        logger.error(
            f"Account configuration for {debug_name} account with"
            f" name '{account_name}' is not presented in 'configuration.json'"
        )
        raise ValueError


def main():
    cli_arguments = parse_cli_arguments()

    setup_console_logging(cli_arguments.verbose)

    logger.debug(f"CLI arguments {cli_arguments}")

    configuration_base_directory = cli_arguments.base_directory

    base_directory = pathlib.Path(configuration_base_directory)
    log_path = os.path.join(configuration_base_directory, "debug.log")

    try:
        if not base_directory.exists():
            logger.info(
                "Base configuration directory does not exist. Creating one with configuration template..."
            )
            base_directory.mkdir()
            configuration_json_path = os.path.join(base_directory, "configuration.json")
            with open(configuration_json_path, "w") as f_out:
                configuration_template = Configuration(
                    accounts={
                        "<outlook_account_short_name_1>": AccountConfiguration(
                            client_id="<client_id> for registered azure applications",
                            client_secret="<client_secret> for registered azure applications",
                            tenant_id="<tenant_id> for registered azure applications",
                            redirect_uri="<redirect_uri> for registered azure applications",
                            event_prefix="<event_prefix> for registered azure applications",
                            exclude_subjects=[
                                "Meeting with such subject should not be synced",
                                "Regexp are supported\\s+$",
                            ],
                        ),
                        "<outlook_account_short_name_2>": AccountConfiguration(
                            client_id="<client_id> for registered azure applications",
                            client_secret="<client_secret> for registered azure applications",
                            tenant_id="<tenant_id> for registered azure applications",
                            redirect_uri="<redirect_uri> for registered azure applications",
                            event_prefix="<event_prefix> for registered azure applications",
                            exclude_subjects=[
                                "Meeting with such subject should not be synced",
                                "Regexp are supported\\s+$",
                            ],
                        ),
                    },
                    defaults=DefaultConfiguration(
                        source_account="<outlook_account_short_name_1>. Calendar events would be read from",
                        target_account="<outlook_account_short_name_2>. Calendar events would be written to",
                    ),
                )
                configuration_template_dict = configuration_template.to_dict()
                json.dump(configuration_template_dict, f_out, indent=2)
            logger.info(
                f"Done."
                f" Please fill 'configuration.json' file with right variables."
                f" Full path to configuration file: {configuration_json_path}"
            )
        else:
            setup_file_logging(log_path)

            logger.info("Reading configuration directory...")

            configuration = read_configuration_file(configuration_base_directory)
            logger.debug(f"'configuration.json' content: {configuration}")

            logger.info("Opening connection to source account...")
            source_account = create_outlook_account(
                [cli_arguments.source_account, configuration.defaults.source_account],
                configuration.accounts,
                configuration_base_directory,
                "Target",
            )
            logger.info("Opening connection to target account...")
            target_account = create_outlook_account(
                [cli_arguments.target_account, configuration.defaults.target_account],
                configuration.accounts,
                configuration_base_directory,
                "Source",
            )

            synchronize_calendars(
                source_account,
                target_account,
                cli_arguments.weeks_from_now_to_sync,
            )
            logger.info("Application finished successfully. Have a nice day :)")
    except Exception:
        logger.exception(
            f"An error has occurred. Failed to synchronize accounts. Debug log can be found here: '{log_path}'"
        )
