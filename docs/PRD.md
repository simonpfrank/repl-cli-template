# Product Requirements Document: Python REPL/CLI Template

**Version:** 1.0
**Date:** 2025-10-16
**Status:** Draft

---

## 1. Executive Summary

### 1.1 Purpose
A reusable Python template for building applications with unified REPL (Read-Eval-Print Loop) and CLI (Command Line Interface) interfaces that share the same core business logic without code duplication.

### 1.2 Goals
- **Simple**: Minimal boilerplate, easy to understand and extend in new projects
- **Unified**: Same commands work in both REPL and CLI modes
- **Testable**: Enable functional testing without UI interaction to catch bugs early
- **Maintainable**: No code duplication between interfaces
- **Future-proof**: Architecture supports adding API/Web interfaces later

### 1.3 Non-Goals
- No packaging/distribution as pip-installable package
- No automatic installation to user home directories
- No complex plugin systems or abstract base classes
- Not a full TUI (Text User Interface) framework
- CLI is NOT a subset of REPL - they share the same commands

---

## 2. Technical Stack

### 2.1 Core Dependencies
| Package | Purpose | Justification |
|---------|---------|---------------|
| **click** | CLI framework | Industry standard, simple, well-documented |
| **click-repl** | REPL mode for click | Bridges CLI commands into REPL seamlessly |
| **rich** | Terminal formatting | Beautiful tables, colors, panels - Claude Code-like output |
| **prompt_toolkit** | (via click-repl) | History, auto-completion, multi-line input |
| **PyYAML** | Config persistence | Standard YAML support |

### 2.2 Optional Dependencies
| Package | Purpose | When to Use |
|---------|---------|-------------|
| **questionary** | Interactive prompts | When you need fancy selection lists, confirmations |
| **watchdog** | File watching | For hot reload functionality |

### 2.3 Python Version
- **Minimum:** Python 3.8+ (for Rich library)
- **Recommended:** Python 3.10+

---

## 3. Architecture

### 3.1 Conceptual Architecture

```
┌─────────────────────────────────────────────┐
│         Interface Layer                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │   REPL   │  │   CLI    │  │ Future:  │ │
│  │  (click- │  │ (click)  │  │ API/Web  │ │
│  │   repl)  │  │          │  │          │ │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘ │
└────────┼─────────────┼─────────────┼───────┘
         │             │             │
         └─────────────┼─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   Command Registry        │
         │   (click commands)        │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   Core Business Logic     │
         │   (pure Python modules)   │
         │   - No CLI/REPL deps      │
         │   - Framework-agnostic    │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   Configuration           │
         │   Logging                 │
         │   Utilities               │
         └───────────────────────────┘
```

### 3.2 Design Principles

1. **Command Definition**: Define each command once as a click command
2. **Business Logic Separation**: Core logic in pure Python modules, no click/CLI dependencies
3. **Testability**: Core functions can be imported and tested directly
4. **Shared Configuration**: Single config object/dict shared across all interfaces
5. **Non-intrusive Logging**: Logs to file, console output only in CLI mode
6. **Thin Commands**: Commands are minimal wrappers - core handles validation and logic
7. **Config Hierarchy**: Defaults → Config File → CLI Args (each overrides previous)
8. **Descriptive Variable Names**: Use `context` not `ctx`, `configuration` not `cfg`, etc.

### 3.3 Directory Structure

