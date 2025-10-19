# Key Decisions Summary

**Project**: Python REPL/CLI Template
**Date**: 2025-10-16

---

## Technical Stack (APPROVED)

✅ **Core Dependencies**:
- click (CLI framework)
- click-repl (REPL mode)
- rich (beautiful terminal output)
- prompt_toolkit (via click-repl - history, completion, multi-line)
- PyYAML (config persistence)

✅ **Optional Dependencies**:
- questionary (interactive prompts)
- watchdog (hot reload - Phase 2)

❌ **Rejected**:
- Textual (too complex, overkill for our needs)
- Ravel (couldn't find/verify, possibly unmaintained)

---

## Architecture Decisions

### 1. Folder Structure ✅

```
project_root/
├── repl_cli_template/    # All template code here
│   ├── commands/         # UI layer (not "cli" folder)
│   ├── core/             # Business logic
│   ├── ui/               # REPL UI components (welcome, styles)
│   └── tests/
├── config.yaml           # Project root
└── logs/                 # Project root
```

**Rationale**:
- Everything framework-related in `repl_cli_template/`
- Logs at project root for easy access
- `commands/` represents UI layer (serves both REPL and CLI)

---

### 2. Command Prefix in REPL ✅

**Decision**: Always require `/` prefix (e.g., `/help`, `/config show`)

**Rationale**:
- Keeps implementation simple and clean
- Option B (support both) adds complexity
- Can revisit if this creates problems

**Fallback**: Switch to supporting both with/without `/` if needed

---

### 3. Configuration Validation ✅

**Decision**: No validation - if YAML loads, it's valid

**Rationale**:
- Config overrides defaults
- CLI args override config
- Missing config elements are OK (use defaults)
- Core functions handle missing values gracefully

**Hierarchy**:
```
Defaults → Config File → CLI Args
(each layer overrides the previous)
```

---

### 4. Error Handling ✅

**Decision**: Let exceptions bubble up with structured logging

**Pattern**:
- Commands are **thin wrappers** - minimal logic
- **Core functions** handle all validation (file existence, format checks, etc.)
- Commands just pass args to core and format output
- Overall try-except at command level as catchall

**Error Logging Requirements**:
- All errors must include: **exception type, line number, message**
- Use `logger.exception()` to capture full traceback
- Format: `logger.exception(f"Error in {__name__}:{sys._getframe().f_lineno} - {str(e)}")`

**Example**:
```python
@click.command()
def process(context, input):
    try:
        # Core handles file validation
        result = process_data(input, config)
        console.print(f"[green]✓[/green] Success!")
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")
        logger.exception(f"Command failed: {str(e)}")
        raise click.Abort()
```

---

### 5. Hot Reload ✅

**Decision**:
- **Phase 1**: Manual `/reload` command using `importlib.reload()`
- **Phase 2**: Add watchdog auto-reload with manual override

**Requirements**:
- Preserve all REPL state (history, config, data) during reload
- Clear indication when reload occurs
- Option to reload specific modules

---

### 6. Variable Naming ✅

**Decision**: Use descriptive, full variable names

**Examples**:
- ✅ `context` (not `ctx`)
- ✅ `configuration` or `config` (not `cfg`)
- ✅ `input_file` (not `inf`)

**Rationale**: Code readability over brevity

---

### 7. REPL UI Enhancement ✅

**Decision**: Colorful, engaging UI is a **must-have for Phase 1**

**Phase 1 Requirements**:
- ✅ ASCII art welcome screen (customizable)
- ✅ Rich-formatted output (colors, tables, panels)
- ✅ Visual separators between command outputs
- ✅ Status information (config loaded, log location)
- ✅ Friendly feedback (emojis, colors)

**Phase 2 Enhancement**:
- Input at bottom, scrolling output above (Claude Code-style)
- Bottom toolbar with status
- Uses prompt_toolkit's Application/Layout system

**Rationale**:
- Current example (Section 9.1) was "boring"
- Claude Code UI is impressive and engaging
- Good UI encourages usage and makes debugging easier

---

### 8. Auto-Completion Strategy ✅

**Decision**: Claude Code-style slash command completion with live filtering

**Implementation**:
- Custom `SlashCommandCompleter` using prompt_toolkit
- Completions appear as you type after `/`
- Live filtering as more characters are typed
- Backspace automatically refilters
- Support for subcommands (e.g., `/config show`)
- Support for options (e.g., `/config load --file`)
- Prefer long-form options (`--file`) over short (`-f`) when both exist
- Single column layout (one command per line)
- No background colors, bright highlighting for selected item

**Design Decisions**:
- Use standard prompt_toolkit behavior (`complete_while_typing=True`)
- No custom key bindings - use defaults (Tab, Enter, Arrow keys, Backspace)
- Accept that completions insert text (don't fight the framework)
- Transparent backgrounds with colored text for better visibility

**Rationale**:
- Claude Code provides excellent UX model
- Fighting prompt_toolkit defaults creates more problems than it solves
- Standard behavior is predictable and well-tested
- Auto-discovery of subcommands and options from Click command structure

---

## Design Principles

1. **Define once, use everywhere**: Commands work in REPL, CLI, and future API/Web
2. **Thin commands**: Minimal logic in commands, all validation in core
3. **Config hierarchy**: Defaults → Config File → CLI Args
4. **No validation**: Trust YAML, handle missing gracefully
5. **Structured errors**: Always log type + line + message
6. **Visual appeal**: Colorful, clear output is not optional

---

## What We're NOT Building

❌ Pip-installable package
❌ User home directory configs
❌ Abstract base classes
❌ Plugin systems
❌ Full TUI framework
❌ CLI as subset of REPL (they share same commands)

---

## Success Criteria

✅ Copy template to new project in < 5 minutes
✅ Add new command in < 10 minutes
✅ Same command works in REPL and CLI
✅ Can test functionally without UI interaction
✅ No code duplication
✅ Logging doesn't disrupt REPL UI
✅ Template code is understandable
✅ All examples work out of the box

---

**Document Version**: 1.0
**Status**: Approved for Phase 1 Implementation
