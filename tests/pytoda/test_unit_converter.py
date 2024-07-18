"""Test unit_converter."""

import logging
from typing import Any
from unittest.mock import MagicMock, patch

from pytoda.unit_converter import Converter, main

log = logging.getLogger("pytoda")


def test_unit_converter_init():
    """Test converter init function."""

    log = MagicMock()

    converter = Converter(
        unit_length="m",
        unit_weight="kg",
        unit_time="s",
        log=log,
        enable_logging=False,
    )

    assert converter.unit_length == "m"
    assert converter.unit_weight == "kg"
    assert converter.unit_time == "s"
    assert converter.log == log
    assert converter.enable_logging is False


def test_unit_converter_setup_target_unit_system():
    """Test setup_target_unit_system function."""

    log = MagicMock()

    converter = Converter(
        unit_length="m",
        unit_weight="kg",
        unit_time="s",
        log=log,
        enable_logging=False,
    )

    ureg = converter.setup_target_unit_system()

    assert ureg.default_system == "mkgs"


def test_unit_converter_convert():
    """Test convert function."""

    log = MagicMock()

    converter = Converter(
        unit_length="meter",
        unit_weight="kilogram",
        unit_time="second",
        log=log,
        enable_logging=False,
    )

    ureg = converter.setup_target_unit_system()

    quantity = ureg.Quantity("1 newton")
    converted_quantity = converter.convert(quantity)

    assert converted_quantity.magnitude == 1.0
    assert converted_quantity.units == "kilogram * meter / second ** 2"

    quantity = ureg.Quantity("1 N/m**2")
    converted_quantity = converter.convert(quantity, target_unit="bar")

    assert converted_quantity.magnitude == 1.00000e-05
    assert converted_quantity.units == "bar"


def test_unit_converter_main(caplog: Any):
    """Test main function.

    Args:
        caplog (Any): Log capture from terminal output.
    """

    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(
            unit_length="nm", unit_weight="g", unit_time="ms", quantity="1 bar"
        ),
    ):

        log.propagate = True

        with caplog.at_level(logging.DEBUG, logger="pytoda"):
            main()

        assert "Unit conversion started" in caplog.text
        assert "Length:         nm" in caplog.text
        assert "Weight:          g" in caplog.text
        assert "Time:           ms" in caplog.text
        assert (
            "Input quantity:                                 1 bar"
            in caplog.text
        )
        assert (
            "Converted quantity:      1.00000e-07 g / ms ** 2 / nm"
            in caplog.text
        )
        assert "Unit conversion finished" in caplog.text
