# Adding a New Skill to Skillpack

This guide ensures all new skills follow the established architecture and stay in sync with the project structure.

## Quick Checklist

```
[ ] 1. Create skill folder structure
[ ] 2. Implement core logic in skillpack/skills/
[ ] 3. Create metadata.yaml
[ ] 4. Create skill.md
[ ] 5. Register in CLI
[ ] 6. Add tests
[ ] 7. Create wrapper script
[ ] 8. Validate dependencies
[ ] 9. Update README
```

---

## Step 1: Create Skill Folder Structure

```bash
mkdir -p skills/<skill_name>/{docs,scripts,examples}
```

Required structure:
```
skills/<skill_name>/
├── metadata.yaml     # REQUIRED (Tier 1)
├── skill.md          # REQUIRED (Tier 2)
├── docs/             # OPTIONAL but recommended
├── scripts/          # RECOMMENDED (thin wrapper)
└── examples/         # RECOMMENDED
```

---

## Step 2: Implement Core Logic

Create `skillpack/skills/<skill_name>.py`:

```python
"""<skill_name> - Brief description."""

import argparse
from pathlib import Path
from typing import Any

from skillpack.utils.output import safe_write_file, get_output_dir


def handler(args: argparse.Namespace) -> int:
    """CLI handler for <skill_name>."""
    # Your implementation
    result = do_skill_work(...)
    
    if result.get("success"):
        return 0
    return 1


def register_parser(subparsers: Any) -> None:
    """Register the <skill_name> subcommand."""
    parser = subparsers.add_parser(
        "<skill-name>",  # CLI name with hyphens
        help="Brief description",
    )
    # Add arguments
    parser.add_argument("--input", required=True, help="Input file")
    parser.set_defaults(handler=handler)


# Core function (called by handler AND wrapper script)
def do_skill_work(...) -> dict[str, Any]:
    """Core implementation - can be imported by wrapper script."""
    output_dir = get_output_dir("<skill_name>")
    # Implementation
    return {"success": True, "files": [...]}
```

---

## Step 3: Create metadata.yaml

```yaml
name: <skill-name>
version: "1.0.0"
description: One-line description of what this skill does
tags: [tag1, tag2, tag3]

triggers:
  - "natural language trigger 1"
  - "natural language trigger 2"

dependencies: []  # Or list skills this depends on

command:
  binary: skillpack
  subcommand: <skill-name>
  template: "skillpack <skill-name> --input {input_path}"

arguments:
  input_path:
    type: file_path
    required: true
    cli_name: "--input"
    description: Description of the argument
    validation:
      file_must_exist: true

output:
  directory: "./out/<skill_name>/"
  files:
    - output_file.ext
```

---

## Step 4: Create skill.md

Use this template (all sections required):

```markdown
# <Skill Name> Skill

## When to Use
- Trigger condition 1
- Trigger condition 2

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| input_path | file_path | Yes | Description |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| output.ext | format | Description |

## Procedure
1. **Step 1** - Description
2. **Step 2** - Description

## Guardrails

### Allowed
- What the skill CAN do

### Forbidden
- What the skill MUST NOT do

## Preconditions
- [ ] Condition that must be true

## Postconditions
- [ ] Guaranteed after success

## Error Handling
| Error | Condition | Recovery |
|-------|-----------|----------|
| ErrorName | When it occurs | How to fix |

## Examples
```bash
skillpack <skill-name> --input file.txt
```

## Related Skills
- **other-skill**: Why it's related
```

---

## Step 5: Register in CLI

Edit `skillpack/cli.py`:

```python
from skillpack.skills import (
    # ... existing imports
    <skill_name>,  # Add import
)

def create_parser() -> argparse.ArgumentParser:
    # ... existing code
    
    # Add registration (in appropriate section)
    <skill_name>.register_parser(subparsers)
```

---

## Step 6: Add Tests

Create `tests/test_<skill_name>.py`:

```python
"""Tests for <skill_name> skill."""

import tempfile
from pathlib import Path

import pytest

from skillpack.skills.<skill_name> import (
    do_skill_work,
    # other functions
)


def test_basic_functionality() -> None:
    """Test core functionality."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = do_skill_work(
            input_path=Path("test_input"),
            output_dir=Path(tmpdir),
        )
        assert result["success"]


def test_error_handling() -> None:
    """Test error cases."""
    with pytest.raises(FileNotFoundError):
        do_skill_work(input_path=Path("nonexistent"))
```

---

## Step 7: Create Wrapper Script

Create `skills/<skill_name>/scripts/run_skill.py`:

```python
#!/usr/bin/env python3
"""Thin wrapper script for <skill-name> skill.

Usage:
    python run_skill.py --input INPUT_PATH
"""

import argparse
import sys
from pathlib import Path

SKILLPACK_ROOT = Path(__file__).parent.parent.parent.parent / "skillpack"
if str(SKILLPACK_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLPACK_ROOT.parent))

from skillpack.skills.<skill_name> import do_skill_work


def main() -> int:
    parser = argparse.ArgumentParser(description="Description")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("./out/<skill_name>"))
    args = parser.parse_args()

    result = do_skill_work(
        input_path=args.input,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated files in {args.output_dir}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## Step 8: Validate

```bash
# Run all tests
python -m pytest tests/ -v

# Verify skill appears in list
skillpack list-skills

# Test the skill
skillpack <skill-name> --help
skillpack <skill-name> --input test_file

# Validate dependencies
python -c "from skillpack.utils.skill_loader import validate_all_dependencies; print(validate_all_dependencies())"
```

---

## Step 9: Update README

Add entry in README.md under Skills section:

```markdown
### <skill-name>

Description of what the skill does.

```bash
skillpack <skill-name> --input file.txt
```
```

---

## Validation Script

Run this to check your new skill:

```bash
python -c "
from skillpack.utils.skill_loader import (
    load_skill,
    get_skill_guardrails,
    validate_dependencies,
)

skill_name = '<skill-name>'
skill = load_skill(skill_name)

# Check required fields
assert skill.get('name'), 'Missing name in metadata.yaml'
assert skill.get('description'), 'Missing description'
assert skill.get('skill_md'), 'Missing skill.md'

# Check guardrails exist
guardrails = get_skill_guardrails(skill_name)
assert guardrails['allowed'], 'Missing allowed guardrails'
assert guardrails['forbidden'], 'Missing forbidden guardrails'

# Validate dependencies
deps = validate_dependencies(skill_name)
assert deps['valid'], f'Invalid dependencies: {deps[\"warnings\"]}'

print('✅ Skill validation passed!')
"
```
