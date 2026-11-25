from importlib.metadata import PackageNotFoundError, version

from repository_dumper.core import (
    DEFAULT_ENCODING,
    DEFAULT_OUTPUT_FILENAME,
    DirectoryNode,
    DirectoryWalker,
    ExportWriter,
    IgnoreRuleMatcher,
    ProjectSourceExporter,
)

try:
    __version__ = version("repository-dumper")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"

__all__ = [
    "__version__",
    "DEFAULT_ENCODING",
    "DEFAULT_OUTPUT_FILENAME",
    "DirectoryNode",
    "DirectoryWalker",
    "ExportWriter",
    "IgnoreRuleMatcher",
    "ProjectSourceExporter",
]