from typing import Union

import argparse
import os
from repository_dumper.core import ProjectSourceExporter


DEFAULT__OUTPUT_FILENAME: str = "exported_source_project.txt"


def main() -> None:
    args_parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description = "Recursively scans a project directory, extracts all source files, and writes them into a single text file with file paths as headers",
        add_help = True
    )

    args_parser.add_argument(
        "-r",
        "--root_dir",
        dest = "root_dir",
        action = "store",
        type = str,
        required = True,
        help = "Root directory to scan" 
    )
    
    args_parser.add_argument(
        "-o",
        "--output_file",
        dest = "output_file",
        action = "store",
        type = str,
        required = False,
        help = "Output file path"
    )

    args_parser.add_argument(
        "-e",
        "--allowed_extensions",
        dest = "allowed_extensions",
        action = "store",
        type = str,
        nargs = "+",
        required = False,
        help = "Allowed file extension (e.g. .py, .java, ...)"
    )

    args_parser.add_argument(
        "--exclude_extensions",
        dest = "exclude_extensions",
        action = "store",
        type = str,
        nargs = "+",
        required = False,
        help = "File extensions to exclude (e.g. .pyc, .md)"
    )

    args_parser.add_argument(
        "--exclude_files",
        dest = "exclude_files",
        action = "store",
        type = str,
        nargs = "+",
        required = False,
        help = "Specific file names to exclude (e.g. secrets.json)"
    )

    args_parser.add_argument(
        "--exclude_folders",
        dest = "exclude_folders",
        action = "store",
        type = str,
        nargs = "+",
        required = False,
        help = "Specific folder names to exclude (e.g. .git, node_modules)"
    )

    args: argparse.Namespace = args_parser.parse_args()

    output_file: Union[str, None] = args.output_file
    if (not output_file):
        output_file = os.path.join(args.root_dir, DEFAULT__OUTPUT_FILENAME)

    project_source_explorer: ProjectSourceExporter = ProjectSourceExporter(args.root_dir, output_file)
    
    project_source_explorer.run(
        allowed_extensions = args.allowed_extensions,
        exclude_extensions = args.exclude_extensions,
        exclude_files = args.exclude_files,
        exclude_folders = args.exclude_folders
    )