"""Test logger."""

import logging
import os
from pathlib import Path
from typing import Any

from pytoda.logger import log_full_width, print_header, setup_logging

log = logging.getLogger("pytoda")


def test_logger_file(tmp_path: Path):
    """Test logging to log file.

    Args:
        tmp_path (Path): Temporary path from pytest.
    """

    # create sim directory manually due to RunManager not being called
    os.makedirs(os.path.join(tmp_path, "test_sim"), exist_ok=True)

    setup_logging(
        log_to_console=False,
        log_file="test.log",
        output_directory=str(tmp_path),
        sim_name="test_sim",
        logger_name="pytoda",
    )
    log.info("This is a test log message.")

    log_file = tmp_path / "test_sim" / "test.log"
    assert log_file.exists()

    with open(log_file, "r") as f:
        log_content = f.read()
        assert "This is a test log message." in log_content

    # check invalid input parameter combination
    try:
        setup_logging(
            log_to_console=False,
            log_file="test.log",
            output_directory=None,
            sim_name=None,
            logger_name="pytoda",
        )
    except ValueError as error:
        assert str(error) == (
            "Output directory and sim name must be provided for output!"
        )


def test_logger_console(caplog: Any):
    """Test logging to console.

    Args:
        caplog (Any): Log capture from terminal output.
    """

    setup_logging(
        log_to_console=True,
        log_file=None,
        output_directory=None,
        sim_name=None,
        logger_name="pytoda",
    )

    log.propagate = True

    with caplog.at_level(logging.DEBUG, logger="pytoda"):
        log.info("This is a test log message.")

    assert "This is a test log message." in caplog.text


def test_logger_print_header(tmp_path: Path):
    """Test logging header print.

    Args:
        tmp_path (Path): Temporary path from pytest.
    """

    # create sim directory manually due to RunManager not being called
    os.makedirs(os.path.join(tmp_path, "test_sim"), exist_ok=True)

    setup_logging(
        log_to_console=False,
        log_file="test.log",
        output_directory=str(tmp_path),
        sim_name="test_sim",
        logger_name="pytoda",
    )
    print_header("PyToDa", "A dummy log line")
    log.info("This is a test log message.")

    log_file = tmp_path / "test_sim" / "test.log"
    assert log_file.exists()

    with open(log_file, "r") as f:
        log_content = f.read()
        assert (
            "/ ____/ /_/ // / / /_/ / /_/ / /_/ /" in log_content
        )  # exemplary line in log
        assert "A dummy log line" in log_content


def test_logger_log_full_width(tmp_path: Path):
    """Test logging full width log.

    Args:
        tmp_path (Path): Temporary path from pytest.
    """

    # create sim directory manually due to RunManager not being called
    os.makedirs(os.path.join(tmp_path, "test_sim"), exist_ok=True)

    setup_logging(
        log_to_console=False,
        log_file="test.log",
        output_directory=str(tmp_path),
        sim_name="test_sim",
        logger_name="pytoda",
    )
    log_full_width("THIS IS A TEST")
    log_full_width()

    log_file = tmp_path / "test_sim" / "test.log"
    assert log_file.exists()

    with open(log_file, "r") as f:
        log_content = f.read()
        assert (
            "====================== THIS IS A TEST ======================"
            in log_content
        )
        assert (
            "============================================================"
            in log_content
        )
