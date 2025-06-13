from typing import Callable, Any, Dict, Optional, Tuple
from src.models.http_methods import HTTPMethod


class RouterTrieNode:
    def __init__(self):
        self.children = {}
        self.is_terminal = False
        self.handler_method_type_pair = {}


class RouterTrie:
    def __init__(self):
        """Initializes the router trie with an empty root node."""
        self.root = RouterTrieNode()

    def insert(self, path: str, handler: Callable[..., Any], method_type: HTTPMethod):
        """
        Inserts a route path into the trie.
        """
        path_parts = path.split("/")
        node = self.root

        for part in path_parts:
            normalised = "/" if part == "" else part

            if normalised not in node.children:
                node.children[normalised] = RouterTrieNode()

            node = node.children[normalised]

        node.is_terminal = True
        node.handler_method_type_pair[method_type] = handler

    def search(
        self, path: str, method_type: HTTPMethod
    ) -> Optional[Tuple[Callable, Dict[str, str]]]:
        """
        Searches for a complete route path in the trie and returns callable and args.
        """
        path_parts = path.split("/")
        node = self.root
        dynamic_keys = {}

        for part in path_parts:
            normalised = "/" if part == "" else part

            if normalised in node.children:
                node = node.children[normalised]
                continue

            dynamic_key = next(
                (key for key in node.children if key.startswith("{")), None
            )
            if dynamic_key:
                dynamic_keys[dynamic_key[1:-1]] = normalised
                node = node.children[dynamic_key]
                continue

            return None
        return (
            (node.handler_method_type_pair[method_type], dynamic_keys)
            if method_type in list(node.handler_method_type_pair.keys())
            else None
        )

    def __str__(self) -> str:
        """
        Returns a visual string representation of the trie structure.
        """

        def dfs(node, depth=0):
            result = ""
            for key in sorted(node.children):
                prefix = "    " * depth + "|__ "
                result += f"{prefix}{key}\n"
                result += dfs(node.children[key], depth + 1)
            return result

        return dfs(self.root)
