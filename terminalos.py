"""
terminalos.py - Main Entry Point for TerminalOS
-------------------------------------------------
Wires together all modules and runs the main shell loop.

Project structure:
    terminalos.py   ← you are here (boot + main loop)
    filesystem.py   ← virtual in-memory filesystem
    commands.py     ← built-in command handling
    users.py        ← user login and prompt

Run with:
    python terminalos.py
"""

import time

# Import the three supporting modules
from filesystem import FileSystem
from users      import UserSession
from commands   import CommandHandler


# ─────────────────────────────────────────────────────────────────────────────
#  Boot sequence
# ─────────────────────────────────────────────────────────────────────────────

def boot_sequence() -> None:
    """
    Display an animated boot sequence to set the OS atmosphere.
    Each message is printed with a short delay to mimic a real boot process.
    """
    banner = r"""
  ______                    _             _  ____   _____
 |__  / |_ ___ _ _ _ __ ___ (_)_ _   __ _| |/ __ \ / ____|
   / /| __/ _ \ '_| '_ ` _ \| | ' \ / _` | | |  | | (___
  / /_| ||  __/ | | | | | | | | | | | (_| | | |__| |\__ \
 /____|\__\___|_| |_| |_| |_|_|_| |_|\__,_|_|\____/ |____/
    """
    print(banner)

    boot_steps = [
        ("Booting TerminalOS v1.0 ...", 0.45),
        ("Loading system files ...   ", 0.50),
        ("Mounting virtual drives ...", 0.40),
        ("Starting services ...      ", 0.45),
        ("System ready.              ", 0.30),
    ]

    print("=" * 50)
    for message, delay in boot_steps:
        print(f"  [ OK ]  {message}")
        time.sleep(delay)
    print("=" * 50)


# ─────────────────────────────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    """
    Application entry point.

    Flow:
      1. Display boot sequence
      2. Show login screen and capture username
      3. Initialise the virtual filesystem and create a home directory
      4. Print the welcome message
      5. Enter the interactive command loop
    """

    # ── 1. Boot ──────────────────────────────────────────────────────────
    boot_sequence()

    # ── 2. Login ─────────────────────────────────────────────────────────
    user = UserSession()
    user.login()

    # ── 3. Filesystem setup ──────────────────────────────────────────────
    fs = FileSystem()
    fs.ensure_user_home(user.username)   # creates /home/<username>

    # ── 4. Welcome ───────────────────────────────────────────────────────
    user.print_welcome()

    # ── 5. Command handler ───────────────────────────────────────────────
    handler = CommandHandler(fs, user)

    # ── 6. Main interactive shell loop ───────────────────────────────────
    running = True
    while running:
        try:
            # Display the prompt and wait for user input
            raw_input = input(user.get_prompt(fs.get_path_string()))

            # Pass input to the command handler; it returns False to exit
            running = handler.handle(raw_input)

        except KeyboardInterrupt:
            # Ctrl+C pressed – remind the user how to quit cleanly
            print("\n  (Tip: type 'exit' to shut down TerminalOS)")

        except EOFError:
            # End of piped input – exit gracefully
            print()
            break


# ─────────────────────────────────────────────────────────────────────────────
#  Script guard
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
