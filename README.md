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

`RepositoryDumper` is best installed in an isolated environment using **`pipx`** or **`uv`**. This makes `repo-dump` available globally from any directory and avoids system Python conflicts (such as PEP 668 `externally-managed-environment` errors on Linux and macOS).

**Prerequisites:** Python 3.10+ and Git.

### Option 1: Install with `pipx` (Recommended)

1. Install `pipx` if you don't already have it:

   * **Debian / Ubuntu / Mint:**
     ```bash
     sudo apt update && sudo apt install -y pipx
     pipx ensurepath
     ```
   * **Fedora / RHEL:**
     ```bash
     sudo dnf install -y pipx
     pipx ensurepath
     ```
   * **Arch / Manjaro / Garuda:**
     ```bash
     sudo pacman -S python-pipx
     pipx ensurepath
     ```
   * **macOS (Homebrew):**
     ```bash
     brew install pipx
     pipx ensurepath
     ```
   * **Windows (PowerShell):**
     ```powershell
     py -m pip install --user pipx
     py -m pipx ensurepath
     ```

   *(Restart your terminal after running `pipx ensurepath` so your `PATH` updates.)*

2. Install `repo-dump` directly from GitHub:

   ```bash
   pipx install git+[https://github.com/MassimilianoMorisi/RepositoryDumper.git](https://github.com/MassimilianoMorisi/RepositoryDumper.git)
   ```

### Option 2: Install with `uv`

If you use [uv](https://docs.astral.sh/uv/) (which can also manage Python 3.10+ automatically):

```bash
uv tool install git+[https://github.com/MassimilianoMorisi/RepositoryDumper.git](https://github.com/MassimilianoMorisi/RepositoryDumper.git)
```

Or run `repo-dump` once without installing it permanently:

```bash
uvx --from git+[https://github.com/MassimilianoMorisi/RepositoryDumper.git](https://github.com/MassimilianoMorisi/RepositoryDumper.git) repo-dump
```

### Verify Installation

```bash
repo-dump --help
```

---

## Upgrading

* **With `pipx`:**
  ```bash
  pipx install --force git+[https://github.com/MassimilianoMorisi/RepositoryDumper.git](https://github.com/MassimilianoMorisi/RepositoryDumper.git)
  ```
* **With `uv`:**
  ```bash
  uv tool upgrade repository-dumper
  ```

---

## Uninstallation

* **With `pipx`:**
  ```bash
  pipx uninstall repository-dumper
  ```
* **With `uv`:**
  ```bash
  uv tool uninstall repository-dumper
  ```

---

## Usage

Basic usage (scans the current working directory and writes to `./repo_dump.txt` by default):

```bash
repo-dump
```

Specify a target root directory:

```bash
repo-dump -r path/to/project
```

Specify output file:

```bash
repo-dump -o snapshot.txt
```

Filter by allowed file extensions:

```bash
repo-dump -e py js ts
```

Exclude specific extensions, folders, and files:

```bash
repo-dump --exclude-extensions pyc md --exclude-folders .git node_modules --exclude-files secrets.json
```

Exclude paths using a `.gitignore` file (automatically excludes `.git/` as well):

```bash
repo-dump --exclude-from-file .gitignore
```

Exclude paths using a custom ignore file combined with extension filters:

```bash
repo-dump -e py toml --exclude-from-file .dumpignore -o snapshot.txt
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

## Development

To contribute or run the test suite locally, clone the repository into an isolated virtual environment:

```bash
git clone [https://github.com/MassimilianoMorisi/RepositoryDumper.git](https://github.com/MassimilianoMorisi/RepositoryDumper.git)
cd RepositoryDumper
python -m venv .venv
```

Activate the virtual environment:

* **Linux / macOS (Bash/Zsh):** `source .venv/bin/activate`
* **Linux / macOS (Fish):** `source .venv/bin/activate.fish`
* **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`

Install in editable mode with development dependencies and run tests:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

---

## Technical Notes

* Files are read using UTF-8 encoding
* Binary or unreadable files are skipped safely
* Directory traversal is recursive and deterministic
* When `-r` / `--root-dir` is omitted, the current working directory (`.`) is scanned by default
* When `-o` / `--output-file` is omitted, the dump is written to `<root_dir>/repo_dump.txt` and automatically excluded from being dumped into itself
* Extension filters (`-e` / `--allowed-extensions`, `--exclude-extensions`) are case-insensitive and accept dotless extensions (e.g., `py java`) as well as dot-prefixed ones (e.g., `.py .java`)
* `.gitignore`-style ignore files support comments (`#`), blank lines, globs, directory patterns, root-anchored paths, and negation (`!`)
* Output is appended in a structured sequential format