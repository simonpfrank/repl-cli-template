# REPL/CLI Template

A Python template for building applications with unified REPL (Read-Eval-Print Loop) and CLI (Command Line Interface) interfaces. Define commands once, use them everywhere.

## Features

- **Unified Architecture**: Same commands work in both REPL and CLI modes
- **Smart Auto-Completion**: Claude Code-style slash commands with live filtering, subcommand and option completion
- **Beautiful UI**: Colorful terminal output with ASCII art welcome screen
- **Config Management**: YAML-based configuration with override hierarchy
- **Structured Logging**: Non-intrusive logging with detailed error tracking
- **Testable**: Framework-agnostic core logic, easy to test without UI
- **Extensible**: Simple to add new commands and customize

## Quick Start

### Installation

1. **Clone or copy this template** into your project directory
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### REPL Mode (Interactive)
```bash
python -m repl_cli_template.app
```

Or with custom config:
```bash
python -m repl_cli_template.app --config myconfig.yaml
```

#### CLI Mode (Single Command)
```bash
# Show config
python -m repl_cli_template.app config show

# Process a file
python -m repl_cli_template.app process --input data.txt

# Get help
python -m repl_cli_template.app --help
python -m repl_cli_template.app process --help
```

## Auto-Completion

The REPL features smart auto-completion inspired by Claude Code:

- **Type `/`** to see all available commands
- **Keep typing** to filter commands (e.g., `/con` shows only `/config`)
- **Press Space** to complete the highlighted command
- **Subcommands**: After typing `/config `, see subcommands like `show`, `load`, `save`, `set`
- **Options**: After `/config load `, see available options like `--file`
- **Backspace** automatically refilters the list

Auto-completion works for:
- Top-level commands (`/help`, `/config`, `/process`)
- Subcommands (`/config show`, `/config load`)
- Command options (`/config load --file`)

## Usage Examples

### REPL Mode

```
> /help
Available Commands

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Command            ┃ Description                        ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ /config            │ Configuration management commands  │
│ /process           │ Process data from input file       │
│ /help              │ Show available commands            │
│ /quit              │ Exit the REPL                      │
└────────────────────┴────────────────────────────────────┘

> /config show
╭─────────── Current Configuration ────────────╮
│ app:                                          │
│   name: REPL CLI Template                     │
│   version: 1.0.0                              │
│ logging:                                      │
│   level: INFO                                 │
│   file: logs/app.log                          │
╰───────────────────────────────────────────────╯

> /process --input test.txt
✓ Successfully processed 3 rows

┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property       ┃ Value                ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ Rows Processed │ 3                    │
│ Output File    │ data/output/test.txt │
└────────────────┴──────────────────────┘

> /quit
Goodbye! 👋
```

## Project Structure

```
repl_cli_template/
├── app.py                   # Main entry point
├── commands/                # Command definitions (UI layer)
│   ├── config_commands.py   # Config management
│   ├── process_commands.py  # Business logic commands
│   └── system_commands.py   # Help, quit, etc.
├── core/                    # Business logic (framework-agnostic)
│   ├── config_manager.py    # Config loading/saving
│   ├── logging_setup.py     # Logging configuration
│   └── processor.py         # Example business logic
├── ui/                      # REPL UI components
│   ├── completion.py        # Auto-completion for slash commands
│   ├── welcome.py           # Welcome screen, ASCII art
│   └── styles.py            # Rich themes and styles
└── tests/                   # Unit and integration tests
    ├── test_core.py         # Core logic tests
    ├── test_commands.py     # Command tests
    └── fixtures/            # Test data
```

## Customizing the Template

### 1. Adding a New Command

Create a command in `commands/` folder:

```python
# commands/my_commands.py
import click
from rich.console import Console
from core.my_module import my_function
from ui.styles import APP_THEME, format_success

console = Console(theme=APP_THEME)

@click.command()
@click.option('--input', required=True)
@click.pass_context
def my_command(context, input):
    """My custom command."""
    try:
        config = context.obj.get('config', {})
        result = my_function(input, config)
        console.print(format_success(f"Done: {result}"))
    except Exception as e:
        console.print(f"[error]Error:[/error] {str(e)}")
        raise click.Abort()
```

Register it in `app.py`:

```python
from repl_cli_template.commands.my_commands import my_command
cli.add_command(my_command, name='my_command')
```

### 2. Adding Business Logic

Add your core logic in `core/` folder:

