from pathlib import Path

from repository_dumper import ProjectSourceExporter


def test_exporter_writes_allowed_files(tmp_path: Path) -> None:
    src_file = tmp_path / "hello.py"
    src_file.write_text("print('hello')\n", encoding="utf-8")

    ignored_file = tmp_path / "notes.md"
    ignored_file.write_text("# ignored\n", encoding="utf-8")

    output_file = tmp_path / "snapshot.txt"

    exporter = ProjectSourceExporter(str(tmp_path), str(output_file))
    exporter.run(allowed_extensions=[".py"])

    result = output_file.read_text(encoding="utf-8")
    assert "hello.py" in result
    assert "print('hello')" in result
    assert "notes.md" not in result