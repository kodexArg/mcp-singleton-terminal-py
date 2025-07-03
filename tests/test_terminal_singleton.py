#!/usr/bin/env python3
"""
Tests básicos para TerminalSingleton

Verifica las funcionalidades principales del singleton de terminal.
"""

import unittest
import os
import sys

# Agregar el directorio padre al path para importar el módulo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from terminal_singleton import TerminalSingleton


class TestTerminalSingleton(unittest.TestCase):
    """Tests para la clase TerminalSingleton."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        # Asegurar que empezamos con una instancia limpia
        TerminalSingleton._instance = None
    
    def tearDown(self):
        """Limpieza después de cada test."""
        # Cerrar cualquier instancia abierta
        if TerminalSingleton._instance is not None:
            try:
                TerminalSingleton._instance.close()
            except:
                pass
            TerminalSingleton._instance = None
    
    def test_singleton_behavior(self):
        """Verificar que se comporta como singleton."""
        terminal1 = TerminalSingleton()
        terminal2 = TerminalSingleton()
        
        # Deben ser la misma instancia
        self.assertIs(terminal1, terminal2)
        self.assertEqual(id(terminal1), id(terminal2))
    
    def test_basic_command_execution(self):
        """Test de ejecución básica de comandos."""
        terminal = TerminalSingleton()
        
        # Comando simple
        result = terminal.run("echo 'test'")
        self.assertEqual(result.strip(), "test")
        
        # Verificar que get_last_output devuelve lo mismo
        self.assertEqual(terminal.get_last_output().strip(), "test")
    
    def test_state_persistence(self):
        """Verificar que el estado persiste entre comandos."""
        terminal = TerminalSingleton()
        
        # Establecer una variable
        terminal.run("export TEST_VAR='persistence_test'")
        
        # Verificar que persiste
        result = terminal.run("echo $TEST_VAR")
        self.assertEqual(result.strip(), "persistence_test")
        
        # Cambiar directorio
        terminal.run("cd /tmp")
        
        # Verificar que el directorio cambió
        result = terminal.run("pwd")
        self.assertIn("/tmp", result)
    
    def test_log_accumulation(self):
        """Verificar que el historial se acumula correctamente."""
        terminal = TerminalSingleton()
        
        # Ejecutar varios comandos
        terminal.run("echo 'command1'")
        terminal.run("echo 'command2'")
        terminal.run("echo 'command3'")
        
        # Verificar último output
        self.assertEqual(terminal.get_last_output().strip(), "command3")
        
        # Verificar que el log completo contiene todos
        full_log = terminal.get_full_log()
        self.assertIn("command1", full_log)
        self.assertIn("command2", full_log)
        self.assertIn("command3", full_log)
    
    def test_command_with_pipes(self):
        """Test de comandos con pipes y redirección."""
        terminal = TerminalSingleton()
        
        # Comando con pipe
        result = terminal.run("echo 'line1\nline2\nline3' | grep 'line2'")
        self.assertEqual(result.strip(), "line2")
        
        # Comando con múltiples pipes
        result = terminal.run("echo 'test' | tr 'a-z' 'A-Z'")
        self.assertEqual(result.strip(), "TEST")
    
    def test_error_handling(self):
        """Verificar manejo de comandos que fallan."""
        terminal = TerminalSingleton()
        
        # Comando que genera error (pero no excepción)
        result = terminal.run("ls /directorio_inexistente 2>&1")
        
        # Debe contener algún mensaje de error
        self.assertTrue(len(result) > 0)
        
        # El terminal debe seguir funcionando
        next_result = terminal.run("echo 'still_working'")
        self.assertEqual(next_result.strip(), "still_working")
    
    def test_multiple_sessions(self):
        """Verificar que múltiples accesos usan la misma sesión."""
        # Primera instancia
        terminal1 = TerminalSingleton()
        terminal1.run("export SHARED_VAR='shared_value'")
        
        # Segunda instancia (debería ser la misma)
        terminal2 = TerminalSingleton()
        result = terminal2.run("echo $SHARED_VAR")
        
        self.assertEqual(result.strip(), "shared_value")
        self.assertIs(terminal1, terminal2)


class TestTerminalSingletonIntegration(unittest.TestCase):
    """Tests de integración más complejos."""
    
    def setUp(self):
        """Configuración antes de cada test."""
        TerminalSingleton._instance = None
    
    def tearDown(self):
        """Limpieza después de cada test."""
        if TerminalSingleton._instance is not None:
            try:
                TerminalSingleton._instance.close()
            except:
                pass
            TerminalSingleton._instance = None
    
    def test_complex_workflow(self):
        """Test de un flujo de trabajo complejo."""
        terminal = TerminalSingleton()
        
        # Crear directorio temporal
        terminal.run("mkdir -p /tmp/test_terminal")
        terminal.run("cd /tmp/test_terminal")
        
        # Crear archivos
        terminal.run("echo 'content1' > file1.txt")
        terminal.run("echo 'content2' > file2.txt")
        
        # Verificar contenido
        result = terminal.run("cat file1.txt")
        self.assertEqual(result.strip(), "content1")
        
        # Listar archivos
        result = terminal.run("ls -1 *.txt")
        self.assertIn("file1.txt", result)
        self.assertIn("file2.txt", result)
        
        # Limpiar
        terminal.run("rm -rf /tmp/test_terminal")
    
    def test_environment_variables(self):
        """Test exhaustivo de variables de entorno."""
        terminal = TerminalSingleton()
        
        # Establecer múltiples variables
        terminal.run("export VAR1='value1'")
        terminal.run("export VAR2='value2'")
        terminal.run("export PATH_BACKUP=$PATH")
        
        # Verificar todas
        result1 = terminal.run("echo $VAR1")
        result2 = terminal.run("echo $VAR2")
        
        self.assertEqual(result1.strip(), "value1")
        self.assertEqual(result2.strip(), "value2")
        
        # Modificar PATH y verificar persistencia
        terminal.run("export PATH=/custom/path:$PATH")
        result = terminal.run("echo $PATH")
        self.assertIn("/custom/path", result)


if __name__ == "__main__":
    # Verificar que zsh está disponible antes de ejecutar tests
    import subprocess
    try:
        subprocess.run(["/usr/bin/zsh", "--version"], 
                      capture_output=True, check=True)
        print("zsh encontrado, ejecutando tests...")
        unittest.main(verbosity=2)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: zsh no está instalado en /usr/bin/zsh")
        print("Los tests requieren zsh para funcionar.")
        sys.exit(1) 