# lab/grader/grader_c.py
from lab.core.entities.grader import Grader
from lab.infrastructure.ui.console_utils import run_with_spinner


class GraderC(Grader):
    def check_lab_systems(self):
        return True


    def restore_password(self):
        return False


    def verify_connectivity(self):
        return True


    def install_packages(self):
        return False


    def grade(self):
        checks = [
            ("Checking lab systems",self.check_lab_systems),
            ("Restoring the student user password",self.restore_password),
            ("Verifying network connectivity",self.verify_connectivity),
            ("Installing required packages",self.install_packages),
        ]
        print(f"Comezamos la validación del ejericio '{self.exercisename}'\n")
        run_with_spinner('grader',checks)