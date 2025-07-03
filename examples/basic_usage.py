#!/usr/bin/env python3
"""
Ejemplo básico de uso del TerminalSingleton

Demuestra las funcionalidades principales:
- Ejecución de comandos
- Recuperación de output del último comando
- Consulta del historial completo
- Persistencia del estado del shell
"""

from terminal_singleton import TerminalSingleton


def main():
    """Ejemplo de uso básico del TerminalSingleton."""
    
    # Crear instancia (singleton)
    terminal = TerminalSingleton()
    
    print("=== Ejemplo 1: Comandos básicos ===")
    
    # Ejecutar comando simple
    output = terminal.run("pwd")
    print(f"Directorio actual: {output}")
    
    # Ejecutar varios comandos
    terminal.run("ls -la")
    print(f"Listado de archivos:\n{terminal.get_last_output()}")
    
    print("\n=== Ejemplo 2: Persistencia del estado ===")
    
    # Cambiar directorio y crear variable
    terminal.run("cd /tmp")
    terminal.run("export MI_VARIABLE='Hola desde zsh'")
    terminal.run("echo $MI_VARIABLE")
    print(f"Variable: {terminal.get_last_output()}")
    
    # Verificar que el directorio persiste
    terminal.run("pwd")
    print(f"Directorio después del cambio: {terminal.get_last_output()}")
    
    print("\n=== Ejemplo 3: Historial completo ===")
    
    print("Historial completo de la sesión:")
    print("=" * 50)
    print(terminal.get_full_log())
    print("=" * 50)
    
    print("\n=== Ejemplo 4: Singleton behavior ===")
    
    # Crear otra "instancia" - debería ser la misma
    terminal2 = TerminalSingleton()
    terminal2.run("echo 'Desde la segunda instancia'")
    
    # Verificar que ambas instancias son la misma
    print(f"¿Son la misma instancia? {terminal is terminal2}")
    print(f"Último output desde terminal1: {terminal.get_last_output()}")
    print(f"Último output desde terminal2: {terminal2.get_last_output()}")
    
    print("\n=== Ejemplo 5: Comandos con pipes y redirección ===")
    
    terminal.run("echo 'prueba1\nprueba2\nprueba3' | grep 'prueba2'")
    print(f"Resultado del grep: {terminal.get_last_output()}")
    
    terminal.run("ls -1 | head -3")
    print(f"Primeros 3 archivos: {terminal.get_last_output()}")
    
    # Cerrar la sesión
    print("\n=== Cerrando sesión ===")
    terminal.close()
    print("Sesión cerrada.")


if __name__ == "__main__":
    main() 