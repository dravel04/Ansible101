# lab/infrastructure/grader/g_a.py
from typing import Callable, Tuple
from functools import partial
# Importamos Puertos del Core
from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort

import logging
logger = logging.getLogger("lab")

# Definimos el tipo de la funcion de chequeo que vamos a pasar al notificador
CheckFunc = Callable[[], Tuple[bool, str]]

class GraderA:

    def __init__(self, exercisename: str):
        self.exercisename = exercisename

    def _restore_password(self):
        failed = False
        error_output = "ERROR: No se puede conectar con el gestor de password"
        return failed, error_output

    def _verify_packages(self):
        failed = True
        error_output = "ERROR: Falta el paquete 'hostname'"
        return failed, error_output

    def grade(self, notifier: ProgressNotifierPort) -> None:
        checks: list[Tuple[str, CheckFunc]] = [
            ("Creating exercise containers", self._restore_password),
            ("Installing required packages", self._verify_packages),
            # Añadir mas checks...
        ]
        notifier.run_checks('grade', checks)
