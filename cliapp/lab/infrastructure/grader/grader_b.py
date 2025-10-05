# lab/grader/grader_b.py
from lab.grader.grader import Grader
from lab.grader.utils import run_validations


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
        run_validations(checks)