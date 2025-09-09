# lab/grade/grade_func.py
from lab.grade.scripts import grade_ok, grade_rich, grade_error
import typer

GRADE_MODULES = {
    "ok": grade_ok,
    "rich": grade_rich,
    "error": grade_error,
}

def grade_func(exercisename: str):
    typer.echo(f"Evaluando el ejercicio: {exercisename}\n")

    module = GRADE_MODULES.get(exercisename.lower())
    if not module:
        typer.echo(
            f"Fallo durante la evaluación de {exercisename}. "
            f"No se encontró el script correspondiente."
        )
        return

    # Ejecuta el run solo cuando se necesita
    module.run()
