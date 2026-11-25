from typing import Optional, Sequence
import argparse
import sys

from repository_dumper.core import DEFAULT_OUTPUT_FILENAME, ProjectSourceExporter


def build_parser() -> argparse.ArgumentParser:
    args_parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=(
            "Recursively scans a project directory, extracts all source files, "
            "and writes them into a single text file with file paths as headers"
        ),
        add_help=True,
    )

    args_parser.add_argument(
        "-r",
        "--root-dir",
        dest="root_dir",
        action="store",
        type=str,
        default=".",
        required=False,
        help="Root directory to scan (defaults to the current working directory '.')",
    )

    args_parser.add_argument(
        "-o",
        "--output-file",
        dest="output_file",
        action="store",
        type=str,
        required=False,
        help=f"Output file path (defaults to '<root_dir>/{DEFAULT_OUTPUT_FILENAME}')",
    )

    args_parser.add_argument(
        "-e",
        "--allowed-extensions",
        dest="allowed_extensions",
        action="store",
        type=str,
        nargs="+",
        required=False,
        help="Allowed file extensions without leading dots (e.g. py java; leading dots also accepted)",
    )

    args_parser.add_argument(
        "--exclude-extensions",
        dest="exclude_extensions",
        action="store",
        type=str,
        nargs="+",
        required=False,
        help="File extensions to exclude without leading dots (e.g. pyc md; leading dots also accepted)",
    )

    args_parser.add_argument(
        "--exclude-files",
        dest="exclude_files",
        action="store",
        type=str,
        nargs="+",
        required=False,
        help="Specific file names to exclude (e.g. secrets.json)",
    )

    args_parser.add_argument(
        "--exclude-folders",
        dest="exclude_folders",
        action="store",
        type=str,
        nargs="+",
        required=False,
        help="Specific folder names to exclude (e.g. .git, node_modules)",
    )

    args_parser.add_argument(
        "--exclude-from-file",
        dest="exclude_from_file",
        action="store",
        type=str,
        required=False,
        help=(
            "Path to a .gitignore-style file specifying patterns to exclude "
            "(if the filename is '.gitignore', the '.git' directory is excluded automatically)"
        ),
    )

    return args_parser


def main(argv: Optional[Sequence[str]] = None) -> None:
    args_parser: argparse.ArgumentParser = build_parser()
    args: argparse.Namespace = args_parser.parse_args(argv)

    project_source_exporter: ProjectSourceExporter = ProjectSourceExporter(
        args.root_dir, args.output_file
    )

    try:
        project_source_exporter.run(
            allowed_extensions=args.allowed_extensions,
            exclude_extensions=args.exclude_extensions,
            exclude_files=args.exclude_files,
            exclude_folders=args.exclude_folders,
            exclude_from_file=args.exclude_from_file,
        )
    except (FileNotFoundError, IsADirectoryError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)