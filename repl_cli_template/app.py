"""
Main entry point for REPL/CLI application.
"""

import click
from click_repl import repl
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
import sys
from pathlib import Path

from repl_cli_template.core.config_manager import ConfigManager
from repl_cli_template.core.logging_setup import setup_logging
from repl_cli_template.ui.welcome import show_welcome
from repl_cli_template.ui.styles import APP_THEME
from repl_cli_template.commands.system_commands import (
    help_command,
    quit_command,
    exit_command,
)
from repl_cli_template.commands.config_commands import config
from repl_cli_template.commands.process_commands import process

# Initialize console
console = Console(theme=APP_THEME)

# Application metadata
APP_NAME = "REPL CLI Template"
APP_VERSION = "1.0.0"
DEFAULT_CONFIG = "config.yaml"


@click.group(invoke_without_command=True)
@click.option("--config", "-c", default=DEFAULT_CONFIG, help="Path to config file")
@click.option("--repl-mode", is_flag=True, default=False, help="Start in REPL mode")
@click.pass_context
def cli(context, config, repl_mode):
    """
    REPL/CLI Template Application.

    Run without arguments to start REPL mode.
    Run with a command for CLI mode.
    """
    # Initialize context object
    context.ensure_object(dict)

    # Load configuration
    try:
        if Path(config).exists():
            config_dict = ConfigManager.load(config)
            config_dict = ConfigManager.merge_with_defaults(config_dict)
        else:
            # Use defaults if config file doesn't exist
            config_dict = ConfigManager.get_defaults()
            console.print("[dim]Config file not found, using defaults[/dim]")

        context.obj["config"] = config_dict
        context.obj["config_file"] = config

    except Exception as e:
        console.print(f"[error]Error loading config:[/error] {str(e)}")
        sys.exit(1)

    # Setup logging
    log_file = ConfigManager.get(config_dict, "logging.file", "logs/app.log")
    log_level = ConfigManager.get(config_dict, "logging.level", "INFO")

    # Enable console logging only if NOT in REPL mode
    console_enabled = context.invoked_subcommand is not None

    setup_logging(log_file, log_level, console_enabled)

    # If no subcommand provided, start REPL mode
    if context.invoked_subcommand is None or repl_mode:
        start_repl(context)


def get_command_names(cli_group):
    """
    Get all command names from the CLI group.

    Args:
        cli_group: Click group containing commands

    Returns:
        List of command names
    """
    names = []
    if hasattr(cli_group, "commands"):
        for name in cli_group.commands.keys():
            names.append(name)
    return names


