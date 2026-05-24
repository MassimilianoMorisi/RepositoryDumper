"""
RepositoryDumper core engine
"""

from dataclasses import dataclass
from typing import List, Optional, Protocol, Sequence, Union
from pathlib import Path
import os

DEFAULT_ENCODING: str = "utf-8"

class FileValidator(Protocol):

    def __call__(self, path) -> bool:
        ...

@dataclass
class DirectoryNode:
    name: str
    path: str
    is_file: bool
    sub_items: Union[List["DirectoryNode"], None] = None


class NodeVisitor(Protocol):

    def __call__(self, node: DirectoryNode) -> None:
        ...


class DirectoryWalker:

    def __init__(self, root_dir: str, is_file_valid: Optional[FileValidator]) -> None:
        self.__root_dir: str = root_dir
        self.__root_node: Union[DirectoryNode, None] = None
        self.__is_file_valid: FileValidator = is_file_valid or (lambda path: True)
        self.__node_visitor: NodeVisitor = lambda node: None

    def __get_directory_tree_recursively(self, path: str) -> Union[DirectoryNode, None]:
        is_file: bool = os.path.isfile(path)
        
        if (is_file):
            if (self.__is_file_valid(path)):
                return DirectoryNode(os.path.basename(path), path, is_file)
        
            return None

        directory_name: str = os.path.basename(path)
        sub_items: List[DirectoryNode] = list()
        for entry in os.listdir(path):
            entry_path: str = os.path.join(path, entry)
            item: Union[DirectoryNode, None] = self.__get_directory_tree_recursively(entry_path)
            if (item):
                sub_items.append(item)
        
        return DirectoryNode(directory_name, path, False, sub_items)

    def __load_directory_tree(self) -> None:
        if (not self.__root_node):
            self.__root_node = self.__get_directory_tree_recursively(self.__root_dir)

    def __walk_recursively(self, node: DirectoryNode) -> None:
        if (node.is_file):
            self.__node_visitor(node)

            return
        
        for sub_node in (node.sub_items or []):
            self.__walk_recursively(sub_node)

        self.__node_visitor(node)

    def walk(self, visitor: NodeVisitor) -> None:
        self.__load_directory_tree()
        self.__node_visitor = visitor

        if (self.__root_node):
            self.__walk_recursively(self.__root_node)


class ExportWriter:
    __OUTER_BORDER: str = "-" * 80
    __INNER_BORDER: str = "=" * 50

    @classmethod
    def __extract_path_from_root(cls, root_dir_name: str, absolute_path: str) -> str:
        path: Path = Path(absolute_path)

        try:
            start_index: int = path.parts.index(root_dir_name)

        except ValueError:
            return absolute_path

        path_segments: Sequence[str] = path.parts[start_index:]
        relative_path: Path = Path(*path_segments)

        return relative_path.as_posix()

    @classmethod
    def __get_formatted_block(cls, root_dir_name: str, filepath: str) -> Union[str, None]:
        if (not os.path.isfile(filepath)):
            return None
        
        try:
            content: str = Path(filepath).read_text(encoding = DEFAULT_ENCODING)

        except Exception:
            return None

        return (
            f"{cls.__OUTER_BORDER}\n"
            f"\n"
            f"{cls.__INNER_BORDER}\n"
            f"{cls.__extract_path_from_root(root_dir_name, filepath)}\n"
            f"{cls.__INNER_BORDER}\n"
            f"\n"
            f"{content}\n"
            f"{cls.__OUTER_BORDER}\n"
        )

    @classmethod
    def append_formatted_data_to_file(cls, output_file: str, root_dir_name: str, filepath: str) -> None:
        formatted_content: Union[str, None] = cls.__get_formatted_block(root_dir_name, filepath) 
        if (not formatted_content):
            return
        
        with open(output_file, "at", encoding = DEFAULT_ENCODING) as file:
            file.write(formatted_content)
    
    
class ProjectSourceExporter:

    def __init__(self, root_dir: str, output_file: str) -> None:
        self.__root_dir: str = root_dir
        self.__output_file: str = output_file
        self.__allowed_extensions: Union[List[str], None] = None

        self.__directory_walker: DirectoryWalker = DirectoryWalker(self.__root_dir, self.__is_file_valid)

    def __is_file_valid(self, path: str) -> bool:
        if (not self.__allowed_extensions):
            return True

        return any(path.endswith(extension) for extension in self.__allowed_extensions)

    def __handle_node(self, node: DirectoryNode) -> None:
        if (node.is_file):
            ExportWriter.append_formatted_data_to_file(self.__output_file, self.__root_dir, node.path)

    def run(self, allowed_extensions: Optional[List[str]]) -> None:
        self.__allowed_extensions = allowed_extensions

        open(self.__output_file, "w", encoding = DEFAULT_ENCODING).close()

        self.__directory_walker.walk(self.__handle_node)
