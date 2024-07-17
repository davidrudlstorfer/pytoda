"""Logging module."""

import logging
import os
from typing import Optional

import pyfiglet

TERMINAL_WIDTH = 60

# Define type of log for mypy check
# https://github.com/python/mypy/issues/5732
log: logging.Logger


def setup_logging(
    log_to_console: bool,
    log_file: Optional[str] = None,
    output_directory: Optional[str] = None,
    sim_name: Optional[str] = None,
    logger_name: Optional[str] = "pytoda",
) -> None:
    """Setup logging files and handlers.

    Args:
        log_file (str): log file name (if None, no log file is written)
        output_directory (str): path to output directory
        sim_name (str): current simulation name
        log_to_console (bool): option if log is written to console
        logger_name (str): global logger name for use in external repos
    """

    # define logger name
    global log
    log = logging.getLogger(logger_name)

    # setup format for logging to file
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%d-%m %H:%M:%S",
    )

    if log_file is not None:
        # create output folder structure
        if output_directory is None or sim_name is None:
            raise ValueError(
                "Output directory and sim name must be provided for output!"
            )
        os.makedirs(os.path.join(output_directory, sim_name), exist_ok=True)

        logging_file_path = os.path.join(
            output_directory,
            sim_name,
            log_file,
        )
        file_handler = logging.FileHandler(logging_file_path, mode="w")
        file_handler.setFormatter(formatter)
        log.propagate = False
        log.addHandler(file_handler)
        log.setLevel(logging.DEBUG)

    if log_to_console:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)
        log.setLevel(logging.DEBUG)


def print_header(title: str, description: str) -> None:
    """Print header with title and description.

    Args:
        title (str): Title of program.
        description (str): Description of program.
    """
    print_centered_multiline_block(
        pyfiglet.figlet_format(title, font="slant"), TERMINAL_WIDTH
    )
    print_centered_multiline_block(description, TERMINAL_WIDTH)


def print_centered_multiline_block(string: str, output_width: int) -> None:
    """Print a multiline text as a block in the center. This is a new test to
    test the docstring formatter.

    Args:
        string (str): String to be printed
        output_width (int): Terminal output width
    """
    lines = string.split("\n")
    max_line_width = max(len(line) for line in lines)
    if max_line_width % 2:
        output_width += 1
    for line in lines:
        log.info(line.ljust(max_line_width).center(output_width))  # noqa: F821


def log_full_width(text: Optional[str] = None) -> None:
    """Log full width text/headline.

    Args:
        text (Optional[str], optional): Text to be logged. Defaults to None and
        only prints new section.
    """
    if text is None:
        out_str = "=" * TERMINAL_WIDTH
    else:
        text_width = len(text)
        fill_width = int((TERMINAL_WIDTH - text_width) / 2) - 1
        out_str = "=" * fill_width + " " + text + " " + "=" * fill_width

    log.info("")  # noqa: F821
    log.info(out_str)  # noqa: F821
    log.info("")  # noqa: F821
