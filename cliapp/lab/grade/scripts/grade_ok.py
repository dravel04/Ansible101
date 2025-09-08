from lab.grade.scripts.functions import run_validations

def restore_password():
    return False


def install_packages():
    return False


def run():
    checks = [
        ("Restoring the student user password",restore_password),
        ("Installing required packages",install_packages),
    ]
    run_validations(checks)
