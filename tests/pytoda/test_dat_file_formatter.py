"""Test dat_file_formatter."""

import logging
import os
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from pytoda.dat_file_formatter import (
    format_content,
    format_dat_file,
    format_section,
    main,
    split_into_sections,
)

log = logging.getLogger("pytoda")


def test_dat_file_formatter_split_into_sections():
    """Test split_into_sections function."""

    file_content = [
        "-------LINE 1\n",
        "abcd\n",
        "efgh\n",
        "-------LINE 2\n",
        "ijkl\n",
        "mnop\n",
    ]

    sections = split_into_sections(file_content)

    ref_sections = [
        ("-------LINE 1", ["abcd", "efgh"]),
        ("-------LINE 2", ["ijkl", "mnop"]),
    ]

    assert sections == ref_sections


def test_dat_file_formatter_format_section():
    """Test format_section function."""

    section = [
        "DPOINT 1 2 3",
        "NODE 100 DNODE 1",
        "NODE 10 DNODE 10",
        "NODE 1 DNODE 100",
    ]
    format_columns = [1, 3]

    formatted_section = format_section(section, format_columns)

    ref_formatted_section = [
        "DPOINT 1 2 3",
        "NODE 100 DNODE   1",
        "NODE  10 DNODE  10",
        "NODE   1 DNODE 100",
    ]

    assert formatted_section == ref_formatted_section

    section = [
        "NODE 1 COORD -6.92820323e-01 -1.6e+00 0",
        "NODE 1000 COORD -4.187154267428349e-01 -1.692535787334366e+00 4.980333333333333e+00",  # noqa: E501
    ]
    format_colums = [1, 3, 4, 5]

    formatted_section = format_section(section, format_colums)

    ref_formatted_section = [
        "NODE    1 COORD        -6.92820323e-01               -1.6e+00 0.000000000000000e+00",  # noqa: E501
        "NODE 1000 COORD -4.187154267428349e-01 -1.692535787334366e+00 4.980333333333333e+00",  # noqa: E501
    ]

    assert formatted_section == ref_formatted_section


def test_dat_file_formatter_format_content():
    """Test format_content function."""

    file_content = [
        "----------DNODE-NODE TOPOLOGY\n",
        "NODE 1 DNODE 1000\n",
        "NODE 10 DNODE 100\n",
        "NODE 100 DNODE 10\n",
        "NODE 1000 DNODE 1\n",
        "---------------NODE COORDS\n",
        "NODE 1 COORD 6.9282032e-01 -1.600e+00 0.000e+00\n",
        "NODE 100 COORD -4.18715e-01 -1.6926e+00 0.123e+01\n",
        "---------------BLABLUB\n",
        "Testsection which is not formatted\n",
    ]

    format_sections = "DNODE-NODE TOPOLOGY", "NODE COORDS"

    formatted_content = format_content(file_content, format_sections)

    ref_formatted_content = [
        "----------DNODE-NODE TOPOLOGY",
        "NODE    1 DNODE 1000",
        "NODE   10 DNODE  100",
        "NODE  100 DNODE   10",
        "NODE 1000 DNODE    1",
        "---------------NODE COORDS",
        "NODE   1 COORD 6.9282032e-01  -1.600e+00 0.000e+00",
        "NODE 100 COORD  -4.18715e-01 -1.6926e+00 0.123e+01",
        "---------------BLABLUB",
        "Testsection which is not formatted",
    ]

    # test unknown section
    format_sections = "DNODE-NODE TOPOLOGY", "NODE COORDS", "BLABLUB"
    try:
        formatted_content = format_content(file_content, format_sections)
    except ValueError as error:
        assert str(error) == (
            "A given formatted section is currently not supported!"
        )

    assert formatted_content == ref_formatted_content


def test_dat_file_formatter_format_dat_file():
    """Test format_dat_file function."""

    dat_file_path = MagicMock()
    target_path = MagicMock()
    format_sections = MagicMock()

    with (
        patch("builtins.open") as mock_open,
        patch(
            "pytoda.dat_file_formatter.format_content"
        ) as mock_format_content,
    ):

        format_dat_file(dat_file_path, target_path, format_sections)

        assert mock_open.call_count == 2
        mock_format_content.assert_called_once()


def test_dat_file_formatter_main(caplog: Any):
    """Test main function.

    Args:
        caplog (Any): Log capture from terminal output.
    """

    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(
            dat_file_path="tmp/test.dat",
            output_file_path="tmp/test_new.dat",
            format_sections=["DNODE-NODE TOPOLOGY", "NODE COORDS"],
        ),
    ):

        with patch(
            "pytoda.dat_file_formatter.format_dat_file"
        ) as mock_format_dat_file:

            log.propagate = True

            with caplog.at_level(logging.DEBUG, logger="pytoda"):
                main()

            assert "4C input .dat file formatter" in caplog.text
            assert "Formatting started" in caplog.text

            mock_format_dat_file.assert_called_once_with(
                "tmp/test.dat",
                "tmp/test_new.dat",
                ["DNODE-NODE TOPOLOGY", "NODE COORDS"],
            )

            assert "Formatted 4C .dat input file written to:" in caplog.text
            assert "Formatting finished" in caplog.text


def test_dat_file_formatter_full_integration(tmp_path: Path):
    """Test full integration of dat_file_formatter.py.

    Args:
        tmp_path (Path): Temporary path from pytest.
    """

    format_dat_file(
        "tests/reference_files/dat_file_formatter_unformatted.dat",
        os.path.join(tmp_path, "input_file_formatted.dat"),
        [
            "DESIGN LINE BEAM POTENTIAL CHARGE CONDITIONS",
            "DNODE-NODE TOPOLOGY",
            "DLINE-NODE TOPOLOGY",
            "NODE COORDS",
            "STRUCTURE ELEMENTS",
        ],
    )

    with open(
        "tests/reference_files/dat_file_formatter_formatted.dat",
        "r",
    ) as ref_file:
        ref_lines = ref_file.read().splitlines()

    with open(os.path.join(tmp_path, "input_file_formatted.dat"), "r") as file:
        lines = file.read().splitlines()

    assert ref_lines == lines
