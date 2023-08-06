"""
This module is internal module for mylogging library. It's not supposed to be used by user.
"""

# from datetime import datetime
import warnings
from typing import Callable

from ._config import config
from . import colors
from .logger_module import my_logger


printed_infos = set()
user_filters = []
original_formatwarning = warnings.formatwarning
level_str_to_int = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}


logging_functions = {
    "DEBUG": my_logger.logger.debug,
    "INFO": my_logger.logger.info,
    "WARNING": my_logger.logger.warning,
    "ERROR": my_logger.logger.error,
    "CRITICAL": my_logger.logger.critical,
}


class CustomWarning(UserWarning):
    pass


def filter_out(message, level):
    # All logging can be turned off
    if config.FILTER == "ignore":
        return True

    # Check if sufficient level

    if level_str_to_int[level] < level_str_to_int[config.LEVEL]:
        return True

    message = config._repattern.sub("", message)[:150]

    # Filters
    if config.FILTER == "once":
        if message in printed_infos:
            return True
        else:
            printed_infos.add(message)

    for i in config.BLACKLIST:
        if i in message:
            return True


def log_warn(message, level, showwarning_details=True, stack_level=3):
    """If _TO_FILE is configured, it will log message into file on path _TO_FILE. If not _TO_FILE is configured, it will
    warn or print INFO message.

    Args:
        message (str): Any string content of warning.
        log_type (str): 'INFO' or something else, generated automatically from __init__ module.
        edit_showwarning (bool): Whether to override warnings details display. After warning, default one will be again used.
            Defaults to True.
    """

    if config.FILTER == "error":
        raise RuntimeError(message)

    if config._console_log_or_warn == "log":
        try:
            # From version 3.8
            logging_functions[level](message, stacklevel=stack_level)
        except TypeError:
            logging_functions[level](message)

    else:
        warnings.formatwarning = formatwarning_detailed if showwarning_details else formatwarning_stripped

        CustomWarning.__name__ = level
        CustomWarning.level = level

        warnings.warn(message, stacklevel=stack_level, category=CustomWarning)

        warnings.formatwarning = original_formatwarning


def objectize_str(message):
    """Make a class from a string to be able to apply escape characters and colors if raise.

    Args:
        message (str): Any string you use.

    Returns:
        Object: Object, that can return string if printed or used in warning or raise.
    """

    class X(str):
        def __repr__(self):
            return f"{message}"

    return X(message)


def formatwarning_detailed(message, category, filename, lineno, *args, **kwargs):
    """Function that can override warnings printed info. """
    return (
        f"\n\n{colors.colorize(category.__name__, level=category.level)}from {filename}:{lineno} {message}\n"
    )


def formatwarning_stripped(message, *args, **kwargs):
    """Function that can override warnings printed info."""
    return f"{message}\n"


class RedirectedLogsAndWarnings:
    def __init__(
        self, logs: list, warnings: list, showwarning_backup: Callable, OUTPUT_backup: str, STREAM_backup
    ) -> None:
        self.logs = logs
        self.warnings = warnings
        self.showwarning_backup = showwarning_backup
        self.OUTPUT_backup = OUTPUT_backup
        self.STREAM_backup = STREAM_backup

    def close_redirect(self):
        warnings.showwarning = self.showwarning_backup
        config.OUTPUT = self.OUTPUT_backup
        config.STREAM = self.STREAM_backup
        config.TO_LIST = None


def redirect_logs_and_warnings_to_lists(used_logs, used_warnings) -> RedirectedLogsAndWarnings:
    """For example if using many processes with multiprocessing, it may be beneficial to log from one place.
    It's possible to log to variables (logs as well as warnings), pass it to the main process and then log it
    with workings filter etc.

    To log stored logs and warnings, use

    Args:
        used_logs (list): List where logs will be stored
        used_warnings (list): List where warnings will be stored

    Returns:
        RedirectedLogsAndWarnings: Object, where you can reset redirect. Logs and warnings you already have
        from inserted parameters.
    """
    showwarning_backup = warnings.showwarning
    OUTPUT_backup = config.OUTPUT
    STREAM_backup = config.STREAM

    def custom_warn(message, category, filename, lineno, file=None, line=None):
        used_warnings.append(
            {
                "message": message,
                "category": category,
                "filename": filename,
                "lineno": lineno,
                "file": file,
                "line": line,
            }
        )

    warnings.showwarning = custom_warn
    config.OUTPUT = None
    config.STREAM = None
    config.TO_LIST = used_logs

    return RedirectedLogsAndWarnings(
        logs=used_logs,
        warnings=used_warnings,
        showwarning_backup=showwarning_backup,
        OUTPUT_backup=OUTPUT_backup,
        STREAM_backup=STREAM_backup,
    )
