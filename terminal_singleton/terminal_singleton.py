"""
Terminal Singleton - Librería Python para automatización de terminal

Implementa un patrón singleton que mantiene un proceso zsh persistente,
permitiendo ejecutar comandos de terminal desde Python conservando
el estado del shell entre ejecuciones.

Características principales:
    - Una única instancia global (singleton pattern)
    - Persistencia de estado (variables, directorio de trabajo, historial)
    - Captura controlada de salida de comandos
    - Auto-recovery del proceso en caso de fallo
    - Control de timeout configurable

Ejemplo de uso:
    from terminal_singleton import TerminalSingleton
    
    terminal = TerminalSingleton()
    terminal.run("cd /tmp && export VAR=test")
    output = terminal.run("echo $VAR")
    print(output)  # "test"
    terminal.close()
"""

import uuid, signal, os, pexpect


class TerminalSingleton:
    """
    Clase singleton para automatización de terminal con proceso zsh persistente.
    
    Esta clase implementa el patrón singleton garantizando una única instancia
    por proceso Python. Mantiene un proceso zsh activo que preserva estado
    (variables de entorno, directorio de trabajo, etc.) entre comandos.
    
    Atributos privados:
        _proc (pexpect.spawn): Proceso zsh controlado via pexpect
        _timeout (int): Tiempo límite en segundos para ejecución de comandos
        _last (str): Salida del último comando ejecutado
        _log (str): Historial completo de todas las salidas
    
    Métodos públicos:
        run(cmd): Ejecuta un comando y devuelve su salida
        get_last_output(): Obtiene la salida del último comando
        get_full_log(): Obtiene el historial completo de la sesión
        close(): Cierra el proceso zsh y libera recursos
        
    Ejemplo:
        terminal = TerminalSingleton()
        terminal.run("cd /tmp")
        result = terminal.run("pwd")  # Devuelve "/tmp"
    """
    _instance = None

    def __new__(cls, *a, **kw):
        """
        Implementa el patrón singleton devolviendo siempre la misma instancia.
        
        Si la instancia no existe o el proceso zsh murió, se crea/respawnea
        automáticamente una nueva instancia.
        
        Returns:
            TerminalSingleton: La única instancia de la clase
        """
        if cls._instance is None or not getattr(cls._instance, "_proc", None) or not cls._instance._proc.isalive():
            cls._instance = super().__new__(cls)
            cls._instance._init(*a, **kw)
        return cls._instance

    def _init(self, shell_path="/usr/bin/zsh", timeout=30):
        """
        Inicializa el proceso zsh y configura los buffers internos.
        
        Args:
            shell_path (str): Ruta al ejecutable de zsh
            timeout (int): Tiempo límite en segundos para comandos
        """
        self._proc = pexpect.spawn(shell_path, encoding="utf-8", echo=False)
        self._proc.delaybeforesend = 0.05
        self._timeout = timeout
        self._last = ""
        self._log = ""

    def run(self, cmd: str) -> str:
        """
        Ejecuta un comando en el shell zsh y devuelve su salida.
        
        Utiliza marcadores UUID únicos para delimitar la salida y capturar
        exactamente la respuesta del comando ejecutado.
        
        Args:
            cmd (str): Comando a ejecutar en el shell
            
        Returns:
            str: Salida combinada (stdout + stderr) del comando
            
        Raises:
            pexpect.TIMEOUT: Si el comando excede el tiempo límite
            
        Example:
            output = terminal.run("ls -la /tmp")
            print(output)
        """
        marker = f"__END__{uuid.uuid4().hex}__"
        self._proc.sendline(f"{cmd} ; printf '{marker}\\n'")
        self._proc.expect(marker, timeout=self._timeout)
        out = self._proc.before.strip()
        self._last = out
        self._log += out + "\n"
        return out

    def get_last_output(self) -> str:
        """
        Obtiene la salida del último comando ejecutado.
        
        Returns:
            str: Salida del último comando ejecutado via run()
        """
        return self._last

    def get_full_log(self) -> str:
        """
        Obtiene el historial completo de la sesión de terminal.
        
        Returns:
            str: Todo el historial de comandos y salidas desde el inicio
        """
        return self._log.rstrip()

    def close(self):
        """
        Cierra el proceso zsh y libera recursos del sistema.
        
        Envía comando 'exit' al shell y fuerza la terminación del proceso
        si es necesario. Limpia el PID del sistema operativo.
        """
        if self._proc.isalive():
            self._proc.sendline("exit")
            self._proc.terminate(force=True)
            try:
                os.kill(self._proc.pid, signal.SIGTERM)
            except OSError:
                pass 