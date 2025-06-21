import typer
from importlib import import_module

def grade_func(exercisename):
    typer.echo(f"Evaluando el ejercicio: {exercisename}")

    # Importa el script correspondiente dinámicamente
    script_module_name = f"lab.grade.scripts.grade_{exercisename.lower()}"
    try:
        script_module = import_module(script_module_name)
        script_module.run()
    except ImportError:
        typer.echo(f"Fallo durante la evaluacion de {exercisename}. No se encontró el script scripts.grade_{exercisename.lower()}.py")
        return