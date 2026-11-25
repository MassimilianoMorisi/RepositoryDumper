from pathlib import Path

import pytest

from repository_dumper import (
    DEFAULT_ENCODING,
    DEFAULT_OUTPUT_FILENAME,
    ProjectSourceExporter,
)


def test_exporter_writes_allowed_files(tmp_path: Path) -> None:
    src_file = tmp_path / "hello.py"
    src_file.write_text("print('hello')\n", encoding="utf-8")

    ignored_file = tmp_path / "notes.md"
    ignored_file.write_text("# ignored\n", encoding="utf-8")

    output_file = tmp_path / "snapshot.txt"

    exporter = ProjectSourceExporter(str(tmp_path), str(output_file))
    exporter.run(allowed_extensions=["py"])

    result = output_file.read_text(encoding="utf-8")
    assert "hello.py" in result
    assert "print('hello')" in result
    assert "notes.md" not in result


def test_default_output_filename_and_self_exclusion(tmp_path: Path) -> None:
    assert DEFAULT_ENCODING == "utf-8"
    assert DEFAULT_OUTPUT_FILENAME == "repo_dump.txt"

    (tmp_path / "notes.txt").write_text("plain-text-note\n", encoding="utf-8")
    default_output = tmp_path / DEFAULT_OUTPUT_FILENAME
    default_output.write_text("stale-previous-dump\n", encoding="utf-8")

    exporter = ProjectSourceExporter(str(tmp_path))
    exporter.run(allowed_extensions=["txt"])

    assert default_output.exists()
    result = default_output.read_text(encoding="utf-8")
    assert "plain-text-note" in result
    assert "stale-previous-dump" not in result
    assert DEFAULT_OUTPUT_FILENAME not in result