```python
# core/my_module.py
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def my_function(input_data: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Framework-agnostic business logic.
    Can be called from REPL, CLI, API, Web UI, or tests.
    """
    logger.info(f"Processing: {input_data}")

    # Your logic here
    result = {"status": "success", "data": processed_data}

    return result
```

### 3. Customizing the Welcome Screen

Edit `ui/welcome.py`:

```python
def generate_ascii_art(app_name: str = "REPL CLI") -> str:
    # Generate your ASCII art at: http://patorjk.com/software/taag/
    art = """
  __  ____   __    _    ____  ____
 |  \\/  \\ \\ / /   / \\  |  _ \\|  _ \\
 | |\\/| |\\ V /   / _ \\ | |_) | |_) |
 | |  | | | |   / ___ \\|  __/|  __/
 |_|  |_| |_|  /_/   \\_\\_|   |_|
    """
    return art
```

### 4. Extending Configuration

Edit `config.yaml` and add your custom settings:

```yaml
custom:
  my_setting: "value"
  api_key: "your-key"
  max_retries: 3
```

Access in your code:

```python
from repl_cli_template.core.config_manager import ConfigManager

value = ConfigManager.get(config, 'custom.my_setting', 'default')
```

## Testing

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=repl_cli_template --cov-report=html
```

Run specific test file:

```bash
pytest repl_cli_template/tests/test_core.py
```

### Example: Testing Without UI

```python
# Test core logic directly
from repl_cli_template.core.processor import process_data

def test_my_function():
    config = {'setting': 'value'}
    result = process_data('input.txt', config)
    assert result['status'] == 'success'

# Test commands programmatically
from click.testing import CliRunner
from repl_cli_template.app import cli

def test_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['process', '--input', 'test.txt'])
    assert result.exit_code == 0
    assert 'Success' in result.output
```

## Configuration

### Config Hierarchy

Configuration follows this override pattern:

```
Defaults → Config File → CLI Arguments
```

Each layer overrides the previous. Missing values use defaults.

### Config File Structure

```yaml
app:
  name: "My App"
  version: "1.0.0"

logging:
  level: "INFO"         # DEBUG, INFO, WARNING, ERROR, CRITICAL
  file: "logs/app.log"
  console_enabled: false

paths:
  input_dir: "data/input"
  output_dir: "data/output"

custom:
  # Your project-specific settings
```

## Architecture Principles

1. **Define Once, Use Everywhere**: Commands work in REPL, CLI, and future interfaces
2. **Thin Commands**: Commands are minimal wrappers around core logic
3. **Core is King**: Business logic in `core/` has no CLI dependencies
4. **Config Hierarchy**: Defaults → File → Args (each overrides previous)
5. **Structured Errors**: All errors logged with type, line number, message
6. **Visual Appeal**: Rich formatting is not optional

## Development Tips

### Adding Dependencies

Add to `requirements.txt`:

```
# Optional: Interactive prompts
questionary>=2.0.0

# Optional: Hot reload
watchdog>=3.0.0
```

### Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

# Log with context
logger.info(f"Processing file: {filename}")

# Log errors with full traceback
logger.exception(f"Failed to process: {str(e)}")
```

### Error Handling Pattern

```python
@click.command()
def my_command(context, input):
    """Command description."""
    try:
        # Core handles validation
        result = my_core_function(input, config)

        # Display result
        console.print(format_success("Done!"))

    except Exception as e:
        # Catchall - core already logged details
        console.print(format_error(str(e)))
        logger.exception(f"Command failed: {str(e)}")
        raise click.Abort()
```

## Troubleshooting

### REPL commands not found

Make sure you're using the `/` prefix:
- ✓ `/help`
- ✗ `help`

### Config not loading

Check the config file path and YAML syntax:

```bash
# Verify config file
python -m yaml config.yaml

# Specify config explicitly
python -m repl_cli_template.app --config /path/to/config.yaml
```

### Logs not appearing in REPL

This is by design. Logs go to file only in REPL mode to avoid UI disruption.
Check `logs/app.log` for log output.

## License

This template is provided as-is for your use. Customize freely!

## Contributing

This is a template project. Fork it and make it your own!

## Support

For issues or questions, refer to:
- **PRD**: See `PRD.md` for complete requirements
- **Decisions**: See `DECISIONS.md` for architecture decisions
- **Tests**: See `repl_cli_template/tests/` for examples

---

**Built with**: Python 3.8+, Click, Rich, click-repl, prompt_toolkit

**Happy Building!** 🚀
