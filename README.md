# RepositoryDumper

CLI tool to export a code repository into a single structured text snapshot.

It recursively scans a project directory and writes all source files into one output file with clearly structured headers, making it useful for code sharing, analysis, backups, and LLM context ingestion.

---

## Features

- Recursive directory traversal
- File filtering by allowed extensions
- Exclusion of specific extensions, files, and folders
- `.gitignore`-style exclusion file support (with automatic `.git/` exclusion for `.gitignore`)
- Structured snapshot output format
- Lightweight CLI tool
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
repo-dump -r . -e py js ts
```

Exclude specific extensions, folders, and files:

```bash
repo-dump -r . --exclude_extensions pyc md --exclude_folders .git node_modules --exclude_files secrets.json
```

Exclude paths using a `.gitignore` file (automatically excludes `.git/` as well):

```bash
repo-dump -r . --exclude-from-file .gitignore
```

Exclude paths using a custom ignore file combined with extension filters:

```bash
repo-dump -r . -e py toml --exclude-from-file .dumpignore -o snapshot.txt
```

---

## Output Format

Each file is written in the following structured format:

```text
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
* Extension filters (`-e`, `--exclude_extensions`) are case-insensitive and accept dotless extensions (e.g., `py java`) as well as dot-prefixed ones (e.g., `.py .java`)
* `.gitignore`-style ignore files support comments (`#`), blank lines, globs, directory patterns, root-anchored paths, and negation (`!`)
* Output is appended in a structured sequential format