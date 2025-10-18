"""
Custom auto-completion for REPL (Claude Code style).
"""

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from typing import Iterable


class SlashCommandCompleter(Completer):
    """
    Custom completer for commands with / prefix (Claude Code style).

    Features:
    - Live dropdown as you type
    - Matches commands that start with typed text
    - Shows command descriptions
    - Styled for better visibility
    - Auto-selects when only one match available
    """

    def __init__(self, commands: dict):
        """
        Initialize completer with command dictionary.

        Args:
            commands: Dict mapping command names to help text
                     e.g., {'help': 'Show available commands', ...}
        """
        self.commands = commands

    def get_completions(
        self, document: Document, complete_event
    ) -> Iterable[Completion]:
        """
        Get completions for the current input.

        Args:
            document: Current document/input
            complete_event: Completion event

        Yields:
            Completion objects for matching commands
        """
        # Get current text before cursor
        text = document.text_before_cursor

        # Only show completions if we start with /
        if not text.startswith("/"):
            return

        # Get the part after /
        search_text = text[1:]

        # Check if we're past the command (space detected after /)
        if " " in search_text:
            # Space means user is entering arguments/subcommands - no completions
            return

        # Convert to lowercase for case-insensitive matching
        search_lower = search_text.lower()

        # Find matching commands
        for cmd_name, cmd_help in sorted(self.commands.items()):
            if cmd_name.lower().startswith(search_lower):
                # Calculate how many characters to replace
                # If user typed "/c", we want to replace "c" with "config"
                start_position = -len(search_text) if search_text else 0

                yield Completion(
                    text=cmd_name,
                    start_position=start_position,
                    display=f"/{cmd_name}",
                    display_meta=cmd_help or "",
                )

        # If no matches found and user has typed something, list disappears
        # (handled by yielding nothing)
