"""
users.py - User Session Management for TerminalOS
--------------------------------------------------
Handles login, stores the active username, and generates
the coloured shell prompt string.
No passwords required – any non-empty username is accepted.
"""


class UserSession:
    """
    Represents the currently logged-in user.

    Responsibilities:
      - Prompt for a username at login
      - Store the username in memory for the session
      - Build the shell prompt string shown before every command
    """

    def __init__(self):
        self.username: str = ""

    # ────────────────────────────────────────────────────────────────────
    #  Login
    # ────────────────────────────────────────────────────────────────────

    def login(self) -> None:
        """
        Display the TerminalOS login screen and ask for a username.
        Loops until a non-empty username is entered.
        """
        self._print_login_banner()

        while True:
            username = input("Username: ").strip()
            if username:
                self.username = username
                break
            print("  Username cannot be empty. Please try again.")

    # ────────────────────────────────────────────────────────────────────
    #  Prompt
    # ────────────────────────────────────────────────────────────────────

    def get_prompt(self, path_string: str) -> str:
        """
        Return the formatted, coloured shell prompt.

        Example output (rendered in terminal):
            alice@TerminalOS:/home/alice$
            └─ green ─┘          └─ blue ─┘
        """
        green = "\033[92m"
        blue  = "\033[94m"
        reset = "\033[0m"
        return f"{green}{self.username}@TerminalOS{reset}:{blue}{path_string}{reset}$ "

    # ────────────────────────────────────────────────────────────────────
    #  Welcome message
    # ────────────────────────────────────────────────────────────────────

    def print_welcome(self) -> None:
        """Print a welcome message after a successful login."""
        print(f"\nWelcome, {self.username}!")
        print("Type 'help' to see available commands.\n")

    # ────────────────────────────────────────────────────────────────────
    #  Internal helpers
    # ────────────────────────────────────────────────────────────────────

    @staticmethod
    def _print_login_banner() -> None:
        """Print the login screen banner."""
        print("\n" + "=" * 42)
        print("         TerminalOS v1.0  –  Login")
        print("=" * 42)
