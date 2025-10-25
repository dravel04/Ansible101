import typer
from typing_extensions import Annotated
from rich.logging import RichHandler
import logging

# Variable global para guardar la instancia de Lab
lab = None

# Configuracion global del logger
logger = logging.getLogger("lab")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
handler = RichHandler(rich_tracebacks=True)
handler.setFormatter(formatter)
handler.setLevel(logging.NOTSET)
logger.addHandler(handler)

# descripcion general
app = typer.Typer(
    help="Un app para tus herramientas de laboratorio.",
    context_settings={"help_option_names": ["-h", "--help"]}
) 

@app.command()
def init(
    # Un argumento posicional se define simplemente con el tipo
    # y typer.Argument() si quieres añadir metadatos (como la ayuda)
    engine: Annotated[str, typer.Argument(help="Container engine a usar")] = "docker",
    debug: bool = typer.Option(False, "--debug", "-d", help="Activa el modo debug"),
    force: bool = typer.Option(False, "--force", "-f", help="Fuerza la inicializacion de un nuevo lab")
):
    """
    Inicia el laboratorio y sus dependencias
    """
    try:
        from lab.core.entities.lab import Lab
        from lab.infrastructure.services.lab_service import LabService
        if debug:
            logger.setLevel(logging.DEBUG)
        exists,lab = Lab.load(force)
        if not exists:
            lab.engine=engine
            lab.save()
        else:
            raise ValueError(f"Ya existe una instancia de Lab [engine={lab.engine}]. Para crear una nueva instancia, usar 'lab init <engine> -f' o borrar el fichero '~/.lab_config.json'")
        service = LabService(lab)
        service.init()
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")

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
    # print(lab.engine)
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