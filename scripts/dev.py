#!/usr/bin/env python3
"""
Script de desarrollo para Terminal Singleton
Script de automatización usando Python puro
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_cmd(cmd, description=""):
    """Ejecutar comando y mostrar resultado."""
    if description:
        print(f"🔨 {description}")
    print(f"   → {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Error ejecutando: {cmd}")
        sys.exit(1)
    print("✅ Completado\n")

def install():
    """Instalar el paquete."""
    run_cmd("pip install .", "Instalando paquete")

def dev_install():
    """Instalar en modo desarrollo."""
    run_cmd("pip install -e .", "Instalando en modo desarrollo")

def test():
    """Ejecutar tests."""
    run_cmd("python -m pytest tests/ -v", "Ejecutando tests")

def test_simple():
    """Ejecutar test simple."""
    run_cmd("python tests/test_terminal_singleton.py", "Ejecutando test básico")

def clean():
    """Limpiar archivos temporales."""
    print("🧹 Limpiando archivos temporales")
    
    dirs_to_remove = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_remove:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"   🗑️  Eliminado: {path}")
    
    # Limpiar __pycache__
    for path in Path(".").rglob("__pycache__"):
        shutil.rmtree(path)
        print(f"   🗑️  Eliminado: {path}")
    
    # Limpiar archivos .pyc
    for path in Path(".").rglob("*.pyc"):
        path.unlink()
        print(f"   🗑️  Eliminado: {path}")
    
    print("✅ Limpieza completada\n")

def build():
    """Construir paquete."""
    clean()
    run_cmd("python setup.py sdist bdist_wheel", "Construyendo paquete")

def example():
    """Ejecutar ejemplo básico."""
    run_cmd("python examples/basic_usage.py", "Ejecutando ejemplo")

def check_deps():
    """Verificar dependencias."""
    print("🔍 Verificando dependencias")
    
    try:
        import pexpect
        print(f"   ✅ pexpect: {pexpect.__version__}")
    except ImportError:
        print("   ❌ pexpect: NO INSTALADO")
    
    zsh_path = shutil.which("zsh")
    if zsh_path:
        print(f"   ✅ zsh: {zsh_path}")
    else:
        print("   ❌ zsh: NO ENCONTRADO")
    print()

def dev_deps():
    """Instalar dependencias de desarrollo."""
    run_cmd("pip install pytest black flake8 wheel twine", 
            "Instalando dependencias de desarrollo")

def help_menu():
    """Mostrar ayuda."""
    print("🛠️  Comandos disponibles:")
    print("   install     - Instalar el paquete")
    print("   dev-install - Instalar en modo desarrollo")
    print("   test        - Ejecutar tests")
    print("   test-simple - Ejecutar test básico")
    print("   clean       - Limpiar archivos temporales")
    print("   build       - Construir paquete")
    print("   example     - Ejecutar ejemplo")
    print("   check-deps  - Verificar dependencias")
    print("   dev-deps    - Instalar deps de desarrollo")
    print("   help        - Mostrar esta ayuda")

def main():
    """Función principal."""
    if len(sys.argv) < 2:
        help_menu()
        return
    
    command = sys.argv[1]
    
    commands = {
        "install": install,
        "dev-install": dev_install,
        "test": test,
        "test-simple": test_simple,
        "clean": clean,
        "build": build,
        "example": example,
        "check-deps": check_deps,
        "dev-deps": dev_deps,
        "help": help_menu,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Comando desconocido: {command}")
        help_menu()
        sys.exit(1)

if __name__ == "__main__":
    main() 