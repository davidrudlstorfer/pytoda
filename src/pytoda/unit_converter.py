"""Unit converter."""

import argparse
import logging
from typing import Optional

import pint

from pytoda.logger import log_full_width, print_header, setup_logging

log = logging.getLogger("pytoda")


class Converter:
    """Converter class."""

    def __init__(
        self,
        unit_length: str,
        unit_weight: str,
        unit_time: str,
        log: logging.Logger,
        enable_logging: bool = True,
    ):

        self.unit_length = unit_length
        self.unit_weight = unit_weight
        self.unit_time = unit_time
        self.log = log
        self.enable_logging = enable_logging

    def setup_target_unit_system(self) -> pint.UnitRegistry:
        """Setup the global target unit system.

        Returns:
            pint.UnitRegistry: pint unit registry system
        """

        ureg = pint.UnitRegistry()

        target_system = [
            f"@system {self.unit_length}{self.unit_weight}{self.unit_time} using international",  # noqa: 501
            f"{self.unit_length}",
            f"{self.unit_weight}",
            f"{self.unit_time}",
            "@end",
        ]
        ureg.System.from_lines(target_system, ureg.get_root_units)
        ureg.default_system = (
            f"{self.unit_length}{self.unit_weight}{self.unit_time}"
        )

        if self.enable_logging:
            self.log.info("Target unit system:")
            self.log.info("")
            self.log.info(f"     Length: {self.unit_length.rjust(10)}")
            self.log.info(f"     Weight: {self.unit_weight.rjust(10)}")
            self.log.info(f"     Time: {self.unit_time.rjust(12)}")
            self.log.info("")

        return ureg

    def convert(
        self,
        quantity: pint.Quantity,
        title: Optional[str] = None,
        target_unit: Optional[pint.Unit] = None,
    ) -> pint.Quantity:
        """Convert quantity to either the global target unit system or a
        specific target unit system. Optionally log results.

        Args:
            quantity (pint.Quantity): Quantity which gets converted.
            title (str): Name of the quantity to be logged.
            target_unit (Optional[pint.Unit], optional): Target unit if no
                conversion to the global target unit system is wanted.

        Returns:
            pint.Quantity: Converted quantity.
        """

        if target_unit:
            converted_quantity = quantity.to(target_unit)
        else:
            converted_quantity = quantity.to_base_units()

        if self.enable_logging:
            self.log.info(f"Converting {title or ""} ...")
            self.log.info(f"     Input quantity: {str(quantity).rjust(37)}")
            self.log.info(
                f"     Converted quantity: {f'{converted_quantity:.5e}'.rjust(33)}"  # noqa: 501
            )
            self.log.info("")

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

    converter = Converter(
        unit_length=args.unit_length,
        unit_weight=args.unit_weight,
        unit_time=args.unit_time,
        log=log,
        enable_logging=True,
    )

    ureg = converter.setup_target_unit_system()

    converter.convert(ureg.Quantity(args.quantity))

    log_full_width("Unit conversion finished")


if __name__ == "__main__":  # pragma: no cover

    main()
    exit(0)
