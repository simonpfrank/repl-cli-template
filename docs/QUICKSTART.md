# Quick Start Guide

Get up and running with the REPL/CLI Template in 5 minutes!

## Step 1: Install Dependencies

```bash
cd /path/to/repl_cli_template
pip install -r requirements.txt
```

## Step 2: Try the REPL

```bash
python -m repl_cli_template.app
```

You should see a colorful welcome screen!

## Step 3: Try Some Commands

In the REPL, type:

```
> /help
```

Show the current config:
```
> /config show
```

Create a test file and process it:
```bash
# First, exit the REPL
> /quit

# Create a sample input file
mkdir -p data/input
echo -e "hello\nworld\ntest" > data/input/sample.txt

# Start REPL again
python -m repl_cli_template.app

# Process the file
> /process --input data/input/sample.txt
```

## Step 4: Try CLI Mode

```bash
# Show config (no REPL)
python -m repl_cli_template.app config show

# Process file (no REPL)
python -m repl_cli_template.app process --input data/input/sample.txt
```

## Step 5: Run Tests

```bash
pytest repl_cli_template/tests/
```

## Next Steps

1. **Customize the welcome screen**: Edit `repl_cli_template/ui/welcome.py`
2. **Add your first command**: See README.md "Adding a New Command"
3. **Add your business logic**: Create modules in `repl_cli_template/core/`
4. **Customize config**: Edit `config.yaml`

## Common First Customizations

### Change the App Name

Edit `config.yaml`:
```yaml
app:
  name: "My Awesome App"
  version: "1.0.0"
```

### Change ASCII Art

Visit http://patorjk.com/software/taag/ and generate new ASCII art, then paste into `repl_cli_template/ui/welcome.py`.

### Add a Custom Command

1. Create `repl_cli_template/commands/my_command.py`
2. Define your command using `@click.command()`
3. Register it in `repl_cli_template/app.py` with `cli.add_command()`

See README.md for detailed examples!

---

**Need Help?** Check the README.md for full documentation.
