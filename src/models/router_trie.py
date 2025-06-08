class RouterTrieNode:

    def __init__(self):
        self.children = {}
        self.is_terminal = False


class RouterTrie:
    def __init__(self):
        self.root = RouterTrieNode()

    def insert(self, path):
        path_parts = path.split("/")
        node = self.root

        for part in path_parts:
            normalised = "/" if part == "" else "{id}" if part[0] == "{" else part

            if normalised not in node.children:
                node.children[normalised] = RouterTrieNode()

            node = node.children[normalised]
        node.is_terminal = True

    def search(self, path):
        path_parts = path.split("/")
        node = self.root
        for part in path_parts:
            normalised = "/" if part == "" else part

            if normalised not in node.children:
                node = node.children[normalised]
                continue

            if "{id}" in node.children:
                node = node.children["{id}"]
                continue

            return False
        return node.is_terminal

    def __str__(self):
        def dfs(node, depth=0):
            result = ""
            for key in sorted(node.children):
                prefix = "    " * depth + "|__ "
                result += f"{prefix}{key}\n"
                result += dfs(node.children[key], depth + 1)
            return result

        return dfs(self.root)