def start_repl(context):
    """Start the REPL interface with / prefix support and auto-completion."""
    # Show welcome screen
    config_dict = context.obj["config"]
    config_file = context.obj["config_file"]
    log_file = ConfigManager.get(config_dict, "logging.file", "logs/app.log")

    app_name = ConfigManager.get(config_dict, "app.name", APP_NAME)
    app_version = ConfigManager.get(config_dict, "app.version", APP_VERSION)

    show_welcome(console, app_name, app_version, config_file, log_file)

    # Build command dictionary with help text
    commands_dict = {}
    if hasattr(context.command, "commands"):
        for name, cmd in context.command.commands.items():
            commands_dict[name] = cmd.help or "No description"

    # Create custom completer (Claude Code style)
    from repl_cli_template.ui.completion import SlashCommandCompleter

    completer = SlashCommandCompleter(commands_dict)

    # Custom style for completion dropdown (Claude Code exact colors from images)
    # Image 1: Unhighlighted command text color
    # Image 2: Highlighted command font color
    # Image 3: Unhighlighted help text color
    # Image 4: Highlighted help text color
    completion_style = Style.from_dict(
        {
            "completion-menu": "bg:#1e1e1e",  # Dark background for menu
            "completion-menu.completion": "bg:#2d2d2d #5fafff",  # Unhighlighted: dark gray bg, blue text
            "completion-menu.completion.current": "bg:#0a7aca #ffffff",  # Highlighted: blue bg, white text
            "completion-menu.meta": "bg:#1e1e1e",  # Dark background for meta
            "completion-menu.meta.completion": "bg:#2d2d2d #808080",  # Unhighlighted help: dark gray bg, gray text
            "completion-menu.meta.completion.current": "bg:#0a7aca #e0e0e0",  # Highlighted help: blue bg, light gray text
        }
    )

    # Configure prompt_toolkit with history, auto-completion, and styling
    from prompt_toolkit.key_binding import KeyBindings

    # Create custom key bindings for better completion behavior
    kb = KeyBindings()

    @kb.add("tab")
    def _(event):
        """Tab completes the current selection or triggers completion."""
        b = event.app.current_buffer
        if b.complete_state:
            b.complete_next()
        else:
            b.start_completion(select_first=True)

    @kb.add("down")
    def _(event):
        """Down arrow navigates through completions."""
        b = event.app.current_buffer
        if b.complete_state:
            b.complete_next()
        else:
            b.start_completion(select_first=True)

    @kb.add("up")
    def _(event):
        """Up arrow navigates through completions."""
        b = event.app.current_buffer
        if b.complete_state:
            b.complete_previous()
        else:
            b.start_completion(select_first=True)

    @kb.add("space")
    def _(event):
        """Space completes the highlighted command and adds space for arguments."""
        b = event.app.current_buffer
        if b.complete_state:
            # If completion menu is showing, apply the current completion
            completion = b.complete_state.current_completion
            if completion:
                b.apply_completion(completion)
                b.cancel_completion()
        # Always insert space
        b.insert_text(" ")

    @kb.add("enter")
    def _(event):
        """Enter accepts completion if menu is showing, then submits the command."""
        b = event.app.current_buffer
        if b.complete_state:
            # If completion menu is showing, apply the current (highlighted) completion
            completion = b.complete_state.current_completion
            if completion:
                b.apply_completion(completion)
                # After applying completion, cancel completion state and submit
                b.cancel_completion()
                b.validate_and_handle()
                return
        # Otherwise, just submit the buffer
        b.validate_and_handle()

    # Custom prompt - just "> " with separator handled separately
    prompt_kwargs = {
        "message": "> ",  # Simple prompt
        "history": FileHistory(".repl_history"),
        "completer": completer,
        "complete_while_typing": True,  # Live dropdown as you type
        "complete_in_thread": False,  # Sync completion for faster response
        "style": completion_style,
        "key_bindings": kb,  # Custom key bindings for better completion
        "complete_style": "COLUMN",  # Single column - one command per line
        "reserve_space_for_menu": 8,  # Reserve space for completion menu
    }

    # Patch click_repl to strip leading / from commands and add separators
    import click_repl._repl as repl_module
    from click_repl import ExitReplException

    # Save original function
    original_execute = repl_module._execute_internal_and_sys_cmds

    def execute_with_slash_stripping(
        command, allow_internal_commands, allow_system_commands
    ):
        """Wrapper that strips leading / before processing command and adds separators."""
        # Check if agent mode is enabled
        agent_enabled = ConfigManager.get(config_dict, "agent.enabled", False)

        # Strip leading / if present (Claude Code style)
        if command.startswith("/"):
            command = command[1:]
        else:
            # No / prefix - could be free text for agent
            if agent_enabled and command.strip():
                # Future: Send to agent/LLM
                console.print()
                console.print(
                    "[yellow]Agent mode:[/yellow] Would send to LLM: " + command
                )
                console.print("[dim](Agent integration not yet implemented)[/dim]")
                console.print()
                console.print("[dim]" + "─" * console.width + "[/dim]")
                console.print()
                return None

        # Try to execute the command
        try:
            result = original_execute(
                command, allow_internal_commands, allow_system_commands
            )
            # Print separator below the output (above next prompt)
            console.print()
            console.print("[dim]" + "─" * console.width + "[/dim]")
            return result

        except click.exceptions.ClickException as e:
            # Handle Click exceptions (missing args, bad options, etc.) gracefully
            console.print()
            console.print(f"[red]Error:[/red] {e.format_message()}")
            console.print()
            console.print(f"[dim]Try:[/dim] [cyan]/{command} --help[/cyan] for usage")
            console.print()
            return None

        except Exception as e:
            # Handle unknown command errors gracefully
            error_msg = str(e)
            if (
                "No such command" in error_msg
                or "no command named" in error_msg.lower()
            ):
                console.print()
                console.print(f"[red]Unknown command:[/red] {command}")
                console.print()
                console.print("[dim]Commands must start with /[/dim]")
                console.print(
                    "[dim]Try:[/dim] [cyan]/help[/cyan] to see available commands"
                )
                if not agent_enabled:
                    console.print(
                        "[dim]Tip: Enable agent mode in config to send free text to LLM[/dim]"
                    )
                console.print()
                return None
            else:
                # For other exceptions, show simplified error
                console.print()
                console.print(f"[red]Error:[/red] {str(e)}")
                console.print()
                return None

    # Temporarily replace the function
    repl_module._execute_internal_and_sys_cmds = execute_with_slash_stripping

    # Start REPL
    try:
        repl(context, prompt_kwargs=prompt_kwargs)
    except (KeyboardInterrupt, EOFError):
        # Handle Ctrl+C and Ctrl+D gracefully
        from repl_cli_template.ui.welcome import show_goodbye

        console.print()
        show_goodbye(console)
        sys.exit(0)
    except ExitReplException:
        # Clean exit from /quit or /exit command
        sys.exit(0)
    finally:
        # Restore original function
        repl_module._execute_internal_and_sys_cmds = original_execute


# Register commands
cli.add_command(help_command, name="help")
cli.add_command(quit_command, name="quit")
cli.add_command(exit_command, name="exit")
cli.add_command(config, name="config")
cli.add_command(process, name="process")


def main():
    """Entry point for the application."""
    cli(obj={})


if __name__ == "__main__":
    main()
