"""
commands.py - Command Handler for TerminalOS
---------------------------------------------
Parses raw user input and dispatches it to the correct command method.
Each built-in command is implemented as a private method (_cmd_<name>).

To add a new command:
  1. Write a  _cmd_yourcommand(self, args: str) -> bool  method.
  2. Register it in the  _build_dispatch_table()  method.
"""

import os

from filesystem import FileSystem
from users import UserSession


class CommandHandler:
    """
    Parses user input and runs the matching built-in command.

    All command methods follow this contract:
      - Accept a single `args` string (everything after the command word).
      - Return True  → keep the OS shell running.
      - Return False → shut down the OS.
    """

    # ── Help text shown by the 'help' command ────────────────────────────
    HELP_TEXT = """
┌─────────────────────────────────────────────────┐
│              TerminalOS  –  Commands             │
├──────────────┬──────────────────────────────────┤
│ help         │ Show this help message            │
│ clear        │ Clear the screen                  │
│ whoami       │ Show current username             │
│ pwd          │ Show current directory path       │
│ ls           │ List files and folders            │
│ cd <dir>     │ Change directory                  │
│ cd ..        │ Go up one directory               │
│ mkdir <name> │ Create a new directory            │
│ touch <name> │ Create a new empty file           │
│ cat <file>   │ Show file contents                │
│ echo <text>  │ Print text to the screen          │
│ write <file> │ Write text into a file            │
│ exit         │ Shut down TerminalOS              │
└──────────────┴──────────────────────────────────┘
"""

    def __init__(self, fs: FileSystem, user: UserSession):
        self.fs   = fs
        self.user = user
        # Build the command → method mapping once at startup
        self._dispatch = self._build_dispatch_table()

    # ────────────────────────────────────────────────────────────────────
    #  Public interface
    # ────────────────────────────────────────────────────────────────────

    def handle(self, raw_input: str) -> bool:
        """
        Parse raw_input and execute the matching command.

        Returns:
            True  – the shell should keep running.
            False – the shell should exit.
        """
        # Split into (command, rest-of-line)
        parts   = raw_input.strip().split(maxsplit=1)
        if not parts:
            return True   # blank line – do nothing

        command = parts[0].lower()
        args    = parts[1] if len(parts) > 1 else ""

        if command in self._dispatch:
            return self._dispatch[command](args)

        # Unknown command
        print(f"TerminalOS: '{command}': command not found  "
              f"(type 'help' for a list of commands)")
        return True

    # ────────────────────────────────────────────────────────────────────
    #  Dispatch table
    # ────────────────────────────────────────────────────────────────────

    def _build_dispatch_table(self) -> dict:
        """
        Map command name strings to their handler methods.
        Adding a new command is as simple as adding one entry here
        and writing the corresponding _cmd_* method below.
        """
        return {
            "help":   self._cmd_help,
            "clear":  self._cmd_clear,
            "whoami": self._cmd_whoami,
            "pwd":    self._cmd_pwd,
            "ls":     self._cmd_ls,
            "cd":     self._cmd_cd,
            "mkdir":  self._cmd_mkdir,
            "touch":  self._cmd_touch,
            "cat":    self._cmd_cat,
            "echo":   self._cmd_echo,
            "write":  self._cmd_write,
            "exit":   self._cmd_exit,
        }

    # ────────────────────────────────────────────────────────────────────
    #  Built-in command implementations
    # ────────────────────────────────────────────────────────────────────

    def _cmd_help(self, _args: str) -> bool:
        """Display the help table."""
        print(self.HELP_TEXT)
        return True

    def _cmd_clear(self, _args: str) -> bool:
        """Clear the terminal screen (cross-platform)."""
        os.system("cls" if os.name == "nt" else "clear")
        return True

    def _cmd_whoami(self, _args: str) -> bool:
        """Print the current username."""
        print(self.user.username)
        return True

    def _cmd_pwd(self, _args: str) -> bool:
        """Print the current working directory path."""
        print(self.fs.get_path_string())
        return True

    def _cmd_ls(self, _args: str) -> bool:
        """List files and folders in the current directory."""
        self.fs.list_directory()
        return True

    def _cmd_cd(self, args: str) -> bool:
        """
        Change directory.
          cd          → go to the user's home directory
          cd <name>   → enter sub-directory <name>
          cd ..       → go up one level
        """
        target = args.strip()
        if not target:
            # No argument: jump straight to the user's home
            self.fs.current_path = ["home", self.user.username]
        else:
            self.fs.change_directory(target)
        return True

    def _cmd_mkdir(self, args: str) -> bool:
        """Create a new directory inside the current directory."""
        name = args.strip()
        if not name:
            print("mkdir: missing directory name")
        else:
            self.fs.make_directory(name)
        return True

    def _cmd_touch(self, args: str) -> bool:
        """Create a new empty file inside the current directory."""
        name = args.strip()
        if not name:
            print("touch: missing file name")
        else:
            self.fs.touch_file(name)
        return True

    def _cmd_cat(self, args: str) -> bool:
        """Print the contents of a file."""
        name = args.strip()
        if not name:
            print("cat: missing file name")
        else:
            self.fs.cat_file(name)
        return True

    def _cmd_echo(self, args: str) -> bool:
        """Print the supplied text to the screen."""
        print(args)
        return True

    def _cmd_write(self, args: str) -> bool:
        """
        Interactively write multi-line text into a file.
        The user types lines; an empty line signals end-of-input.
        """
        filename = args.strip()
        if not filename:
            print("write: missing file name")
            return True

        print(f"Writing to '{filename}'. Enter your text below.")
        print("(Leave a blank line and press Enter to save and finish.)\n")

        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)

        self.fs.write_file(filename, "\n".join(lines))
        return True

    def _cmd_exit(self, _args: str) -> bool:
        """Initiate the TerminalOS shutdown sequence."""
        import time
        print("\nShutting down TerminalOS...")
        time.sleep(0.6)
        print("All processes stopped.")
        time.sleep(0.3)
        print("Goodbye!\n")
        return False   # signals the main loop to stop
