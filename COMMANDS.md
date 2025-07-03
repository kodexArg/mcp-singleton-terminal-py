# Comandos

## execute_command
- **Uso**: `execute_command(command: str)`
- **Función**: Ejecuta cualquier comando en el terminal singleton
- **Ejemplo**: `execute_command("ls -la")`

## get_working_directory
- **Uso**: `get_working_directory()`
- **Función**: Obtiene el directorio de trabajo actual
- **Ejemplo**: `get_working_directory()`

## change_directory
- **Uso**: `change_directory(path: str)`
- **Función**: Cambia el directorio de trabajo
- **Ejemplo**: `change_directory("/tmp")`

## get_last_output
- **Uso**: `get_last_output()`
- **Función**: Obtiene la salida del último comando ejecutado
- **Ejemplo**: `get_last_output()`

## get_full_log
- **Uso**: `get_full_log()`
- **Función**: Obtiene todo el historial de comandos y salidas de la sesión
- **Ejemplo**: `get_full_log()`

## close_terminal
- **Uso**: `close_terminal()`
- **Función**: Cierra limpiamente el terminal singleton
- **Ejemplo**: `close_terminal()`

## Características del terminal

- **Persistencia**: El terminal mantiene estado entre comandos
- **Variables**: Las variables de entorno persisten
- **Directorio**: El directorio actual se mantiene
- **Historial**: Se conserva el historial de comandos 