```
project_root/                    # e.g., my-awesome-project/
├── repl_cli_template/           # Template code (all framework code here)
│   ├── __init__.py
│   ├── app.py                   # Main entry point (REPL & CLI)
│   ├── commands/                # Click command definitions (UI layer)
│   │   ├── __init__.py
│   │   ├── config_commands.py   # Config-related commands
│   │   ├── process_commands.py  # Business logic commands
│   │   └── system_commands.py   # Help, reload, etc.
│   ├── core/                    # Business logic (framework-agnostic)
│   │   ├── __init__.py
│   │   ├── processor.py         # Example: data processing logic
│   │   ├── config_manager.py    # Config load/save/validation
│   │   └── logging_setup.py     # Logging configuration
│   ├── ui/                      # REPL UI components (enhanced UI)
│   │   ├── __init__.py
│   │   ├── welcome.py           # ASCII art, welcome screen
│   │   └── styles.py            # Rich themes and styles
│   └── tests/
│       ├── test_core.py         # Unit tests for business logic
│       ├── test_commands.py     # Functional tests for commands
│       └── fixtures/            # Test data
├── config.yaml                  # Configuration file (project root)
├── logs/                        # Log files (project root, gitignored)
├── requirements.txt             # Dependencies
└── README.md                   # Usage instructions
```

**Note**: `logs/` stays in project root for easy access, while all template code is organized under `repl_cli_template/`

---

## 4. Sample Commands (Base Template)

The template will provide these commands as examples and scaffolding:

### 4.1 System Commands

| Command | Description | REPL | CLI | Example |
|---------|-------------|------|-----|---------|
| `help` | Show available commands with brief descriptions | ✓ | ✓ | `help` or `--help` |
| `quit` / `exit` | Exit the REPL | ✓ | N/A | `quit` |
| `reload` | Hot reload modules (nice-to-have) | ✓ | N/A | `reload` |

### 4.2 Configuration Commands

| Command | Description | REPL | CLI | Example |
|---------|-------------|------|-----|---------|
| `config show` | Display current config in Rich panel | ✓ | ✓ | `config show` |
| `config load` | Load config from YAML file | ✓ | ✓ | `config load --file config.yaml` |
| `config save` | Save current config to YAML file | ✓ | ✓ | `config save --file config.yaml` |
| `config set` | Set a config value interactively | ✓ | ✓ | `config set --key log_level --value DEBUG` |

### 4.3 Example Business Commands

| Command | Description | REPL | CLI | Example |
|---------|-------------|------|-----|---------|
| `process` | Process data from input file | ✓ | ✓ | `process --input data.csv` |
| `list-select` | Demo interactive list selection | ✓ | ✓ | `list-select --items a,b,c` |
| `multiline` | Demo multi-line input handling | ✓ | ✓ | `multiline` (then type text) |

### 4.4 Command Signature Pattern

All commands should follow a consistent pattern:

```python
import click
from rich.console import Console
from core.processor import process_data  # Core logic import

console = Console()

@click.command()
@click.option('--input', required=True, help='Input file path')
@click.pass_context
def process(context, input):
    """Process data from input file"""
    try:
        # Get config from context
        config = context.obj.get('config', {})

        # Call core business logic (which handles file validation, etc.)
        result = process_data(input, config)

        # Rich formatted output
        console.print(f"[green]✓[/green] Processed {result['rows']} rows")
        console.print_json(data=result)

    except Exception as e:
        # Catchall exception handler
        console.print(f"[red]✗ Error:[/red] {str(e)}")
        logger.exception(f"Command failed: {str(e)}")
        raise click.Abort()
```

---

## 5. Feature Requirements

### 5.1 Must-Have Features

#### 5.1.1 Command History
- **Requirement**: REPL maintains command history across sessions
- **Implementation**: prompt_toolkit FileHistory
- **Location**: `.app_history` in project root

#### 5.1.2 Slash Commands
- **Requirement**: In REPL mode, commands are prefixed with `/` (click-repl default)
- **Behavior**: `/help`, `/config show`, `/process --input file.csv`
- **Alternative**: Also support commands without `/` prefix

#### 5.1.3 Auto-completion
- **Requirement**: Tab completion for commands and options
- **Scope**:
  - Command names
  - Command options/flags
  - File paths (nice-to-have)
- **Implementation**: prompt_toolkit completers via click-repl

#### 5.1.4 Basic Help System
- **Requirement**:
  - List all commands with brief descriptions
  - Detailed help for each command (`command --help`)
