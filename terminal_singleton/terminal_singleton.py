import uuid, signal, os, pexpect

class TerminalSingleton:
    _instance = None

    def __new__(cls, *a, **kw):
        if cls._instance is None or not getattr(cls._instance, "_proc", None) or not cls._instance._proc.isalive():
            cls._instance = super().__new__(cls)
            cls._instance._init(*a, **kw)
        return cls._instance

    def _init(self, shell_path="/usr/bin/zsh", timeout=30):
        self._proc = pexpect.spawn(shell_path, encoding="utf-8", echo=False)
        self._proc.delaybeforesend = 0.05
        self._timeout = timeout
        self._last = ""
        self._log = ""

    def run(self, cmd: str) -> str:
        marker = f"__END__{uuid.uuid4().hex}__"
        self._proc.sendline(f"{cmd} ; printf '{marker}\\n'")
        self._proc.expect(marker, timeout=self._timeout)
        out = self._proc.before.strip()
        self._last = out
        self._log += out + "\n"
        return out

    def get_last_output(self) -> str:
        return self._last

    def get_full_log(self) -> str:
        return self._log.rstrip()

    def close(self):
        if hasattr(self, '_proc') and self._proc and self._proc.isalive():
            self._proc.sendline("exit")
            self._proc.terminate(force=True)
            try:
                os.kill(self._proc.pid, signal.SIGTERM)
            except OSError:
                pass