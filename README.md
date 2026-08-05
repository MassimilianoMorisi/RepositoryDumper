# RepositoryDumper

CLI tool to export a code repository into a single structured text snapshot.

It recursively scans a project directory and writes all source files into one output file with clearly structured headers, making it useful for code sharing, analysis, backups, and LLM context ingestion.

---

## Features

- Recursive directory traversal
- File filtering by allowed extensions
- Exclusion of specific extensions, files, and folders
- Structured snapshot output format
- Lightweight CLI tool (no dependencies)
- Stable formatting for programmatic parsing and LLM usage

---

## Installation

Clone the repository:

```bash
git clone [https://github.com/MassimilianoMorisi/RepositoryDumper.git](https://github.com/MassimilianoMorisi/RepositoryDumper.git)
cd RepositoryDumper

```

Install in editable mode:

```bash
pip install -e .

```

---

## Usage

Basic usage:

```bash
repo-dump -r .

```

Specify output file:

```bash
repo-dump -r . -o snapshot.txt

```

Filter by allowed file extensions:

```bash
repo-dump -r . -e .py .js .ts

```

Exclude specific extensions, folders, and files:

```bash
repo-dump -r . --exclude_extensions .pyc .md --exclude_folders .git node_modules --exclude_files secrets.json

```

---

## Output Format

Each file is written in the following structured format:

```
--------------------------------------------------------------------------------

==================================================
path/to/file.py
==================================================

<file content>
--------------------------------------------------------------------------------

```

* The outer dashed line separates files
* The inner equals lines highlight the file path
* Spacing lines improve readability and parsing stability

---

## Example Use Cases

* Exporting a repository for AI / LLM context
* Code review and sharing snapshots
* Lightweight project backups
* Repository inspection and auditing
* Generating static representations of codebases

---

## Technical Notes

* Files are read using UTF-8 encoding
* Binary or unreadable files are skipped safely
* Directory traversal is recursive and deterministic
* Output is appended in a structured sequential format

---