- **Implementation**: Click's built-in help + custom help command

#### 5.1.5 Rich Output Formatting
- **Patterns to demonstrate**:
  - **Tables**: Display data in formatted tables
  - **Panels/Boxes**: Show config in bordered boxes
  - **Colors**: Success (green), errors (red), info (blue)
  - **Progress**: Optional progress bars for long operations
  - **JSON**: Pretty-print JSON data

#### 5.1.6 Configuration Management
- **Format**: YAML
- **Location**: `config.yaml` in project root (or specified path)
- **Schema**:
  - Common base config (logging, paths)
  - Custom project config (extensible dict)
- **Operations**: load, save, show, set individual values
- **Validation**: Basic type checking (optional)

#### 5.1.7 Logging
- **Requirements**:
  - Log to file by default (`logs/app.log`)
  - Console logging in CLI mode (optional)
  - NO console logging in REPL mode (to avoid UI disruption)
  - Configurable log levels
- **Format**: Text-based, structured logs
- **Pattern**:
  ```
  2025-10-16 14:30:45 [INFO] core.processor - Processing file: data.csv
  2025-10-16 14:30:46 [ERROR] core.processor - Failed to read file: FileNotFoundError
  ```

#### 5.1.8 Multi-line Input
- **Requirement**: Support multi-line input for prompts, code, etc.
- **Trigger**: Shift+Enter continues to next line
- **Submit**: Enter (or Meta+Enter) submits
- **Use Case**: Agent prompts, SQL queries, long text

#### 5.1.9 Test Examples
- **Unit Tests**: Test core business logic functions
- **Integration Tests**: Test commands programmatically
- **Functional Tests**: Test full workflow scenarios
- **Goal**: Show how to test without REPL UI interaction

#### 5.1.10 Enhanced REPL UI (Claude Code-inspired)
- **Requirement**: Colorful, engaging REPL interface with visual polish
- **Components**:
  - **ASCII Art Welcome Screen**: Custom, configurable banner/logo
  - **Colorful Output**: Rich-formatted command output with colors, tables, panels
  - **Visual Separators**: Clear separation between command outputs
  - **Status Information**: Show config loaded, log location, ready state
  - **Friendly Feedback**: Colorful success/error messages, emojis for personality
- **Implementation**:
  - Use Rich library for all formatting
  - Template provides example ASCII art generator/customizer
  - Color scheme configurable via `ui/styles.py`
- **Advanced (Phase 2)**: Input at bottom with scrolling output above
  - Use prompt_toolkit's Application/Layout system
  - Similar to Claude Code's interface
  - Output buffer scrolls above, input stays fixed at bottom

### 5.2 Nice-to-Have Features

#### 5.2.1 Interactive List Selection
- **Package**: questionary
- **Use Case**: Choose from a list of options interactively
- **Example**: Select columns, choose mode, pick file from list
- **Pattern**:
  ```python
  import questionary

  choice = questionary.select(
      "Choose an option:",
      choices=['Option A', 'Option B', 'Option C']
  ).ask()
  ```

#### 5.2.2 Hot Reload / Module Reload
- **Requirement**: Reload core modules without restarting REPL
- **Approaches**:
  - **Simple**: `reload` command using `importlib.reload()`
  - **Advanced**: watchdog-based auto-reload on file changes
- **Scope**: Preserve REPL state (history, config, data)
- **Command**: `/reload` or `/reload module_name`

#### 5.2.3 Different Log Levels for REPL vs CLI
- **REPL**: Default to WARNING or ERROR (less noise)
- **CLI**: Default to INFO (more visibility)
- **Override**: Via config or command-line flag

---

## 6. UI/UX Patterns to Demonstrate

The template should include working examples of these patterns:

### 6.1 Simple Text Output
```python
console.print("Processing complete!")
console.print("[green]Success![/green]")
```

