# lab/grader/grader_a.py
from lab.core.entities.grader import Grader
from lab.infrastructure.ui.console_utils import run_with_spinner
import logging

# Configuración global del logger
logger = logging.getLogger("lab")

class GraderA(Grader):

    def restore_password(self):
        return False

    def install_packages(self):
        return False

    def grade(self):
        checks = [
            ("Restoring the student user password",self.restore_password),
            ("Installing required packages",self.install_packages),
        ]
        print(f"Comezamos la validación del ejericio '{self.exercisename}'\n")
        run_with_spinner('grader',checks)
