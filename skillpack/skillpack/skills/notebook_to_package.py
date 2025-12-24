"""notebook-to-package - Convert Jupyter notebooks to Python packages."""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any

from skillpack.utils.output import get_output_dir, write_text


def handler(args: argparse.Namespace) -> int:
    """CLI handler for notebook-to-package."""
    result = notebook_to_package_main(
        notebook_path=args.notebook,
        package_name=args.name,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated package: {result['package_name']}")
        for f in result.get("files", []):
            print(f"   - {f}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


def register_parser(subparsers: Any) -> None:
    """Register the notebook-to-package subcommand."""
    parser = subparsers.add_parser(
        "notebook-to-package",
        help="Convert Jupyter notebooks to Python packages",
    )
    parser.add_argument(
        "--notebook",
        type=Path,
        required=True,
        help="Path to Jupyter notebook (.ipynb)",
    )
    parser.add_argument(
        "--name",
        help="Package name (defaults to notebook name)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/notebook_to_package"),
        help="Output directory",
    )
    parser.set_defaults(handler=handler)


def notebook_to_package_main(
    notebook_path: Path,
    package_name: str | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Convert a Jupyter notebook to a Python package."""
    if output_dir is None:
        output_dir = get_output_dir("notebook_to_package")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    if not notebook_path.exists():
        return {"success": False, "error": f"Notebook not found: {notebook_path}"}

    if package_name is None:
        package_name = notebook_path.stem.replace("-", "_").replace(" ", "_").lower()

    try:
        # Parse notebook
        with open(notebook_path, encoding="utf-8") as f:
            notebook = json.load(f)

        cells = notebook.get("cells", [])
        
        # Extract code and organize
        modules = extract_modules(cells, package_name)
        
        files = []
        
        # Generate package __init__.py
        init_code = generate_init(package_name, modules)
        write_text(content=init_code, filename=f"{package_name}/__init__.py", skill_name="notebook_to_package")
        files.append(f"{package_name}/__init__.py", output_dir=output_dir)

        # Generate main module
        main_code = generate_main_module(cells, package_name)
        write_text(content=main_code, filename=f"{package_name}/core.py", skill_name="notebook_to_package")
        files.append(f"{package_name}/core.py", output_dir=output_dir)

        # Generate utils module
        utils_code = generate_utils_module(cells)
        write_text(content=utils_code, filename=f"{package_name}/utils.py", skill_name="notebook_to_package")
        files.append(f"{package_name}/utils.py", output_dir=output_dir)

        # Generate CLI entry point
        cli_code = generate_cli(package_name)
        write_text(content=cli_code, filename=f"{package_name}/cli.py", skill_name="notebook_to_package")
        files.append(f"{package_name}/cli.py", output_dir=output_dir)

        # Generate pyproject.toml
        pyproject = generate_pyproject(package_name, cells)
        write_text(content=pyproject, filename="pyproject.toml", skill_name="notebook_to_package")
        files.append("pyproject.toml", output_dir=output_dir)

        # Generate README
        readme = generate_readme(package_name, cells)
        write_text(content=readme, filename="README.md", skill_name="notebook_to_package")
        files.append("README.md", output_dir=output_dir)

        return {
            "success": True,
            "package_name": package_name,
            "output_dir": str(output_dir),
            "files": files,
            "cell_count": len(cells),
        }

    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid notebook format"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def extract_modules(cells: list[dict], package_name: str) -> dict[str, list[str]]:
    """Extract code into logical modules."""
    modules = {"imports": [], "functions": [], "classes": [], "main": []}
    
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        
        # Categorize code
        for line in source.split("\n"):
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")):
                modules["imports"].append(line)
            elif stripped.startswith("def "):
                modules["functions"].append(source)
                break
            elif stripped.startswith("class "):
                modules["classes"].append(source)
                break
    
    return modules


def generate_init(package_name: str, modules: dict) -> str:
    """Generate __init__.py."""
    return dedent(f'''\
        """{package_name} - Generated from Jupyter notebook.
        
        Generated by skillpack notebook-to-package on {datetime.now().strftime("%Y-%m-%d %H:%M")}
        """

        from {package_name}.core import *
        from {package_name}.utils import *

        __version__ = "0.1.0"
        __all__ = ["main", "run"]
    ''')


def generate_main_module(cells: list[dict], package_name: str) -> str:
    """Generate core.py with main logic."""
    code_cells = [c for c in cells if c.get("cell_type") == "code"]
    
    # Extract imports
    imports = set()
    functions = []
    other_code = []
    
    for cell in code_cells:
        source = "".join(cell.get("source", []))
        lines = source.split("\n")
        
        in_function = False
        current_function = []
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith(("import ", "from ")):
                imports.add(line)
            elif stripped.startswith("def ") or in_function:
                in_function = True
                current_function.append(line)
                if line.strip() and not line.startswith(" ") and not stripped.startswith("def "):
                    functions.append("\n".join(current_function[:-1]))
                    in_function = False
                    current_function = []
                    other_code.append(line)
            elif not stripped.startswith("#") and stripped:
                other_code.append(line)
        
        if current_function:
            functions.append("\n".join(current_function))
    
    imports_str = "\n".join(sorted(imports))
    functions_str = "\n\n\n".join(functions) if functions else "pass"
    
    return dedent(f'''\
        """{package_name} core module.
        
        Generated from Jupyter notebook on {datetime.now().strftime("%Y-%m-%d %H:%M")}
        """

{imports_str}


{functions_str}


def main():
    """Main entry point."""
    print("Running {package_name}...")
    # TODO: Add main logic from notebook
    

def run(**kwargs):
    """Run with keyword arguments."""
    return main()


if __name__ == "__main__":
    main()
    ''')


def generate_utils_module(cells: list[dict]) -> str:
    """Generate utils.py with helper functions."""
    return dedent(f'''\
        """{datetime.now().strftime("%Y-%m-%d %H:%M")} - Utility functions."""

        import logging
        from pathlib import Path
        from typing import Any


        logger = logging.getLogger(__name__)


        def setup_logging(level: str = "INFO") -> None:
            """Configure logging."""
            logging.basicConfig(
                level=getattr(logging, level.upper()),
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )


        def load_data(path: Path) -> Any:
            """Load data from file."""
            import pandas as pd
            
            suffix = path.suffix.lower()
            if suffix == ".csv":
                return pd.read_csv(path)
            elif suffix == ".parquet":
                return pd.read_parquet(path)
            elif suffix == ".json":
                return pd.read_json(path)
            else:
                raise ValueError(f"Unsupported format: {{suffix}}")


        def save_data(data: Any, path: Path) -> None:
            """Save data to file."""
            path.parent.mkdir(parents=True, exist_ok=True)
            
            suffix = path.suffix.lower()
            if suffix == ".csv":
                data.to_csv(path, index=False)
            elif suffix == ".parquet":
                data.to_parquet(path, index=False)
            elif suffix == ".json":
                data.to_json(path, orient="records")
            else:
                raise ValueError(f"Unsupported format: {{suffix}}")
    ''')


def generate_cli(package_name: str) -> str:
    """Generate CLI module."""
    return dedent(f'''\
        """Command-line interface for {package_name}."""

        import argparse
        import sys
        from pathlib import Path

        from {package_name}.core import main
        from {package_name}.utils import setup_logging


        def create_parser() -> argparse.ArgumentParser:
            parser = argparse.ArgumentParser(
                prog="{package_name}",
                description="{package_name} - converted from Jupyter notebook",
            )
            parser.add_argument(
                "-v", "--verbose",
                action="store_true",
                help="Enable verbose output",
            )
            parser.add_argument(
                "--input",
                type=Path,
                help="Input file path",
            )
            parser.add_argument(
                "--output",
                type=Path,
                default=Path("./output"),
                help="Output directory",
            )
            return parser


        def cli_main() -> int:
            parser = create_parser()
            args = parser.parse_args()
            
            setup_logging("DEBUG" if args.verbose else "INFO")
            
            try:
                main()
                return 0
            except Exception as e:
                print(f"Error: {{e}}", file=sys.stderr)
                return 1


        if __name__ == "__main__":
            sys.exit(cli_main())
    ''')


def generate_pyproject(package_name: str, cells: list[dict]) -> str:
    """Generate pyproject.toml."""
    # Extract dependencies from imports
    deps = set()
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        for line in source.split("\n"):
            if line.strip().startswith(("import ", "from ")):
                # Extract package name
                match = re.match(r"(?:from|import)\s+(\w+)", line.strip())
                if match:
                    pkg = match.group(1)
                    if pkg not in ("os", "sys", "re", "json", "typing", "pathlib", "collections", "itertools", "functools"):
                        deps.add(pkg.lower())
    
    deps_str = ",\n    ".join([f'"{d}"' for d in sorted(deps)]) if deps else ""
    
    return dedent(f'''\
        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"

        [project]
        name = "{package_name}"
        version = "0.1.0"
        description = "{package_name} - converted from Jupyter notebook"
        requires-python = ">=3.10"
        dependencies = [
            {deps_str}
        ]

        [project.scripts]
        {package_name} = "{package_name}.cli:cli_main"

        [tool.hatch.build.targets.wheel]
        packages = ["{package_name}"]
    ''')


def generate_readme(package_name: str, cells: list[dict]) -> str:
    """Generate README.md."""
    # Extract markdown cells for documentation
    docs = []
    for cell in cells:
        if cell.get("cell_type") == "markdown":
            docs.append("".join(cell.get("source", [])))
    
    docs_section = "\n\n".join(docs[:3]) if docs else "No documentation found in notebook."
    
    return dedent(f'''\
        # {package_name}

        Generated from Jupyter notebook by skillpack notebook-to-package.

        ## Installation

        ```bash
        pip install -e .
        ```

        ## Usage

        ### As a module
        ```python
        from {package_name} import main
        main()
        ```

        ### From command line
        ```bash
        {package_name} --input data.csv --output ./results
        ```

        ## Original Notebook Documentation

        {docs_section}
    ''')