### 6.2 Rich Tables
```python
from rich.table import Table

table = Table(title="Results")
table.add_column("ID", style="cyan")
table.add_column("Name", style="magenta")
table.add_column("Status", style="green")
table.add_row("1", "Item A", "Complete")
console.print(table)
```

### 6.3 Config Display in Panel
```python
from rich.panel import Panel
from rich.syntax import Syntax
import yaml

config_yaml = yaml.dump(config, default_flow_style=False)
syntax = Syntax(config_yaml, "yaml", theme="monokai")
panel = Panel(syntax, title="Current Configuration", border_style="blue")
console.print(panel)
```

### 6.4 Interactive List Chooser
```python
import questionary

columns = ['col1', 'col2', 'col3', 'col4']
selected = questionary.checkbox(
    'Select columns to process:',
    choices=columns
).ask()
```

### 6.5 Error Handling Display
```python
from rich.panel import Panel

try:
    # operation
except Exception as e:
    error_panel = Panel(
        f"[red]{str(e)}[/red]",
        title="Error",
        border_style="red"
    )
    console.print(error_panel)
```

### 6.6 Progress Indication
```python
from rich.progress import track
import time

for item in track(items, description="Processing..."):
    # process item
    time.sleep(0.1)
```

---

## 7. Configuration Schema

### 7.1 Base Configuration Structure

```yaml
# Base template config
app:
  name: "My App"
  version: "1.0.0"

logging:
  level: "INFO"
  file: "logs/app.log"
  console_enabled: true  # Only for CLI mode

paths:
  input_dir: "data/input"
  output_dir: "data/output"

# Custom project configuration (extend as needed)
custom:
  # Project-specific settings go here
  example_setting: "value"
```

### 7.2 Config Manager Interface

```python
class ConfigManager:
    """Manages configuration loading, saving, and validation"""

    def load(self, path: str) -> dict:
        """Load config from YAML file"""
        pass

    def save(self, config: dict, path: str) -> None:
        """Save config to YAML file"""
        pass

    def get(self, config: dict, key: str, default=None):
        """Get nested config value using dot notation"""
        # e.g., get(config, 'logging.level') -> 'INFO'
        pass

    def set(self, config: dict, key: str, value):
        """Set nested config value using dot notation"""
        pass

    def validate(self, config: dict) -> bool:
        """Validate config structure (basic type checking)"""
        pass
```

---

## 8. Testing Strategy

### 8.1 Testing Principles
1. **Core logic is pure Python**: Can be imported and tested directly
2. **Commands are thin wrappers**: Minimal logic, mostly call core + format output
3. **Functional testing without UI**: Use click's `CliRunner` to test commands
4. **Programmatic verification**: Check outputs, return codes, exceptions

### 8.2 Test Structure

#### 8.2.1 Unit Tests (Core Logic)
```python
# tests/test_core.py
from core.processor import process_data

def test_process_data():
    """Test core processing logic without CLI"""
    config = {'mode': 'strict'}
    result = process_data('test_input.csv', config)

    assert result['status'] == 'success'
    assert result['rows'] > 0
```

#### 8.2.2 Integration Tests (Commands)
```python
# tests/test_commands.py
from click.testing import CliRunner
from app import cli

def test_process_command():
    """Test process command programmatically"""
    runner = CliRunner()

    # Run command
    result = runner.invoke(cli, ['process', '--input', 'test.csv'])

    # Verify
    assert result.exit_code == 0
    assert 'Success' in result.output
```

#### 8.2.3 Functional Tests (Workflows)
```python
# tests/test_workflows.py
def test_full_workflow():
    """Test complete workflow: load config -> process -> save results"""
    runner = CliRunner()

    # Step 1: Load config
    result = runner.invoke(cli, ['config', 'load', '--file', 'test_config.yaml'])
    assert result.exit_code == 0

    # Step 2: Process data
    result = runner.invoke(cli, ['process', '--input', 'data.csv'])
    assert result.exit_code == 0

    # Step 3: Verify outputs
    # ... assertions
```

