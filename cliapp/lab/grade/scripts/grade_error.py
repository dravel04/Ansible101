from lab.grade.grade_functions import run_validations

def check_lab_systems():
    return True


def restore_password():
    return False


def run():
    checks = [
        ("Checking lab systems",check_lab_systems),
        ("Restoring the student user password",restore_password),
    ]
    run_validations(checks)