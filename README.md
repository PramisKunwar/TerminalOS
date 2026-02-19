# TerminalOS v1.0

A simulated operating system that runs entirely inside your terminal. Built with Python, TerminalOS mimics the feel of a real OS shell — complete with a boot sequence, login screen, virtual filesystem, and built-in commands — without touching your real system at all.

---

## Features

- Animated boot sequence with status messages
- Login screen with username support (no password required)
- Coloured shell prompt: `username@TerminalOS:/current/path$`
- In-memory virtual filesystem (no real disk access)
- Personal home directory auto-created at login
- 12 built-in commands
- Friendly error messages for invalid input
- Graceful `Ctrl+C` handling

---

## Getting Started

**Requirements:** Python 3.10 or higher. No external libraries needed.

**Installation:** Clone or download the project, then place all four `.py` files in the same folder.

```bash
python terminalos.py
```

That's it. No installs, no dependencies.

---

## Project Structure

```
terminalos/
├── terminalos.py     # Main entry point – boot sequence and shell loop
├── filesystem.py     # Virtual in-memory filesystem logic
├── commands.py       # Built-in command parsing and handling
└── users.py          # User login, session, and prompt generation
```

Each file has a single, focused responsibility so the codebase stays easy to read and extend.

| File | Class | Responsibility |
|---|---|---|
| `terminalos.py` | — | Boot sequence, wires modules, runs the shell loop |
| `filesystem.py` | `FileSystem` | Virtual filesystem stored as a nested Python dict |
| `commands.py` | `CommandHandler` | Parses input, dispatches to command methods |
| `users.py` | `UserSession` | Login screen, stores username, builds the prompt |

---

## Commands

| Command | Description |
|---|---|
| `help` | Show all available commands |
| `clear` | Clear the terminal screen |
| `whoami` | Print the current username |
| `pwd` | Print the current directory path |
| `ls` | List files and folders in the current directory |
| `cd <dir>` | Change into a directory |
| `cd ..` | Go up one directory level |
| `mkdir <name>` | Create a new directory |
| `touch <name>` | Create a new empty file |
| `cat <file>` | Print the contents of a file |
| `echo <text>` | Print text to the screen |
| `write <file>` | Interactively write and save text to a file |
| `exit` | Shut down TerminalOS |

---

## How the Filesystem Works

The virtual filesystem is a nested Python dictionary stored entirely in memory. It is created fresh each time TerminalOS starts and discarded when it exits — nothing is ever written to your real disk.

```python
{
    "home": {
        "alice": {
            "notes.txt": "Welcome, alice!",
            "projects": {}
        }
    },
    "etc": {
        "motd.txt": "Have a productive day!"
    },
    "tmp": {}
}
```

- **Folders** are `dict` values
- **Files** are `str` values (their text content)
- The current path is tracked as a list of keys, e.g. `["home", "alice"]`

When you log in, TerminalOS automatically creates `/home/<username>` with a starter `notes.txt` and an empty `projects/` folder.

---

## Example Session

```
  TerminalOS v1.0

  [ OK ]  Booting TerminalOS v1.0 ...
  [ OK ]  Loading system files ...
  [ OK ]  Mounting virtual drives ...
  [ OK ]  Starting services ...
  [ OK ]  System ready.

  TerminalOS v1.0 – Login
  ════════════════════════
  Username: alice

  Welcome, alice!
  Type 'help' to see available commands.

alice@TerminalOS:/home/alice$ ls
  projects/
  notes.txt

alice@TerminalOS:/home/alice$ mkdir work
Directory 'work' created.

alice@TerminalOS:/home/alice$ touch todo.txt

alice@TerminalOS:/home/alice$ write todo.txt
Writing to 'todo.txt'. Enter your text below.
(Leave a blank line and press Enter to save.)

Finish the TerminalOS readme
Review pull requests

Saved to 'todo.txt'.

alice@TerminalOS:/home/alice$ cat todo.txt
Finish the TerminalOS readme
Review pull requests

alice@TerminalOS:/home/alice$ cd work
alice@TerminalOS:/home/alice/work$ pwd
/home/alice/work

alice@TerminalOS:/home/alice/work$ cd ..
alice@TerminalOS:/home/alice$ exit

Shutting down TerminalOS...
All processes stopped.
Goodbye!
```

---

## Extending TerminalOS

Adding a new command takes three steps:

**1. Write a handler method in `commands.py`:**
```python
def _cmd_date(self, _args: str) -> bool:
    """Print a fake system date."""
    print("TerminalOS Internal Clock: Day 1, 00:00:00")
    return True
```

**2. Register it in `_build_dispatch_table()`:**
```python
"date": self._cmd_date,
```

**3. Add it to `HELP_TEXT`** so users can discover it.

To add persistent data or more complex filesystem features, extend the `FileSystem` class in `filesystem.py`. The clean separation between modules means changes in one file rarely affect the others.

---

## Limitations (By Design)

TerminalOS is intentionally sandboxed. It does not and will not:

- Access your real filesystem
- Execute real OS or shell commands
- Make network requests
- Persist data between sessions
- Implement a permissions system

All state lives in memory and resets on exit. This makes it safe to experiment with freely.

---

## License

This project is released for educational and personal use. Feel free to fork it, extend it, or use it as a starting point for your own terminal projects.
