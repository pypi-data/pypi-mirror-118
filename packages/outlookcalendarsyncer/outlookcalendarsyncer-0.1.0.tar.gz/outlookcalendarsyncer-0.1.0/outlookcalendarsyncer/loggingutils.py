import logging
import sys


def setup_file_logging(log_path: str):
    file_log_handler = logging.FileHandler(
        filename=log_path,
        mode="w+",
        encoding="utf-8",
    )
    file_log_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s outlookcalendarsyncer [%(process)d]: %(message)s", "%b %d %H:%M:%S"
        )
    )
    file_log_handler.setLevel(logging.DEBUG)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_log_handler)
    root_logger.setLevel(logging.DEBUG)


def setup_console_logging(verbose: bool):
    from logging import LogRecord

    class ComponentLogFilter(logging.Filter):
        def __init__(self, name: str = ..., excluded_components=None) -> None:
            super().__init__(name)
            if excluded_components is None:
                excluded_components = set()
            self.__excluded_components = excluded_components

        def filter(self, record: LogRecord) -> bool:
            return record.name not in self.__excluded_components

    console_log_handler = logging.StreamHandler(sys.stdout)
    if verbose:
        console_log_handler.setLevel(logging.DEBUG)
    else:
        console_log_handler.setLevel(logging.INFO)

    console_log_handler.addFilter(
        ComponentLogFilter("O365.connection filter", {"O365.connection"})
    )

    root_logger = logging.getLogger()
    root_logger.addHandler(console_log_handler)
