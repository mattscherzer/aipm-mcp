from mcp.server.mcpserver import MCPServer

mcp: MCPServer = MCPServer("MathServer")


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b


if __name__ == "__main__":
    # Force SSE transport to bypass Windows stdio pipe limits
    print("🚀 Starting Math Server on http://127.0.0.1:54321/sse ...")
    # The host and port are set when the server starts
    mcp.run(transport="sse", host="127.0.0.1", port=54321)
