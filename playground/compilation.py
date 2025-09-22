"""
compilation.py - Compilation logic for frontend and backend DSL files

This module handles all compilation-related functionality for the playground server.
"""

import sys
from pathlib import Path
from typing import List

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "sevdo_backend"))

from sevdo_frontend.frontend_compiler import dsl_to_jsx, load_prefabs
from backend_compiler2 import BackendCompiler


class CompilationManager:
    """Manages compilation of both frontend and backend DSL files."""

    def __init__(
        self,
        input_dir: Path,
        output_dir: Path,
        backend_input_dir: Path,
        backend_output_dir: Path,
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.backend_input_dir = backend_input_dir
        self.backend_output_dir = backend_output_dir
        self.backend_compiler = BackendCompiler()

    def compile_frontend_file(self, input_path: Path) -> bool:
        """Compile a single frontend DSL file to JSX."""
        try:
            # Read the DSL content
            dsl_content = input_path.read_text(encoding="utf-8")

            # Generate component name from filename (sanitize for JavaScript)
            base_name = input_path.stem
            # Replace spaces and special chars with underscores, capitalize each word
            component_name = (
                "".join(
                    word.title()
                    for word in base_name.replace(" ", "_").replace("-", "_").split("_")
                    if word
                )
                + "Component"
            )

            # Compile to JSX
            jsx_content = dsl_to_jsx(
                dsl_content, include_imports=True, component_name=component_name
            )

            # Write to output file
            output_path = self.output_dir / f"{input_path.stem}.jsx"
            output_path.write_text(jsx_content, encoding="utf-8")

            print(f"Compiled frontend {input_path} -> {output_path}")
            return True

        except Exception as e:
            print(f"Error compiling frontend {input_path}: {e}")
            return False

    def compile_backend_file(self, input_path: Path) -> bool:
        """Compile a single backend DSL file to FastAPI."""
        try:
            # Read the DSL content
            dsl_content = input_path.read_text(encoding="utf-8")
            tokens = dsl_content.split()

            if not tokens:
                print(f"No tokens found in {input_path}")
                return False

            # Compile to FastAPI code
            fastapi_code = self.backend_compiler.tokens_to_code(
                tokens, include_imports=True
            )

            # Write to output file
            output_path = self.backend_output_dir / f"{input_path.stem}.py"
            output_path.write_text(fastapi_code, encoding="utf-8")

            print(f"Compiled backend {input_path} -> {output_path}")
            return True

        except Exception as e:
            print(f"Error compiling backend {input_path}: {e}")
            return False

    def compile_all_frontend_files(self) -> int:
        """Compile all frontend DSL files in input directory."""
        compiled_count = 0
        for input_file in self.input_dir.glob("*.txt"):
            if self.compile_frontend_file(input_file):
                compiled_count += 1
        print(f"Compiled {compiled_count} frontend files")
        return compiled_count

    def compile_all_backend_files(self) -> int:
        """Compile all backend DSL files in backend input directory."""
        compiled_count = 0
        for input_file in self.backend_input_dir.glob("*.txt"):
            if self.compile_backend_file(input_file):
                compiled_count += 1
        print(f"Compiled {compiled_count} backend files")
        return compiled_count

    def get_frontend_file_info(self) -> List[dict]:
        """Get information about frontend files."""
        files = []
        for f in self.input_dir.glob("*.txt"):
            output_file = self.output_dir / f"{f.stem}.jsx"
            files.append(
                {
                    "name": f.stem,
                    "input_path": str(f),
                    "output_path": str(output_file),
                    "exists": output_file.exists(),
                    "last_modified": f.stat().st_mtime if f.exists() else 0,
                }
            )
        return files

    def get_backend_file_info(self) -> List[dict]:
        """Get information about backend files."""
        files = []
        for f in self.backend_input_dir.glob("*.txt"):
            output_file = self.backend_output_dir / f"{f.stem}.py"
            files.append(
                {
                    "name": f.stem,
                    "input_path": str(f),
                    "output_path": str(output_file),
                    "exists": output_file.exists(),
                    "last_modified": f.stat().st_mtime if f.exists() else 0,
                    "content": f.read_text(encoding="utf-8") if f.exists() else "",
                }
            )
        return files
