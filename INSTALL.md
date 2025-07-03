# Instalación

## 1. Clonar repositorio

```bash
git clone <repo>
cd mcp-singleton-terminal-py
```

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3. Configurar en Cursor IDE

El archivo `.cursor/mcp.json` ya está configurado:

```json
{
  "mcpServers": {
    "terminal-singleton": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "."
    }
  }
}
```

## 4. Reiniciar Cursor IDE

Reinicia completamente Cursor IDE para cargar la configuración MCP.

## 5. Verificar

En el chat de Cursor, ejecuta: "Ejecuta ls -la" 