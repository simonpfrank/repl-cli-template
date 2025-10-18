"""
Configuration management commands.
"""

import click
import logging
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
import yaml

from repl_cli_template.core.config_manager import ConfigManager
from repl_cli_template.ui.styles import (
    APP_THEME,
    format_success,
    format_error,
    format_info,
)

console = Console(theme=APP_THEME)
logger = logging.getLogger(__name__)


@click.group()
def config():
    """Configuration management commands."""
    pass


@config.command("show")
@click.pass_context
def config_show(context):
    """Display current configuration."""
    try:
        config_dict = context.obj.get("config", {})

        if not config_dict:
            console.print(format_info("No configuration loaded"))
            return

        # Convert config to YAML for pretty display
        config_yaml = yaml.dump(config_dict, default_flow_style=False, sort_keys=False)

        # Syntax highlighting
        syntax = Syntax(config_yaml, "yaml", theme="monokai", line_numbers=False)

        # Display in a panel
        panel = Panel(
            syntax,
            title="[bold cyan]Current Configuration[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )

        console.print()
        console.print(panel)
        console.print()

    except Exception as e:
        console.print(format_error(str(e)))
        logger.exception(f"Failed to display config: {str(e)}")
        raise click.Abort()


@config.command("load")
@click.option("--file", "-f", required=True, help="Path to config file")
@click.pass_context
def config_load(context, file):
    """Load configuration from YAML file."""
    try:
        # Load config
        config_dict = ConfigManager.load(file)

        # Merge with defaults
        config_dict = ConfigManager.merge_with_defaults(config_dict)

        # Update context
        context.obj["config"] = config_dict
        context.obj["config_file"] = file

        console.print()
        console.print(format_success(f"Configuration loaded from: {file}"))
        console.print()

    except FileNotFoundError as e:
        console.print(format_error(str(e)))
        logger.error(f"Config file not found: {file}")
        raise click.Abort()

    except Exception as e:
        console.print(format_error(f"Failed to load config: {str(e)}"))
        logger.exception(f"Failed to load config: {str(e)}")
        raise click.Abort()


@config.command("save")
@click.option("--file", "-f", required=True, help="Path to save config file")
@click.pass_context
def config_save(context, file):
    """Save current configuration to YAML file."""
    try:
        config_dict = context.obj.get("config", {})

        if not config_dict:
            console.print(format_error("No configuration to save"))
            raise click.Abort()

        # Save config
        ConfigManager.save(config_dict, file)

        console.print()
        console.print(format_success(f"Configuration saved to: {file}"))
        console.print()

    except Exception as e:
        console.print(format_error(f"Failed to save config: {str(e)}"))
        logger.exception(f"Failed to save config: {str(e)}")
        raise click.Abort()


@config.command("set")
@click.option(
    "--key", "-k", required=True, help="Config key (dot notation, e.g., logging.level)"
)
@click.option("--value", "-v", required=True, help="Config value")
@click.pass_context
def config_set(context, key, value):
    """Set a configuration value."""
    try:
        config_dict = context.obj.get("config", {})

        if not config_dict:
            console.print(format_error("No configuration loaded"))
            raise click.Abort()

        # Set the value
        ConfigManager.set(config_dict, key, value)

        console.print()
        console.print(format_success(f"Set {key} = {value}"))
        console.print()

    except Exception as e:
        console.print(format_error(f"Failed to set config: {str(e)}"))
        logger.exception(f"Failed to set config: {str(e)}")
        raise click.Abort()