### 8.3 Test Data Management
- **Fixtures**: Sample input files, config files in `tests/fixtures/`
- **Mocking**: Mock external dependencies (APIs, databases)
- **Isolation**: Each test uses temporary directories via `tmpdir` fixture

### 8.4 Coverage Goals
- **Core logic**: 80%+ coverage
- **Commands**: Basic smoke tests (all commands execute successfully)
- **Integration**: Key workflows covered

---

## 9. Usage Patterns

### 9.1 REPL Mode

#### Starting the REPL
```bash
# Default: start REPL with default config
python app.py

# Start with specific config
python app.py --config custom_config.yaml
```

#### REPL Session Example

**Enhanced UI with colorful welcome screen, ASCII art, and Claude Code-like interface:**

```
╔════════════════════════════════════════════════════════════════╗
║  ____  _____ ____  _       ____ _     ___                     ║
║ |  _ \| ____|  _ \| |     / ___| |   |_ _|                    ║
║ | |_) |  _| | |_) | |    | |   | |    | |                     ║
║ |  _ <| |___|  __/| |___ | |___| |___ | |                     ║
║ |_| \_\_____|_|   |_____| \____|_____|___|                    ║
║                                                                ║
║  My Awesome Application v1.0.0                                ║
║  Type /help for available commands | /quit to exit            ║
╚════════════════════════════════════════════════════════════════╝

Config loaded: config.yaml
Logging to: logs/app.log
Ready!

────────────────────────────────────────────────────────────────

> /config show
╭─────────── Current Configuration ────────────╮
│ app:                                          │
│   name: My Awesome Application                │
│   version: 1.0.0                              │
│ logging:                                      │
│   level: INFO                                 │
│   file: logs/app.log                          │
╰───────────────────────────────────────────────╯

────────────────────────────────────────────────────────────────

> /process --input data.csv
✓ Processed 150 rows in 0.45s
┏━━━━┳━━━━━━━━━━━┳━━━━━━━━━┓
┃ ID ┃ Name      ┃ Status  ┃
┡━━━━╇━━━━━━━━━━━╇━━━━━━━━━┩
│ 1  │ Record A  │ ✓ Done  │
│ 2  │ Record B  │ ✓ Done  │
└────┴───────────┴─────────┘
Output: data_processed.csv

────────────────────────────────────────────────────────────────

> /quit
Goodbye! 👋
```

**Note**: Future enhancement could move input to bottom with scrolling output above (Claude Code-style), but MVP focuses on colorful, clear output first.

### 9.2 CLI Mode

#### Single Command Execution
```bash
# Show config
python app.py config show

# Process file
python app.py process --input data.csv

# Load config and process
python app.py config load --file custom.yaml
python app.py process --input data.csv

# Get help
python app.py --help
python app.py process --help
```

#### Scripted/Automated Usage
```bash
#!/bin/bash
# automated_workflow.sh

# Load production config
python app.py config load --file prod_config.yaml

# Process all files
for file in data/*.csv; do
    python app.py process --input "$file"
done
```

### 9.3 Testing Mode (Programmatic)

```python
# test_script.py
from click.testing import CliRunner
from app import cli

runner = CliRunner()

# Test command and capture output
result = runner.invoke(cli, ['process', '--input', 'test.csv'])
print(result.output)
print(f"Exit code: {result.exit_code}")
```

---

## 10. Implementation Phases

### Phase 1: Foundation (MVP)
**Goal**: Basic working template with core architecture and colorful UI

**Deliverables**:
- [ ] Project structure with `repl_cli_template/` folder organization
- [ ] Click CLI setup with command groups
- [ ] click-repl integration for REPL mode
- [ ] **Enhanced REPL UI**:
  - [ ] ASCII art welcome screen (customizable)
  - [ ] Rich console output with colors and formatting
  - [ ] Visual separators between outputs
  - [ ] Friendly status messages
