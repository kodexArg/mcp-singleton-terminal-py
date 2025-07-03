# Terminal Singleton Python

Una **librería Python para automatización de terminal** que implementa el patrón singleton para mantener un proceso zsh persistente. Permite ejecutar comandos de terminal desde Python conservando el estado del shell (variables de entorno, directorio de trabajo, historial) entre ejecuciones.

## Características

✅ **Patrón Singleton**: Una única instancia global que garantiza consistencia  
✅ **Estado Persistente**: Variables de entorno, directorio de trabajo y historial se mantienen  
✅ **Captura Controlada**: Gestión precisa de stdout y stderr de comandos  
✅ **API Simple**: Interfaz intuitiva para ejecutar comandos de terminal  
✅ **Auto-recovery**: Respawnea automáticamente el proceso zsh si muere  
✅ **Control de Timeout**: Evita bloqueos con tiempo límite configurable  
✅ **Soporte para Pipes**: Maneja comandos complejos con redirecciones y pipes

## Instalación

### Desde el código fuente

```bash
git clone https://github.com/kodex/terminal-singleton-py.git
cd terminal-singleton-py
pip install -e .
```

### Usando script de desarrollo

```bash
# Hacer ejecutable y usar comandos simplificados
chmod +x scripts/dev.py
./scripts/dev.py help           # Ver comandos disponibles
./scripts/dev.py dev-install    # Instalar en modo desarrollo
./scripts/dev.py test           # Ejecutar tests
./scripts/dev.py example        # Ejecutar ejemplo
```

## Comandos de Desarrollo

### Con script Python (recomendado)

```bash
./scripts/dev.py help           # Mostrar ayuda
./scripts/dev.py dev-install    # Instalar en modo desarrollo
./scripts/dev.py test           # Ejecutar tests completos
./scripts/dev.py test-simple    # Test básico
./scripts/dev.py example        # Ejecutar ejemplo
./scripts/dev.py check-deps     # Verificar dependencias
./scripts/dev.py clean          # Limpiar archivos temporales
./scripts/dev.py build          # Construir paquete
./scripts/dev.py dev-deps       # Instalar deps de desarrollo
```

### Comandos directos (alternativa)

```bash
# Instalación y desarrollo
pip install -e .                        # Instalar en modo desarrollo
pip install pytest black flake8 wheel twine  # Deps de desarrollo

# Testing y ejemplos
python -m pytest tests/ -v              # Tests completos
python tests/test_terminal_singleton.py  # Test básico
python examples/basic_usage.py          # Ejecutar ejemplo

# Build y distribución
python setup.py sdist bdist_wheel       # Construir paquete
python -c "import pexpect; print(pexpect.__version__)"  # Verificar deps

# Limpieza
rm -rf build/ dist/ *.egg-info/
find . -name __pycache__ -exec rm -rf {} +
```

### Dependencias

- Python 3.7+
- pexpect >= 4.8.0
- zsh (debe estar instalado en `/usr/bin/zsh`)

## Uso Básico

```python
from terminal_singleton import TerminalSingleton

# Crear instancia (singleton - siempre devuelve la misma instancia)
terminal = TerminalSingleton()

# Ejecutar comandos individuales
output = terminal.run("pwd")
print(f"Directorio actual: {output}")

# El estado del shell persiste entre comandos
terminal.run("cd /tmp")
terminal.run("export MI_VAR='valor_persistente'")

# Variables y directorio se mantienen
result = terminal.run("echo $MI_VAR")
print(result)  # "valor_persistente"

current_dir = terminal.run("pwd") 
print(current_dir)  # "/tmp"

# Acceder a salidas anteriores
print("Última salida:", terminal.get_last_output())
print("Historial completo:", terminal.get_full_log())

# Cerrar cuando termine
terminal.close()
```

## API Reference

### `TerminalSingleton(shell_path="/usr/bin/zsh", timeout=30)`

Clase singleton que mantiene un proceso zsh persistente.

#### Parámetros

- `shell_path` (str): Ruta al ejecutable de zsh. Por defecto `/usr/bin/zsh`
- `timeout` (int): Tiempo límite en segundos para la ejecución de comandos. Por defecto 30

#### Métodos

##### `run(cmd: str) -> str`

Ejecuta un comando en la terminal y devuelve su salida.

```python
output = terminal.run("ls -la")
print(output)
```

**Parámetros:**
- `cmd` (str): Comando a ejecutar

**Retorna:**
- `str`: Salida combinada (stdout + stderr) del comando

##### `get_last_output() -> str`

Devuelve la salida del último comando ejecutado.

```python
terminal.run("date")
last = terminal.get_last_output()  # Mismo resultado que el run anterior
```

**Retorna:**
- `str`: Salida del último comando ejecutado

##### `get_full_log() -> str`

Devuelve todo el historial de salida desde que se creó la sesión.