def test_extensions_normalization_and_backward_compatibility(tmp_path: Path) -> None:
    (tmp_path / "Main.JAVA").write_text("class Main {}\n", encoding="utf-8")
    (tmp_path / "script.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "index.ts").write_text("export const a = 1;\n", encoding="utf-8")
    (tmp_path / "README.MD").write_text("# Docs\n", encoding="utf-8")
    (tmp_path / "skip.pyc").write_text("bytecode\n", encoding="utf-8")

    output_file = tmp_path / "snapshot.txt"
    exporter = ProjectSourceExporter(str(tmp_path), str(output_file))
    exporter.run(
        allowed_extensions=[" JAVA ", ".py", "..TS", "md"],
        exclude_extensions=[".MD", " pyc "],
    )

    result = output_file.read_text(encoding="utf-8")
    assert "class Main {}" in result
    assert "x = 1" in result
    assert "export const a = 1;" in result
    assert "# Docs" not in result
    assert "bytecode" not in result


def test_extension_matching_edge_cases(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("py-content\n", encoding="utf-8")
    (tmp_path / "mypy").write_text("no-ext-mypy\n", encoding="utf-8")
    (tmp_path / "py").write_text("no-ext-py\n", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("dotfile-gitignore\n", encoding="utf-8")
    (tmp_path / ".py").write_text("dotfile-py\n", encoding="utf-8")
    (tmp_path / ".env.local").write_text("dotfile-with-ext\n", encoding="utf-8")
    (tmp_path / "app.ts").write_text("plain-ts\n", encoding="utf-8")
    (tmp_path / "types.d.ts").write_text("decl-ts\n", encoding="utf-8")
    (tmp_path / "archive.tar.gz").write_text("tar-gz-content\n", encoding="utf-8")

    output_file = tmp_path / "snapshot.txt"
    exporter = ProjectSourceExporter(str(tmp_path), str(output_file))
    exporter.run(
        allowed_extensions=["py", "gitignore", "local", "ts", "tar.gz"],
        exclude_extensions=["d.ts"],
    )

    result = output_file.read_text(encoding="utf-8")
    assert "py-content" in result
    assert "dotfile-with-ext" in result
    assert "plain-ts" in result
    assert "tar-gz-content" in result

    assert "no-ext-mypy" not in result
    assert "no-ext-py" not in result
    assert "dotfile-gitignore" not in result
    assert "dotfile-py" not in result
    assert "decl-ts" not in result


def test_invalid_dot_only_allowed_extensions_matches_nothing(tmp_path: Path) -> None:
    (tmp_path / "hello.py").write_text("print('hello')\n", encoding="utf-8")

    output_file = tmp_path / "snapshot.txt"
    exporter = ProjectSourceExporter(str(tmp_path), str(output_file))
    exporter.run(allowed_extensions=[".", "   "])

    assert output_file.read_text(encoding="utf-8") == ""


def test_exclude_from_gitignore_rules_and_auto_git_exclusion(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "debug.log").write_text("log data\n", encoding="utf-8")
    (tmp_path / "root_only.txt").write_text("root\n", encoding="utf-8")

    nested_dir = tmp_path / "sub"
    nested_dir.mkdir()
    (nested_dir / "root_only.txt").write_text("nested kept\n", encoding="utf-8")

    build_dir = tmp_path / "build"
    build_dir.mkdir()
    (build_dir / "artifact.py").write_text("generated\n", encoding="utf-8")

    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "temp.log").write_text("skip\n", encoding="utf-8")
    (logs_dir / "important.log").write_text("keep me\n", encoding="utf-8")

    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("[core]\n", encoding="utf-8")

    gitignore = tmp_path / ".gitignore"
    gitignore.write_text(
        "\n"
        "# Comments and blank lines should be ignored\n"
        "*.log\n"
        "!logs/important.log\n"
        "build/\n"
        "/root_only.txt\n",
        encoding="utf-8",
    )

    output_file = tmp_path / "snapshot.txt"
    exporter = ProjectSourceExporter(str(tmp_path), str(output_file))
    exporter.run(exclude_from_file=gitignore)

    result = output_file.read_text(encoding="utf-8")
    assert "app.py" in result
    assert "nested kept" in result
    assert "keep me" in result
    assert "debug.log" not in result
    assert "temp.log" not in result
    assert "artifact.py" not in result
    assert "[core]" not in result
    assert "root\n" not in result


def test_custom_ignore_file_does_not_auto_exclude_git(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("print(1)\n", encoding="utf-8")
    (tmp_path / "secret.txt").write_text("super-secret-value\n", encoding="utf-8")

    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")

    custom_ignore = tmp_path / ".dumpignore"
    custom_ignore.write_text("secret.txt\n", encoding="utf-8")

    output_file = tmp_path / "snapshot.txt"
    exporter = ProjectSourceExporter(str(tmp_path), str(output_file))
    exporter.run(exclude_from_file=custom_ignore)

    result = output_file.read_text(encoding="utf-8")
    assert "main.py" in result
    assert "ref: refs/heads/main" in result
    assert "super-secret-value" not in result
    assert f"secret.txt\n{'=' * 50}" not in result


def test_exclude_from_file_combines_with_existing_filters(tmp_path: Path) -> None:
    (tmp_path / "keep.py").write_text("ok = True\n", encoding="utf-8")
    (tmp_path / "skip_by_flag.py").write_text("flag\n", encoding="utf-8")
    (tmp_path / "skip_by_ignore.py").write_text("ignore\n", encoding="utf-8")
    (tmp_path / "readme.md").write_text("docs\n", encoding="utf-8")

    ignore_file = tmp_path / ".dumpignore"
    ignore_file.write_text("skip_by_ignore.py\n", encoding="utf-8")

    output_file = tmp_path / "snapshot.txt"
    exporter = ProjectSourceExporter(str(tmp_path), str(output_file))
    exporter.run(
        allowed_extensions=["py"],
        exclude_files=["skip_by_flag.py"],
        exclude_from_file=ignore_file,
    )

    result = output_file.read_text(encoding="utf-8")
    assert "keep.py" in result
    assert "skip_by_flag.py" not in result
    assert "skip_by_ignore.py" not in result
    assert "readme.md" not in result


def test_missing_or_directory_ignore_file_raises_without_creating_output(tmp_path: Path) -> None:
    output_file = tmp_path / "snapshot.txt"
    exporter = ProjectSourceExporter(str(tmp_path), str(output_file))

    with pytest.raises(FileNotFoundError, match="Ignore file not found"):
        exporter.run(exclude_from_file=tmp_path / "does_not_exist.gitignore")
    assert not output_file.exists()

    with pytest.raises(IsADirectoryError, match="is a directory"):
        exporter.run(exclude_from_file=tmp_path)
    assert not output_file.exists()