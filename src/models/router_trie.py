from typing import Callable, Any
from models.http_methods import HTTPMethod


class RouterTrieNode:
    def __init__(self):
        self.children = {}
        self.is_terminal = False
        self.handler = None
        self.method_type = None


class RouterTrie:
    def __init__(self):
        """Initializes the router trie with an empty root node."""
        self.root = RouterTrieNode()

    def insert(self, path: str, handler: Callable[..., Any], method_type: HTTPMethod):
        """
        Inserts a route path into the trie.

        Args:
            path (str): The URL path (e.g., "/users/{id}").
            handler (Callable): The function that handles the route.
            method_type (HTTPMethod): The HTTP method associated with this route.
        """
        path_parts = path.split("/")
        node = self.root

        for part in path_parts:
            normalised = "/" if part == "" else "{id}" if part[0] == "{" else part

            if normalised not in node.children:
                node.children[normalised] = RouterTrieNode()

            node = node.children[normalised]

        node.is_terminal = True
        node.handler = handler
        node.method_type = method_type

    def search(self, path: str) -> bool:
        """
        Searches for a complete route path in the trie.

        Args:
            path (str): The path to search (e.g., "/users/123").

        Returns:
            bool: True if a matching path exists, otherwise False.
        """
        path_parts = path.split("/")
        node = self.root

        for part in path_parts:
            normalised = "/" if part == "" else part

            if normalised in node.children:
                node = node.children[normalised]
            elif "{id}" in node.children:
                node = node.children["{id}"]
            else:
                return False

        return node.is_terminal

    def __str__(self) -> str:
        """
        Returns a visual string representation of the trie structure.

        Returns:
            str: A tree-like formatted string of the trie.
        """

        def dfs(node, depth=0):
            result = ""
            for key in sorted(node.children):
                prefix = "    " * depth + "|__ "
                result += f"{prefix}{key}\n"
                result += dfs(node.children[key], depth + 1)
            return result

        return dfs(self.root)
