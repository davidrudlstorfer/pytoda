"""Unit converter."""

import argparse
import logging
from typing import Optional

import pint

from pytoda.logger import log_full_width, print_header, setup_logging

log = logging.getLogger("pytoda")

# Define type of ureg for mypy check
# https://github.com/python/mypy/issues/5732
ureg: pint.UnitRegistry


def define_target_unit_system(
    unit_length: str,
    unit_weight: str,
    unit_time: str,
    enable_logging: bool = True,
) -> pint.UnitRegistry:
    """Define the global target unit system.

    Args:
        unit_length (str): Target unit for length.
        unit_weight (str): Target unit for weight.
        unit_time (str): Target unit for time.
        enable_logging (bool, optional): Enable logging of the target unit
            system. Defaults to True.

    Returns:
        pint.UnitRegistry: pint unit registry system
    """

    global ureg
    ureg = pint.UnitRegistry()

    target_system = [
        f"@system {unit_length}{unit_weight}{unit_time} using international",
        f"{unit_length}",
        f"{unit_weight}",
        f"{unit_time}",
        "@end",
    ]
    ureg.System.from_lines(target_system, ureg.get_root_units)
    ureg.default_system = f"{unit_length}{unit_weight}{unit_time}"

    if enable_logging:
        log.info("Target unit system:")
        log.info("")
        log.info(f"     Length: {unit_length.rjust(10)}")
        log.info(f"     Weight: {unit_weight.rjust(10)}")
        log.info(f"     Time: {unit_time.rjust(12)}")
        log.info("")

    return ureg


def convert(
    quantity: pint.Quantity,
    title: Optional[str] = None,
    target_unit: Optional[pint.Unit] = None,
    enable_logging: bool = True,
) -> pint.Quantity:
    """Convert quantity to either the global target unit system or a specific
    target unit system. Optionally log results.

    Args:
        quantity (pint.Quantity): Quantity which gets converted.
        title (str): Name of the quantity to be logged.
        target_unit (Optional[pint.Unit], optional): Target unit if no
            conversion to the global target unit system is wanted.
        enable_logging (bool, optional): Enable logging of the conversion.
            Defaults to True.

    Returns:
        pint.Quantity: Converted quantity.
    """

    if target_unit:
        converted_quantity = quantity.to(target_unit)
    else:
        converted_quantity = quantity.to_base_units()

    if enable_logging:
        log.info(f"Converting {title or ""} ...")
        log.info(f"     Input quantity: {str(quantity).rjust(37)}")
        log.info(
            f"     Converted quantity: {f'{converted_quantity:.5e}'.rjust(33)}"
        )
        log.info("")

    return converted_quantity


def main() -> None:
    """Parse arguments and call convert quantities."""

    parser = argparse.ArgumentParser(
        description=("Utility to format 4C input .dat files.")
    )
    parser.add_argument(
        "--unit_length",
        "-ul",
        help="Length unit for target unit system",
        type=str,
        default="m",
    )
    parser.add_argument(
        "--unit_weight",
        "-uw",
        help="Weight unit for target unit system",
        type=str,
        default="kg",
    )
    parser.add_argument(
        "--unit_time",
        "-ut",
        help="Time unit for target unit system",
        type=str,
        default="s",
    )
    parser.add_argument(
        "--quantity",
        "-q",
        help="Quantity to convert",
        type=str,
        default="1 newton",
    )

    args = parser.parse_args()

    setup_logging(
        log_to_console=True,
        log_file=None,
        output_directory=None,
        sim_name=None,
        logger_name="pytoda",
    )

    print_header(
        title="PyToDa",
        description="Unit Converter",
    )

    log_full_width("Unit conversion started")

    ureg = define_target_unit_system(
        unit_length=args.unit_length,
        unit_weight=args.unit_weight,
        unit_time=args.unit_time,
    )
    convert(ureg.Quantity(args.quantity))

    log_full_width("Unit conversion finished")


if __name__ == "__main__":  # pragma: no cover

    main()
    exit(0)
