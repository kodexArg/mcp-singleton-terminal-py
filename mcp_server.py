#!/usr/bin/env python3
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP
from terminal_singleton import TerminalSingleton

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("terminal-singleton")

# Global terminal instance
terminal = TerminalSingleton()

@mcp.tool()
async def execute_command(command: str) -> str:
    try:
        result = terminal.run(command)
        logger.info(f"Comando ejecutado: {command}")
        return result
    except Exception as e:
        error_msg = f"Error ejecutando '{command}': {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
async def get_working_directory() -> str:
    try:
        return terminal.run("pwd")
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def change_directory(path: str) -> str:
    try:
        terminal.run(f"cd {path}")
        new_dir = terminal.run("pwd")
        return f"Directorio cambiado a: {new_dir}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def get_last_output() -> str:
    try:
        return terminal.get_last_output()
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def get_full_log() -> str:
    try:
        return terminal.get_full_log()
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def close_terminal() -> str:
    try:
        terminal.close()
        return "Terminal cerrado correctamente"
    except Exception as e:
        return f"Error cerrando terminal: {str(e)}"

if __name__ == "__main__":
    logger.info("Iniciando servidor MCP Terminal Singleton")
    mcp.run(transport="stdio") 