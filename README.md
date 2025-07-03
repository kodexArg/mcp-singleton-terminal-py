# Terminal Singleton MCP Server

Servidor MCP que expone terminal singleton persistente para Cursor IDE.

- [Instalación](INSTALL.md)
- [Comandos](COMMANDS.md)

## Instalación

```bash
git clone <repo>
cd mcp-singleton-terminal-py
pip install -r requirements.txt
```

## Uso

1. Reinicia Cursor IDE
2. En chat: "Ejecuta ls -la" o "cd /tmp && pwd"

## Estructura

```
├── mcp_server.py           # Servidor MCP
├── terminal_singleton/     # Módulo singleton
├── .cursor/mcp.json       # Configuración
└── requirements.txt       # Dependencias
```

El terminal mantiene estado entre comandos (variables, directorio, historial). 