from pathlib import Path

import pytest

from repository_dumper import DEFAULT_OUTPUT_FILENAME
from repository_dumper.cli import build_parser, main


def test_parse_long_flags() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "--root-dir",
            ".",
            "--output-file",
            "out.txt",
            "--allowed-extensions",
            "py",
            "md",
            "--exclude-extensions",
            "pyc",
            "--exclude-files",
            "secrets.json",
            "--exclude-folders",
            ".git",
            "node_modules",
            "--exclude-from-file",
            ".gitignore",
        ]
    )

    assert args.root_dir == "."
    assert args.output_file == "out.txt"
    assert args.allowed_extensions == ["py", "md"]
    assert args.exclude_extensions == ["pyc"]
    assert args.exclude_files == ["secrets.json"]
    assert args.exclude_folders == [".git", "node_modules"]
    assert args.exclude_from_file == ".gitignore"


def test_parse_short_flags_and_defaults() -> None:
    parser = build_parser()
    args = parser.parse_args(["-r", "src", "-o", "dump.txt", "-e", "py", "ts"])

    assert args.root_dir == "src"
    assert args.output_file == "dump.txt"
    assert args.allowed_extensions == ["py", "ts"]
    assert args.exclude_extensions is None
    assert args.exclude_files is None
    assert args.exclude_folders is None
    assert args.exclude_from_file is None


def test_parse_defaults_when_no_args_provided() -> None:
    parser = build_parser()
    args = parser.parse_args([])

    assert args.root_dir == "."
    assert args.output_file is None
    assert args.allowed_extensions is None
    assert args.exclude_extensions is None
    assert args.exclude_files is None
    assert args.exclude_folders is None
    assert args.exclude_from_file is None


def test_main_defaults_to_current_working_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "app.py").write_text("print('cwd')\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    main([])

    output_file = tmp_path / DEFAULT_OUTPUT_FILENAME
    assert output_file.exists()
    result = output_file.read_text(encoding="utf-8")
    assert "print('cwd')" in result
    assert DEFAULT_OUTPUT_FILENAME not in result


def test_main_runs_with_all_flags(tmp_path: Path) -> None:
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    (repo_dir / "keep.py").write_text("print('ok')\n", encoding="utf-8")
    (repo_dir / "skip.md").write_text("# skip\n", encoding="utf-8")
    (repo_dir / "secret.py").write_text("SECRET = 1\n", encoding="utf-8")
    (repo_dir / "ignored_by_rule.py").write_text("RULE_IGNORED = 1\n", encoding="utf-8")

    ignored_dir = repo_dir / "ignored_dir"
    ignored_dir.mkdir()
    (ignored_dir / "nested.py").write_text("print('no')\n", encoding="utf-8")

    ignore_file = tmp_path / ".dumpignore"
    ignore_file.write_text("ignored_by_rule.py\n", encoding="utf-8")

    output_file = tmp_path / "snapshot.txt"

    main(
        [
            "--root-dir",
            str(repo_dir),
            "--output-file",
            str(output_file),
            "--allowed-extensions",
            "py",
            "md",
            "--exclude-extensions",
            "md",
            "--exclude-files",
            "secret.py",
            "--exclude-folders",
            "ignored_dir",
            "--exclude-from-file",
            str(ignore_file),
        ]
    )

    result = output_file.read_text(encoding="utf-8")
    assert "print('ok')" in result
    assert "# skip" not in result
    assert "SECRET = 1" not in result
    assert "RULE_IGNORED = 1" not in result
    assert "print('no')" not in result


def test_main_exits_with_error_on_missing_ignore_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing_file = tmp_path / "missing.gitignore"

    with pytest.raises(SystemExit) as exc_info:
        main(["-r", str(tmp_path), "--exclude-from-file", str(missing_file)])

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Ignore file not found" in captured.err