- [ ] Basic config management (load/save/show)
- [ ] Logging setup (file-based, structured with line numbers)
- [ ] `help`, `quit`, `config` commands
- [ ] One example business command (`process`)
- [ ] Basic test examples showing command testing
- [ ] README with usage instructions

**Estimated Complexity**: ~300-400 lines of template code

### Phase 2: Enhanced Features
**Goal**: Add nice-to-have features and advanced UI

**Deliverables**:
- [ ] Multi-line input support (Shift+Enter)
- [ ] Auto-completion customization
- [ ] Interactive list selection (questionary)
- [ ] More UI pattern examples (tables, progress bars, panels)
- [ ] Hot reload functionality with state preservation
- [ ] **Advanced REPL UI** (Claude Code-style):
  - [ ] Input fixed at bottom
  - [ ] Output scrolls above input
  - [ ] Bottom toolbar with status info
- [ ] Comprehensive test suite
- [ ] Advanced error handling patterns with rich formatting

**Estimated Complexity**: +200-300 lines

### Phase 3: Polish & Documentation
**Goal**: Production-ready template

**Deliverables**:
- [ ] Detailed inline documentation
- [ ] Architecture diagrams
- [ ] Tutorial: "Adding Your First Command"
- [ ] Tutorial: "Extending Configuration"
- [ ] Troubleshooting guide
- [ ] Best practices guide
- [ ] Example project using the template

---

## 11. Success Criteria

### 11.1 Functional Success
- ✓ Developer can copy template into new project in < 5 minutes
- ✓ Adding a new command takes < 10 minutes
- ✓ Same command works identically in REPL and CLI
- ✓ Functional testing possible without manual REPL interaction
- ✓ No code duplication between REPL and CLI logic
- ✓ Logging doesn't disrupt REPL UI

### 11.2 Developer Experience Success
- ✓ Template code is understandable without extensive documentation
- ✓ Clear separation between "template code" and "customize here" sections
- ✓ Minimal dependencies (< 10 packages)
- ✓ All examples actually work out of the box
- ✓ Test examples are clear and instructive

### 11.3 Extensibility Success
- ✓ Can add API layer without changing core logic
- ✓ Can add web UI without changing core logic
- ✓ Can extend config schema without breaking existing code
- ✓ Can add custom output formatters
- ✓ Can integrate with external systems (databases, APIs) cleanly

---

## 12. Open Questions & Decisions Needed

### 12.1 Command Prefix in REPL ✅ DECIDED
**Question**: Should REPL commands require `/` prefix or not?

**Decision**: Option A - Always require `/` prefix (like `/help`, `/config show`)
- **Rationale**: Keep it simple and clean. Option B adds complexity. If that proves problematic, can revisit.
- **Fallback**: If Option A creates difficulties, switch to Option B (support both)

---

### 12.2 Config Validation Level ✅ DECIDED
**Question**: How strict should config validation be?

**Decision**: Option A - No validation (YAML loads successfully = valid)
- **Rationale**: Config should override defaults. CLI args override config. Missing config elements are OK (use defaults).
- **Pattern**:
  - Defaults → Config File → CLI Args (each layer overrides the previous)
  - Core functions handle missing values gracefully

---

### 12.3 Error Handling Strategy ✅ DECIDED
**Question**: How should errors be handled in commands?

**Decision**: Option A - Let exceptions bubble up, with structured logging
- **Rationale**:
  - Commands are thin wrappers - minimal logic
  - Core functions handle validation (e.g., file existence)
  - Commands just pass args to core and format output
  - Overall try-except at command level for catchall
- **Error Logging Requirements**:
  - All errors must include: exception type, line number, and message
  - Use `logger.exception()` to capture full traceback
  - Format: `logger.exception(f"Error in {__name__}:{sys._getframe().f_lineno} - {str(e)}")`

