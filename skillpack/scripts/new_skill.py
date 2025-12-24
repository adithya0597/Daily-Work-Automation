#!/usr/bin/env python3
"""Scaffold a new skill with all required files.

This script creates the folder structure and template files for a new skill.

Usage:
    python scripts/new_skill.py <skill-name> --description "Description"
"""

import argparse
import sys
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).parent.parent


def create_skill(name: str, description: str) -> None:
    """Create a new skill with all required files."""
    # Convert to directory name
    dir_name = name.replace("-", "_")
    module_name = dir_name

    skills_dir = REPO_ROOT / "skills" / dir_name
    package_dir = REPO_ROOT / "skillpack" / "skills"
    tests_dir = REPO_ROOT / "tests"

    # Create directories
    skills_dir.mkdir(parents=True, exist_ok=True)
    (skills_dir / "docs").mkdir(exist_ok=True)
    (skills_dir / "scripts").mkdir(exist_ok=True)
    (skills_dir / "examples").mkdir(exist_ok=True)

    print(f"Creating skill: {name}")
    print(f"  Directory: {skills_dir}")

    # Create metadata.yaml
    metadata = dedent(f"""\
        name: {name}
        version: "1.0.0"
        description: {description}
        tags: []

        triggers:
          - "TODO: add natural language triggers"

        dependencies: []

        command:
          binary: skillpack
          subcommand: {name}
          template: "skillpack {name} --input {{input_path}}"

        arguments:
          input_path:
            type: file_path
            required: true
            cli_name: "--input"
            description: Input file path

        output:
          directory: "./out/{dir_name}/"
          files:
            - output.txt
    """)
    (skills_dir / "metadata.yaml").write_text(metadata)
    print(f"  Created: metadata.yaml")

    # Create skill.md
    skill_md = dedent(f"""\
        # {name.replace('-', ' ').title()} Skill

        ## When to Use
        - TODO: Add trigger conditions

        ## Inputs
        | Name | Type | Required | Description |
        |------|------|----------|-------------|
        | input_path | file_path | Yes | Input file |

        ## Outputs
        | File | Format | Description |
        |------|--------|-------------|
        | output.txt | text | Output file |

        ## Procedure
        1. **Step 1** - TODO
        2. **Step 2** - TODO

        ## Guardrails

        ### Allowed
        - TODO: What the skill CAN do

        ### Forbidden
        - TODO: What the skill MUST NOT do

        ## Preconditions
        - [ ] Input file exists

        ## Postconditions
        - [ ] Output file created

        ## Error Handling
        | Error | Condition | Recovery |
        |-------|-----------|----------|
        | FileNotFoundError | Input missing | Check path |

        ## Examples
        ```bash
        skillpack {name} --input file.txt
        ```

        ## Related Skills
        - TODO
    """)
    (skills_dir / "skill.md").write_text(skill_md)
    print(f"  Created: skill.md")

    # Create Python module
    module = dedent(f'''\
        """{name} - {description}"""

        import argparse
        from pathlib import Path
        from typing import Any

        from skillpack.utils.output import get_output_dir, safe_write_file


        def handler(args: argparse.Namespace) -> int:
            """CLI handler for {name}."""
            result = {module_name}_main(
                input_path=args.input,
            )

            if result.get("success"):
                print(f"✅ Output written to {{result['output_dir']}}")
                return 0
            print(f"❌ Error: {{result.get('error')}}")
            return 1


        def register_parser(subparsers: Any) -> None:
            """Register the {name} subcommand."""
            parser = subparsers.add_parser(
                "{name}",
                help="{description}",
            )
            parser.add_argument(
                "--input",
                type=Path,
                required=True,
                help="Input file path",
            )
            parser.set_defaults(handler=handler)


        def {module_name}_main(
            input_path: Path,
            output_dir: Path | None = None,
        ) -> dict[str, Any]:
            """Main implementation for {name}."""
            if output_dir is None:
                output_dir = get_output_dir("{dir_name}")

            try:
                # Validate input
                if not input_path.exists():
                    return {{"success": False, "error": f"File not found: {{input_path}}"}}

                # TODO: Implement skill logic
                content = input_path.read_text()

                # Write output
                output_file = output_dir / "output.txt"
                safe_write_file(output_file, f"Processed: {{content}}")

                return {{
                    "success": True,
                    "output_dir": output_dir,
                    "files": [str(output_file)],
                }}

            except Exception as e:
                return {{"success": False, "error": str(e)}}
    ''')
    (package_dir / f"{module_name}.py").write_text(module)
    print(f"  Created: skillpack/skills/{module_name}.py")

    # Create wrapper script
    wrapper = dedent(f'''\
        #!/usr/bin/env python3
        """Thin wrapper script for {name} skill."""

        import argparse
        import sys
        from pathlib import Path

        SKILLPACK_ROOT = Path(__file__).parent.parent.parent.parent / "skillpack"
        if str(SKILLPACK_ROOT) not in sys.path:
            sys.path.insert(0, str(SKILLPACK_ROOT.parent))

        from skillpack.skills.{module_name} import {module_name}_main


        def main() -> int:
            parser = argparse.ArgumentParser(description="{description}")
            parser.add_argument("--input", type=Path, required=True)
            parser.add_argument("--output-dir", type=Path, default=Path("./out/{dir_name}"))
            args = parser.parse_args()

            result = {module_name}_main(
                input_path=args.input,
                output_dir=args.output_dir,
            )

            if result.get("success"):
                print(f"✅ Generated files in {{args.output_dir}}")
                return 0
            print(f"❌ Error: {{result.get('error')}}")
            return 1


        if __name__ == "__main__":
            sys.exit(main())
    ''')
    (skills_dir / "scripts" / "run_skill.py").write_text(wrapper)
    print(f"  Created: scripts/run_skill.py")

    # Create test file
    test = dedent(f'''\
        """Tests for {name} skill."""

        import tempfile
        from pathlib import Path

        import pytest

        from skillpack.skills.{module_name} import {module_name}_main


        def test_basic_functionality() -> None:
            """Test core functionality."""
            with tempfile.TemporaryDirectory() as tmpdir:
                # Create test input
                input_file = Path(tmpdir) / "input.txt"
                input_file.write_text("test content")

                result = {module_name}_main(
                    input_path=input_file,
                    output_dir=Path(tmpdir),
                )

                assert result["success"]
                assert (Path(tmpdir) / "output.txt").exists()


        def test_file_not_found() -> None:
            """Test error handling for missing file."""
            result = {module_name}_main(
                input_path=Path("nonexistent.txt"),
            )
            assert not result["success"]
            assert "not found" in result.get("error", "").lower()
    ''')
    (tests_dir / f"test_{module_name}.py").write_text(test)
    print(f"  Created: tests/test_{module_name}.py")

    # Print next steps
    print()
    print("=" * 60)
    print("Next Steps")
    print("=" * 60)
    print(f"""
1. Edit skillpack/cli.py to register the skill:
   - Add import: from skillpack.skills import {module_name}
   - Add registration: {module_name}.register_parser(subparsers)

2. Implement the skill logic in:
   skillpack/skills/{module_name}.py

3. Update skill.md with proper documentation

4. Run tests:
   python -m pytest tests/test_{module_name}.py -v

5. Validate:
   python scripts/validate_skills.py --skill {name}
""")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a new skillpack skill"
    )
    parser.add_argument(
        "name",
        help="Skill name (use hyphens, e.g., my-new-skill)",
    )
    parser.add_argument(
        "--description",
        default="A new skill",
        help="Brief description of the skill",
    )

    args = parser.parse_args()

    # Validate name
    if "_" in args.name:
        print("Error: Use hyphens not underscores in skill name")
        return 1

    create_skill(args.name, args.description)
    return 0


if __name__ == "__main__":
    sys.exit(main())
