import typer
from typing_extensions import Annotated
import logging
from rich.logging import RichHandler

# Configuracion global del logger
logger = logging.getLogger("lab")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
handler = RichHandler(rich_tracebacks=True)
handler.setFormatter(formatter)
handler.setLevel(logging.NOTSET)
logger.addHandler(handler)

# descripcion general
app = typer.Typer(help="Un app para tus herramientas de laboratorio.") 

@app.command()
def start(
    # Un argumento posicional se define simplemente con el tipo
    # y typer.Argument() si quieres añadir metadatos (como la ayuda)
    exercisename: Annotated[str, typer.Argument(help="Nombre del ejercicio a iniciar")],
    debug: bool = typer.Option(False, "--debug", "-d")
):
    """
    Inicia las dependencias del ejercicio correspondiente
    """
    from lab.core.registry import auto_discover_exercises, EXERCISES
    auto_discover_exercises()
    cls = EXERCISES.get(exercisename.lower())
    if not cls:
        typer.secho(
            f"\n❌ Error: Ejercicio '{exercisename}' no existe.\n",
            fg=typer.colors.RED,
            bold=False
        )
        raise typer.Exit(code=1)

    if debug:
        logger.setLevel(logging.DEBUG)

    # Creamos instancia de Exercise con el nombre pasado
    exercise = cls(exercisename)
    exercise.start()


@app.command()
def grade(
    exercisename: Annotated[str, typer.Argument(help="Nombre del ejercicio a evaluar")],
    debug: bool = typer.Option(False, "--debug", "-d")
):
    """
    Evalua el ejercicio correspondiente
    """
    from lab.core.registry import auto_discover_graders, GRADERS
    auto_discover_graders()
    cls = GRADERS.get(exercisename.lower())
    if not cls:
        typer.secho(
            f"\n❌ Error: Ejercicio '{exercisename}' no existe.\n",
            fg=typer.colors.RED,
            bold=False
        )
        raise typer.Exit(code=1)

    if debug:
        logger.setLevel(logging.DEBUG)

    # Creamos instancia de Grader con el nombre pasado
    grader = cls(exercisename)
    grader.grade()


@app.command()
def finish(
    exercisename: Annotated[str, typer.Argument(help="Nombre del ejercicio a finalizar.")],
    debug: bool = typer.Option(False, "--debug", "-d")
):
    """
    Libera las dependencias del ejercicio correspondiente
    """
    from lab.core.registry import auto_discover_exercises, EXERCISES
    auto_discover_exercises()
    cls = EXERCISES.get(exercisename.lower())
    if not cls:
        typer.secho(
            f"\n❌ Error: Ejercicio '{exercisename}' no existe.\n",
            fg=typer.colors.RED,
            bold=False
        )
        raise typer.Exit(code=1)
    
    if debug:
        logger.setLevel(logging.DEBUG)

    # Creamos instancia de Exercise con el nombre pasado
    exercise = cls(exercisename)
    exercise.finish()


if __name__ == '__main__':
    app()