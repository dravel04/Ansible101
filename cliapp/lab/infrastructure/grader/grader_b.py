# lab/grader/grader_b.py
from lab.core.entities.grader import Grader
from lab.infrastructure.ui.console_utils import run_with_spinner


class GraderB(Grader):
    def check_lab_systems(self):
        return True


    def restore_password(self):
        return False


    def grade(self):
        checks = [
            ("Checking lab systems",self.check_lab_systems),
            ("Restoring the student user password",self.restore_password),
        ]
        print(f"Comezamos la validación del ejericio '{self.exercisename}'\n")
        run_with_spinner('grader',checks)