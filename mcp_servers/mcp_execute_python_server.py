import os
import subprocess
import sys

from mcp.server.mcpserver import MCPServer

mcp: MCPServer = MCPServer("SuperServer")


@mcp.tool()
def read_local_file(file_path: str) -> str:
    """Reads the content of a local text file. Provide the full path."""
    if not os.path.exists(file_path):
        return f"Error: File at {file_path} not found."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e!s}"


@mcp.tool()
def execute_python_code(
    code: str | None = None,
    file_path: str | None = None,
    script_name: str | None = None,
) -> str:
    """
    Executes Python code or a script.
    Accepts 'code' (string), 'file_path' (path), or 'script_name' (filename).
    """
    scripts_dir = os.path.abspath("scripts")

    # 1. Resolve which input the model actually gave us
    # This catches cases where the LLM hallucinates the parameter name
    input_content = code or file_path or script_name

    if not input_content:
        return (
            "Error: No code or filename provided. Please provide the 'code' parameter."
        )

    # Setup environment
    env = os.environ.copy()
    env["PYTHONPATH"] = scripts_dir

    # 2. Check if the resolved input is a file on disk
    potential_file = os.path.join(scripts_dir, os.path.basename(input_content.strip()))

    try:
        if input_content.strip().endswith(".py") and os.path.exists(potential_file):
            # CASE A: Run existing file
            command = [sys.executable, potential_file]
        else:
            # CASE B: Execute raw string
            # If the model passed a file path but it didn't exist, we treat the path
            # as the code string (which will likely fail, but it's the safest fallback)
            command = [sys.executable, "-c", input_content]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=scripts_dir,
            env=env,
        )

        if result.stderr:
            return f"Execution Error:\n{result.stderr}"
        return f"Output:\n{result.stdout}" if result.stdout else "Success (No output)."

    except Exception as e:
        return f"Error: {e!s}"


@mcp.tool()
def add(a: float, b: float) -> float:
    """Adds two numbers and returns the sum."""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers and returns the product."""
    return a * b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raises base to the power of exponent and returns the result."""
    return base**exponent


if __name__ == "__main__":
    # Security settings that allow local development are passed when the server starts
    mcp.run(
        transport="sse",
        host="127.0.0.1",
        port=54321,
    )
