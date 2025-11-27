# lab/application/use_cases/grader/grader_vars.py
from typing import Tuple, Union, List
from rich.text import Text
import logging
import sys
import time

from lab.core.dtos.EventInfo import EventInfo
from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort

logger = logging.getLogger("lab")

class GraderWebservers:
    """
    Logica para evaluar del ejercicio "WebServers - Practica"
    """
    def __init__(self, name: str, debug_msg: List[Union[str, Text]] = []):
        self.name = name
        self.debug_msg = debug_msg

    def _verify_apache_config(self) -> Tuple[bool, str]:
        import paramiko
        from pathlib import Path
        config_path = "/etc/httpd/conf.d/main.conf"
        line_to_search = "Listen 9090"
        time.sleep(0.5)
        failed = False
        error_output = ""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ---- Cargar ~/.ssh/config ----
            config = paramiko.SSHConfig()
            with open(Path.home() / ".ssh/config") as f:
                config.parse(f)
            host_config = config.lookup("web1")
            key_path = Path(host_config["identityfile"][0]).expanduser()
            ssh.connect(
                hostname='localhost',
                port=2232,
                username='ansible',
                key_filename=str(key_path) if key_path else None,
                allow_agent=True,
                look_for_keys=True
            )
            sftp = ssh.open_sftp()
            with sftp.open(config_path, "r") as f:
                content = f.read().decode('utf-8')
            if not line_to_search in content:
                failed = True
                error_output = f"Apache no tiene configurado el puerto 9090. Revise roles/apache/defaults/main.yml"
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return failed, error_output

    def _verify_custom_index(self) -> Tuple[bool, str]:
        """
        Verifica que http://localhost:8080 devuelve la pagina
        personalizada usando la libreria requests
        """
        import requests
        failed = False
        error_output = ""
        time.sleep(0.5)
        url = "http://localhost:8080"
        expected_snippet = "¡Apache funcionando!"
        try:
            response = requests.get(url, timeout=2)
            if response.status_code != 200:
                failed = True
                error_output = f"HTTP {response.status_code}: la pagina no responde correctamente"
            content = response.text
            if not expected_snippet in content:
                failed = True
                error_output = f"El servidor Apache no esta devolviendo la pagina esperada. Revise el template 'index.html.j2' y la tarea de despliegue del template"
            return failed, error_output
        except Exception as e:
            return True, f"{type(e).__name__}: {e}"

    def _verify_endpoint(self) -> Tuple[bool, str]:
        """
        Verifica que http://localhost:8080/health devuelve 200 OK
        """
        import requests
        failed = False
        error_output = ""
        time.sleep(0.5)
        url = "http://localhost:8080/health"
        try:
            response = requests.get(url, timeout=2)
            if response.status_code != 200:
                failed = True
                error_output = f"HTTP {response.status_code}: la pagina no responde correctamente"
            content = response.text
            if not 'OK' in content:
                failed = True
                error_output = f"El endpoint de NGINX /health no devuelve 200 OK. Revise el template 'reverse-proxy.conf.j2' y la tarea de despliegue del template"
            return failed, error_output
        except Exception as e:
            return True, f"{type(e).__name__}: {e}"

    def grade(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion del inicio: Define la secuencia de eventos.
        """
        event_info = EventInfo(name='Verificamos la configuracion de Apache')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_apache_config()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Verificamos el despliegue de la pagina custom')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_custom_index()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Verificamos el endpoint /health')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_endpoint()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

