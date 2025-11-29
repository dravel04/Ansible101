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

class GraderVars:
    """
    Logica para evaluar del ejercicio "Variables - Practica"
    """
    def __init__(self, name: str, debug_msg: List[Union[str, Text]] = []):
        self.name = name
        self.debug_msg = debug_msg

    def _verify_directory(self) -> Tuple[bool, str]:
        from pathlib import Path
        directory_path = "/tmp/demo"
        time.sleep(0.5)
        if Path(directory_path).is_dir():
            failed = False
            error_output = ""
        else:
            failed = True
            error_output = f"El directorio {directory_path} NO existe"
        return failed, error_output

    def _verify_file(self) -> Tuple[bool, str]:
        from pathlib import Path
        file_path = "/tmp/demo/index.html"
        time.sleep(0.5)
        if Path(file_path).is_file():
            failed = False
            error_output = ""
        else:
            failed = True
            error_output = f"El fichero {file_path} NO existe"
        return failed, error_output

    def _verify_playbook_content(self) -> Tuple[bool, str]:
        import yaml
        import os
        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'vars_lab.yml')
        vars_to_search = {'web_port','web_root'}
        time.sleep(0.5)
        try:
            with open(file_path, "r") as f:
                contenido = yaml.safe_load(f)
            for _, play in enumerate(contenido):
                vars_in_play = play.get("vars", {})
                remaining = vars_to_search - vars_in_play.keys()
            if remaining:
                failed = True
                error_output = f"No se han definido las variables {','.join(sorted(vars_to_search))}"
            else:
                failed = False
                error_output = ""
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return failed, error_output

    def _verify_file_content(self) -> Tuple[bool, str]:
        file_path = "/tmp/demo/index.html"
        line_to_search = "Servidor escuchando en el puerto 8080"
        time.sleep(0.5)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if line_to_search in content:
                failed = False
                error_output = ""
            else:
                failed = True
                error_output = f"El contenido de index.html NO es el solicitado"
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return failed, error_output

    def grade(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion del inicio: Define la secuencia de eventos.
        """
        event_info = EventInfo(name='Verificamos la definicion del playbook')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_playbook_content()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Verificamos el directorio /tmp/demo')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_directory()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Verificamos el fichero /tmp/demo/index.html')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_file()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None


        event_info = EventInfo(name='Verificamos el contenido del fichero /tmp/demo/index.html')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._verify_playbook_content()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None