```python
log = terminal.get_full_log()
print(log)  # Todo el historial de comandos y salidas
```

**Retorna:**
- `str`: Historial completo de la sesión

##### `close()`

Cierra el proceso zsh y libera recursos del sistema.

```python
terminal.close()
```

## Ejemplos Avanzados

### Persistencia de Estado

```python
terminal = TerminalSingleton()

# Configurar entorno
terminal.run("cd /home/user/proyecto")
terminal.run("export NODE_ENV=development")
terminal.run("source .env")

# Los comandos siguientes mantienen el contexto
terminal.run("npm test")  # Se ejecuta en el directorio correcto
terminal.run("echo $NODE_ENV")  # Salida: "development"
```

### Comandos con Pipes y Redirección

```python
terminal = TerminalSingleton()

# Pipes complejos
result = terminal.run("ps aux | grep python | wc -l")
print(f"Procesos Python activos: {result}")

# Redirección
terminal.run("echo 'log entry' >> /tmp/app.log")
terminal.run("cat /tmp/app.log")
```

### Manejo de Errores

```python
terminal = TerminalSingleton()

try:
    # Comando que puede fallar
    output = terminal.run("comando_inexistente")
except Exception as e:
    print(f"Error ejecutando comando: {e}")
    
# El terminal sigue funcionando después de errores
terminal.run("echo 'continúa funcionando'")
```

### Singleton Behavior

```python
# Múltiples "instancias" son la misma
term1 = TerminalSingleton()
term2 = TerminalSingleton()

print(term1 is term2)  # True

term1.run("export TEST=123")
term2.run("echo $TEST")  # Salida: "123"
```

## Casos de Uso

### Automatización de Despliegues

```python
terminal = TerminalSingleton()

# Preparar entorno
terminal.run("cd /var/www/mi-app")
terminal.run("git pull origin main")

# Build y deploy
terminal.run("npm install")
terminal.run("npm run build")
terminal.run("sudo systemctl restart mi-app")

# Verificar estado
status = terminal.run("systemctl status mi-app")
if "active (running)" in status:
    print("Deploy exitoso")
```

### Testing de Scripts

```python
terminal = TerminalSingleton()

# Configurar entorno de test
terminal.run("cd /tmp")
terminal.run("mkdir test_env && cd test_env")

# Ejecutar batería de tests
tests = ["test1.sh", "test2.sh", "test3.sh"]
for test in tests:
    result = terminal.run(f"./{test}")
    if "PASS" not in result:
        print(f"Test {test} falló: {result}")
```

### Monitoreo de Sistema

```python
import time
from terminal_singleton import TerminalSingleton

terminal = TerminalSingleton()

def monitor_system():
    while True:
        # CPU usage
        cpu = terminal.run("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
        
        # Memory usage
        mem = terminal.run("free | grep Mem | awk '{printf \"%.2f\", $3/$2 * 100.0}'")
        
        # Disk usage
        disk = terminal.run("df -h / | awk 'NR==2{print $5}' | cut -d'%' -f1")
        
        print(f"CPU: {cpu}% | RAM: {mem}% | Disk: {disk}%")
        time.sleep(60)

monitor_system()
```

## Arquitectura Interna

### Patrón Singleton

La clase implementa el patrón Singleton garantizando que:

- Solo existe una instancia por proceso Python
- La instancia se reutiliza en múltiples importaciones
- Si el proceso zsh muere, se respawnea automáticamente

### Gestión de Procesos

- Usa `pexpect` para controlar el proceso zsh
- Implementa marcadores UUID únicos para delimitar salidas
- Maneja timeouts y limpieza de recursos automáticamente

### Control de Output

- Captura stdout y stderr combinados
- Mantiene historial completo de la sesión
- Separa la salida del último comando del historial total

## Limitaciones

1. **Shell específico**: Diseñado para zsh, puede requerir adaptación para otros shells
2. **Timeout fijo**: El timeout se aplica a todo el comando, no a partes individuales
3. **Comandos interactivos**: No maneja comandos que requieren input del usuario
4. **Concurrencia**: No thread-safe, diseñado para uso secuencial

## Troubleshooting

### El proceso zsh no inicia

Verificar que zsh esté instalado:
```bash
which zsh
# Debería mostrar: /usr/bin/zsh
```

### Timeouts frecuentes

Aumentar el timeout al crear la instancia:
```python
terminal = TerminalSingleton(timeout=60)  # 60 segundos
```

### Comandos que no responden

Algunos comandos pueden requerir flags no-interactivos:
```python
# En lugar de:
terminal.run("apt install package")

# Usar:
terminal.run("apt install -y package")
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

MIT License - ver el archivo `LICENSE` para más detalles.

## Changelog

### v1.0.0
- Implementación inicial del patrón Singleton
- Soporte para zsh con pexpect
- API básica (run, get_last_output, get_full_log, close)
- Auto-recovery del proceso
- Control de timeout configurable 