---

### 12.4 Hot Reload Approach ✅ DECIDED
**Question**: Which reload strategy to implement?

**Decision**: Agreed with recommendation - Option A for Phase 1, Option C for Phase 2
- **Phase 1**: Manual `/reload` command using `importlib.reload()`
- **Phase 2**: Add watchdog-based auto-reload with manual override
- **Preservation**: All REPL state (history, config, data) must be preserved during reload

---

## 13. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Over-engineering template | High | Medium | Stick to MVP first, add features only if clearly needed |
| Dependencies break/change | Medium | Low | Pin versions in requirements.txt, test regularly |
| Template too opinionated | Medium | Medium | Clearly mark "customize here" sections, provide alternatives |
| Hard to update template in existing projects | Medium | High | Document "template code" vs "project code" clearly |
| Performance issues with rich output | Low | Low | Provide plain text fallback option |

---

## 14. Appendix

### 14.1 Example Core Function Signature

```python
# core/processor.py
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def process_data(input_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core business logic: process data from input file.

    This function is framework-agnostic and can be called from:
    - REPL commands
    - CLI commands
    - API endpoints
    - Web UI handlers
    - Test code

    Args:
        input_path: Path to input file
        config: Configuration dictionary

    Returns:
        Dictionary with results:
        {
            'status': 'success' | 'error',
            'rows': int,
            'output': str,
            'errors': List[str] (optional)
        }

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input file is invalid format
    """
    logger.info(f"Processing file: {input_path}")

    # Business logic here
    # ...

    result = {
        'status': 'success',
        'rows': 150,
        'output': 'output.csv'
    }

    logger.info(f"Processing complete: {result['rows']} rows")
    return result
```

### 14.2 Example Command Using Core Logic

```python
# commands/process_commands.py
import click
from rich.console import Console
from core.processor import process_data
import logging

console = Console()
logger = logging.getLogger(__name__)

@click.command()
@click.option('--input', required=True, help='Input file path')
@click.option('--output', default=None, help='Output file path (optional)')
@click.pass_context
def process(context, input, output):
    """Process data from input file"""
    try:
        # Get config from context
        config = context.obj.get('config', {})

        # Override output path if specified (CLI arg overrides config)
        if output:
            config['output_path'] = output

        # Call core business logic (handles file existence check, validation, etc.)
        result = process_data(input, config)

        # Rich formatted output
        if result['status'] == 'success':
            console.print(f"[green]✓[/green] Successfully processed {result['rows']} rows")
            console.print(f"Output written to: {result['output']}")
        else:
            console.print(f"[yellow]⚠[/yellow] Completed with warnings")
            for error in result.get('errors', []):
                console.print(f"  [yellow]•[/yellow] {error}")

    except Exception as e:
        # Catchall exception handler - core has already logged details
        console.print(f"[red]✗ Error:[/red] {str(e)}")
        logger.exception(f"Command failed: {str(e)}")
        raise click.Abort()
```

### 14.3 Logging Configuration Example

```python
# core/logging_setup.py
import logging
from pathlib import Path

def setup_logging(log_file: str, log_level: str = "INFO", console_enabled: bool = False):
    """
    Configure logging for the application.

    Args:
        log_file: Path to log file
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        console_enabled: Whether to also log to console (only for CLI mode)
    """
    # Create logs directory if it doesn't exist
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # File handler (always enabled)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level.upper()))
    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler (only for CLI mode, not REPL)
    if console_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Less verbose
        console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
```

---

## 15. Next Steps

1. **Review & Approval**: Stakeholder review of this PRD
2. **Finalize Open Questions**: Make decisions on pending questions (Section 12)
3. **Implementation Phase 1**: Build MVP template
4. **Testing & Validation**: Verify template works in real project
5. **Documentation**: Create tutorials and guides
6. **Phase 2**: Add enhanced features
7. **Example Project**: Build reference implementation

---

**Document End**
