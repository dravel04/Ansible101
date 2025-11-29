# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/application/use_cases/grader/grader_vars.py
from typing import Tuple, Union, List
from rich.text import Text
import logging
import sys
import time

from lab.core.dtos.EventInfo import EventInfo
from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort

logger = logging.getLogger("lab")

class GraderDatabases:
    """
    Logica para evaluar del ejercicio "Databases - Practica"
    """
    def __init__(self, name: str, debug_msg: List[Union[str, Text]] = []):
        self.name = name
        self.debug_msg = debug_msg

    def _verify_listener_config(self) -> Tuple[bool, str]:
        """
        Evalua si el listener de PostgreSQL es el 5433
        """
        import paramiko
        from pathlib import Path
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
            host_config = config.lookup("db1")
            key_path = Path(host_config["identityfile"][0]).expanduser()
            ssh.connect(
                hostname='localhost',
                port=2233,
                username='ansible',
                key_filename=str(key_path) if key_path else None,
                allow_agent=True,
                look_for_keys=True
            )
            command = "sudo -u postgres ss -tulnp | grep postgres | grep 5433 | wc -l"
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode().strip()
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                failed = True
                error_output = f"Error ejecutando el comando en db1: {stderr.read().decode().strip()}"
                return failed, error_output
            if not int(output) == 1:
                failed = True
                error_output = f"PostgreSQL no tiene configurado el puerto 5433. Revise roles/postgresql/defaults/main.yml"
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return failed, error_output

    def _verify_table(self) -> Tuple[bool, str]:
        """
        Evalua si existe la tabla empleados
        """
        import paramiko
        from pathlib import Path
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
            host_config = config.lookup("db1")
            key_path = Path(host_config["identityfile"][0]).expanduser()
            ssh.connect(
                hostname='localhost',
                port=2233,
                username='ansible',
                key_filename=str(key_path) if key_path else None,
                allow_agent=True,
                look_for_keys=True
            )
            command = "sudo -u postgres psql -t -c psql -t -p 5433 -c \"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'empleados';\""
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode().strip()
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                failed = True
                error_output = f"Error ejecutando el comando en db1: {stderr.read().decode().strip()}"
                return failed, error_output
            if not int(output) == 1:
                failed = True
                error_output = f"No existe la tabla 'empleados' en PostgreSQL . Repase 'Ejercicio 2 — Añadir una tabla'"
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return failed, error_output

    def _verify_users(self) -> Tuple[bool, str]:
        """
        Evalua si existe la tabla empleados
        """
        import paramiko
        from pathlib import Path
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
            host_config = config.lookup("db1")
            key_path = Path(host_config["identityfile"][0]).expanduser()
            ssh.connect(
                hostname='localhost',
                port=2233,
                username='ansible',
                key_filename=str(key_path) if key_path else None,
                allow_agent=True,
                look_for_keys=True
            )
            command = "sudo -u postgres psql -t -c psql -t -p 5433 -c \"SELECT COUNT(*) FROM empleados;\""
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode().strip()
            exit_status = stdout.channel.recv_exit_status()
            if exit_status != 0:
                failed = True
                error_output = f"Error ejecutando el comando en db1: {stderr.read().decode().strip()}"
                return failed, error_output
            if not int(output) >= 4:
                failed = True
                error_output = f"No se han creados los usuarios en la tabla 'empleados' en PostgreSQL . Repase 'Ejercicio 3 y 4'"
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return failed, error_output


    def grade(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion del inicio: Define la secuencia de eventos.
        """
        event_info = EventInfo(name='Verificamos la configuracion del listener')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_listener_config()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Verificamos si existe la tabla empleados')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_table()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Verificamos si se han creados los usuarios')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_users()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

