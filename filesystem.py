"""
filesystem.py - Virtual Filesystem for TerminalOS
--------------------------------------------------
Simulates an in-memory filesystem using nested Python dictionaries.
  - Folders are represented as dicts
  - Files are represented as strings (their text content)
No real disk access is performed anywhere in this module.
"""


class FileSystem:
    """
    In-memory virtual filesystem.

    Tree structure example:
    {
        "home": {
            "alice": {
                "notes.txt": "Hello!",
                "projects": {}
            }
        },
        "etc": {
            "motd.txt": "Welcome!"
        },
        "tmp": {}
    }
    """

    def __init__(self):
        # ── Default filesystem tree ──────────────────────────────────────
        self.tree = {
            "home": {},          # user home directories live here
            "etc": {
                "motd.txt": "Have a productive day on TerminalOS v1.0!"
            },
            "tmp": {},           # scratch space
            "bin": {},           # placeholder – commands live in code, not here
        }

        # Current path stored as a list of directory names.
        # e.g. ["home", "alice"] represents /home/alice
        self.current_path: list[str] = []

    # ────────────────────────────────────────────────────────────────────
    #  Path helpers
    # ────────────────────────────────────────────────────────────────────

    def get_path_string(self) -> str:
        """Return the current path as a Unix-style string (e.g. /home/alice)."""
        if not self.current_path:
            return "/"
        return "/" + "/".join(self.current_path)

    def _resolve(self, path_list: list[str]):
        """
        Walk the filesystem tree following a list of directory names.
        Returns the node (dict or str) if found, otherwise None.
        """
        node = self.tree
        for part in path_list:
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return None
        return node

    def current_node(self) -> dict | None:
        """Return the dict representing the current working directory."""
        node = self._resolve(self.current_path)
        if isinstance(node, dict):
            return node
        return None

    # ────────────────────────────────────────────────────────────────────
    #  Navigation
    # ────────────────────────────────────────────────────────────────────

    def change_directory(self, target: str) -> None:
        """
        Change the current working directory.
        Supports:
          '..'  → go up one level
          name  → enter a sub-directory by name
        """
        if target == "..":
            if self.current_path:
                self.current_path.pop()
            else:
                print("cd: already at root /")
            return

        new_path = self.current_path + [target]
        node = self._resolve(new_path)

        if node is None:
            print(f"cd: {target}: Directory not found")
        elif isinstance(node, str):
            print(f"cd: {target}: Not a directory")
        else:
            self.current_path = new_path

    # ────────────────────────────────────────────────────────────────────
    #  Directory listing
    # ────────────────────────────────────────────────────────────────────

    def list_directory(self) -> None:
        """Print the contents of the current directory."""
        node = self.current_node()
        if node is None:
            print("ls: cannot access current directory")
            return

        folders = sorted(k for k, v in node.items() if isinstance(v, dict))
        files   = sorted(k for k, v in node.items() if isinstance(v, str))

        if not folders and not files:
            print("  (empty directory)")
            return

        for name in folders:
            # Blue colour for directories
            print(f"  \033[94m{name}/\033[0m")
        for name in files:
            print(f"  {name}")

    # ────────────────────────────────────────────────────────────────────
    #  Creating files and folders
    # ────────────────────────────────────────────────────────────────────

    def make_directory(self, name: str) -> None:
        """Create a new sub-directory inside the current directory."""
        node = self.current_node()
        if node is None:
            print("mkdir: cannot access current directory")
            return
        if name in node:
            print(f"mkdir: {name}: Already exists")
        else:
            node[name] = {}
            print(f"Directory '{name}' created.")

    def touch_file(self, name: str) -> None:
        """Create an empty file inside the current directory."""
        node = self.current_node()
        if node is None:
            print("touch: cannot access current directory")
            return
        if name in node:
            print(f"touch: {name}: Already exists")
        else:
            node[name] = ""
            print(f"File '{name}' created.")

    # ────────────────────────────────────────────────────────────────────
    #  Reading and writing files
    # ────────────────────────────────────────────────────────────────────

    def cat_file(self, name: str) -> None:
        """Print the contents of a file to the screen."""
        node = self.current_node()
        if node is None:
            print("cat: cannot access current directory")
            return
        if name not in node:
            print(f"cat: {name}: File not found")
        elif isinstance(node[name], dict):
            print(f"cat: {name}: Is a directory")
        else:
            content = node[name]
            print(content if content else "(empty file)")

    def write_file(self, name: str, content: str) -> None:
        """
        Write (or overwrite) content into a file.
        Creates the file if it does not exist yet.
        """
        node = self.current_node()
        if node is None:
            print("write: cannot access current directory")
            return
        if name in node and isinstance(node[name], dict):
            print(f"write: {name}: Is a directory")
            return
        node[name] = content
        print(f"Saved to '{name}'.")

    # ────────────────────────────────────────────────────────────────────
    #  User home directory management
    # ────────────────────────────────────────────────────────────────────

    def ensure_user_home(self, username: str) -> None:
        """
        Create /home/<username> if it does not already exist,
        then set it as the current working directory.
        """
        home_node = self.tree.setdefault("home", {})
        if username not in home_node:
            home_node[username] = {
                "notes.txt": f"Welcome, {username}!\nThis is your personal notes file.",
                "projects": {}
            }
        self.current_path = ["home", username]
