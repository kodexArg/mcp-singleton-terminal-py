"""
Terminal Singleton - Librería Python para automatización de terminal

Una implementación del patrón singleton que mantiene un proceso zsh persistente,
permitiendo ejecutar comandos de terminal desde Python conservando el estado
del shell entre ejecuciones.

Módulos:
    terminal_singleton: Clase principal TerminalSingleton

Uso básico:
    from terminal_singleton import TerminalSingleton
    
    terminal = TerminalSingleton()
    output = terminal.run("pwd")
    print(output)
    terminal.close()
"""

from .terminal_singleton import TerminalSingleton

__version__ = "1.0.0"
__author__ = "Kodex"
__all__ = ["TerminalSingleton"] 