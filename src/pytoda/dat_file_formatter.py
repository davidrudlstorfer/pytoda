"""4C input .dat file formatter."""

import argparse
import logging

from pytoda.logger import log_full_width, print_header, setup_logging

log = logging.getLogger("pytoda")

# sections which are currently supported and associated colums which should be
# aligned (starting at i = 0)
FORMAT_SECTIONS = {
    "DESIGN LINE BEAM POTENTIAL CHARGE CONDITIONS": [1, 4, 6],
    "DNODE-NODE TOPOLOGY": [1, 3],
    "DLINE-NODE TOPOLOGY": [1, 3],
    "NODE COORDS": [1, 3, 4, 5],
    "STRUCTURE ELEMENTS": [0, 3, 4, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17],
}

# Start of lines to be removed within sections
IGNORE_LINES = ["DPOINT", "DLINE"]

# Scientific format for 0 replacement of MeshPy coordinates/triads
FORMAT = "{:.15e}"


def split_into_sections(file_content: list) -> list:
    """Split the file content into sections, each starting with a line
    containing '-'.

    Args:
        file_content (list): List of lines from the .dat file.

    Returns:
        list: List of tuples, each containing a section header and its
            corresponding lines.
    """
    sections = []  # type: list
    current_section = None

    for line in file_content:
        # remove \n from end of line
        line = line.rstrip()

        if line.startswith("-"):
            current_section = (line, [])
            sections.append(current_section)
        elif current_section:
            current_section[1].append(line)

    return sections


def format_section(section: list, format_columns: list) -> list:
    """Format the specified columns of a section.

    Args:
        section (list): Lines of the section to be formatted
        format_columns (list): List of column indices to be formatted

    Returns:
        list: Formatted lines of the section
    """

    # split lines into columns and remove unnecessary first lines
    data = [line.split() for line in section]

    # initialize maximum widths for the specified formatted columns
    max_widths = [0] * len(format_columns)

    # determine maximum width for each specified column to be formatted
    for line in data:

        # ignore initially defined lines
        if any(line[0].startswith(start) for start in IGNORE_LINES):
            continue

        for i, col in enumerate(format_columns):
            if len(line[col]) > max_widths[i]:
                max_widths[i] = len(line[col])

    # Format the lines based on the maximum widths
    formatted_lines = []

    for line in data:

        # ignore initially defined lines
        if any(line[0].startswith(start) for start in IGNORE_LINES):
            formatted_lines.append(" ".join(line))
            continue

        # format line
        formatted_line = []
        for i, section in enumerate(line):
            if i in format_columns:
                # replace 0 coordinates/triads from MeshPy
                if section == "0":
                    section = FORMAT.format(0)  # type: ignore
                # add whitespace to each section
                formatted_line.append(
                    str(section).rjust(max_widths[format_columns.index(i)])
                )
            else:
                formatted_line.append(str(section))

        formatted_lines.append(" ".join(formatted_line))

    return formatted_lines


def format_content(file_content: list, format_sections: list) -> list:
    """Format content of 4C input .dat file. Provided sections will be
    formatted.

    Args:
        file_content (list): File content of the 4C input .dat file
        format_sections (list): List of sections which will be formatted

    Returns:
        str: Formatted contents of 4C input .dat file
    """

    # check if all wanted formatted sections are currently supported
    for section in format_sections:
        if section not in FORMAT_SECTIONS.keys():
            raise ValueError(
                "A given formatted section is currently not supported!"
            )

    dat_sections = split_into_sections(file_content)
    formatted_sections = []

    for dat_section in dat_sections:
        header, lines = dat_section
        # check if section should be formatted
        if any(format_section in header for format_section in format_sections):
            formatted_lines = format_section(
                lines, FORMAT_SECTIONS[header.strip("-")]
            )
            formatted_sections.append((header, formatted_lines))
        else:
            formatted_sections.append(dat_section)

    # combine sections back into a single list of formatted lines
    formatted_content = []
    for section in formatted_sections:
        formatted_content.append(section[0])
        formatted_content.extend(section[1])

    return formatted_content


def format_dat_file(
    dat_file_path: str,
    target_path: str,
    format_sections: list,
) -> None:
    """Format .dat file contents and save to file according to the provided
    format_sections.

    Args:
        dat_file_path (str): Path to the 4C input .dat file
        format_sections (list): List of sections titles which should be
            formatted
        output_file_path (Optional[str], optional): Optional output file path.
            If none is provided, input file is overwritten
    """

    with open(dat_file_path, "r") as file:
        file_content = file.readlines()

    formatted_content = format_content(file_content, format_sections)

    with open(target_path, "w") as file:
        file.writelines("\n".join(formatted_content) + "\n")


def main() -> None:
    """Parse arguments and call format_dat_file with config."""

    parser = argparse.ArgumentParser(
        description=("Utility to format 4C input .dat files.")
    )
    parser.add_argument(
        "--dat_file_path",
        "-dfp",
        help="Path to the 4C .dat input file.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output_file_path",
        "-ofp",
        help="Path to the output file. If none is provided, old file is "
        "overwritten.",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--format_sections",
        "-fs",
        help="Sections which will be formatted.",
        type=str,
        default=[
            "DESIGN LINE BEAM POTENTIAL CHARGE CONDITIONS",
            "DNODE-NODE TOPOLOGY",
            "DLINE-NODE TOPOLOGY",
            "NODE COORDS",
            "STRUCTURE ELEMENTS",
        ],
        nargs="+",
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
        description="4C input .dat file formatter",
    )

    log_full_width("Formatting started")

    log.info("Path to 4C .dat input file:")
    log.info(f"     {args.dat_file_path}")
    log.info("")

    if args.output_file_path is not None:
        target_path = args.output_file_path
    else:
        target_path = args.dat_file_path

    format_dat_file(args.dat_file_path, target_path, args.format_sections)

    log.info("Formatted 4C .dat input file written to:")
    log.info(f"     {target_path}")

    log_full_width("Formatting finished")


if __name__ == "__main__":  # pragma: no cover

    main()
    exit(0)
