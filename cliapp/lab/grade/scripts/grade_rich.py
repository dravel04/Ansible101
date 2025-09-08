from lab.grade.grade_functions import run_validations

def check_lab_systems():
    return True


def restore_password():
    return False


def verify_connectivity():
    return True


def install_packages():
    return False


def run():
    checks = [
        ("Checking lab systems",check_lab_systems),
        ("Restoring the student user password",restore_password),
        ("Verifying network connectivity",verify_connectivity),
        ("Installing required packages",install_packages),
    ]
    run_validations(checks)
