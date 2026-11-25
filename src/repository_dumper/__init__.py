from importlib.metadata import PackageNotFoundError, version

from repository_dumper.core import (
    DirectoryNode,
    DirectoryWalker,
    ExportWriter,
    ProjectSourceExporter,
)

try:
    __version__ = version("repository-dumper")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"

__all__ = [
    "__version__",
    "DirectoryNode",
    "DirectoryWalker",
    "ExportWriter",
    "ProjectSourceExporter",
]