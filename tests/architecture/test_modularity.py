"""Architecture tests for ensuring modularity.

- Core imports should not include UI or visualisation libraries.
"""

import ast
from pathlib import Path

FORBIDDEN = {
    "plotly",
    "panel",
    "holoviews",
    "datashader",
    "marimo",
    "streamlit",
    "dash",
    "seaborn",
    "bokeh",
    "matplotlib",
}
EXCLUDED_DIRS = {"viz"}  # Directories allowed to use UI libraries


def test_no_ui_imports_in_core_modules():
    """Enforce QAS-007: core modules must not import UI/viz libraries."""
    src_dir = Path(__file__).parent.parent.parent / "src" / "starbox"
    violations = []

    for py_file in src_dir.rglob("*.py"):
        # Skip files in excluded directories
        if any(part in EXCLUDED_DIRS for part in py_file.parts):
            continue

        tree = ast.parse(py_file.read_text())
        for node in ast.walk(tree):
            module = None
            if isinstance(node, ast.Import):
                module = node.names[0].name
            elif isinstance(node, ast.ImportFrom) and node.module:
                module = node.module

            if module and module.split(".")[0] in FORBIDDEN:
                violations.append(f"{py_file.relative_to(src_dir)}: imports {module}")

    assert not violations, "Forbidden UI imports:\n" + "\n".join(violations)


def test_domain_code_without_viz_deps_installed():
    """Ensure core functionality without viz dependencies installed."""
    import starbox

    for name in starbox.__all__:
        getattr(starbox, name)
