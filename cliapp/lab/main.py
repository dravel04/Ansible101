import typer
from typing_extensions import Annotated
from rich.logging import RichHandler
import logging
import sys

from lab.infrastructure.ui.progress_notifier_adapter import ProgressNotifierAdapter

IS_PACKAGED = getattr(sys, "frozen", False) or "__compiled__" in globals()

# Configuracion global del logger
logger = logging.getLogger("lab")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
handler = RichHandler(rich_tracebacks=True, show_path=not IS_PACKAGED)
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
    # force: bool = typer.Option(False, "--force", "-f", help="Fuerza la inicializacion de un nuevo lab")
):
    """
    Inicia el laboratorio y sus dependencias
    """
    from lab.infrastructure.adapters.lab_repository_adapter import LabRepositoryAdapter
    from lab.infrastructure.adapters.lab_adapter import LabAdapter
    from lab.application.use_cases.lab_initializer import LabInitializer
    from lab.core.entities.lab import Lab
    if debug:
        logger.setLevel(logging.DEBUG)

    LabInitializer().execute(
        service=LabAdapter(),
        repo_adapter=LabRepositoryAdapter(),
        lab=Lab(engine=engine),
        # force=force
    )


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
    from lab.infrastructure.adapters.registry_adapter import RegistryAdapter
    if debug:
        logger.setLevel(logging.DEBUG)

    registry = RegistryAdapter()
    exercises_map = registry.auto_discover_exercises()
    cls = exercises_map.get(exercisename.lower())
    if not cls:
        typer.secho(
            f"\n❌ Error: Ejercicio '{exercisename}' no existe.\n",
            fg=typer.colors.RED,
            bold=False
        )
        raise typer.Exit(code=1)
    # Creamos instancia de Exercise con el nombre pasado
    exercise = cls(exercisename)
    notifier = ProgressNotifierAdapter()
    exercise.start(notifier)


@app.command()
def grade(
    exercisename: Annotated[str, typer.Argument(help="Nombre del ejercicio a evaluar")],
    debug: bool = typer.Option(False, "--debug", "-d")
):
    """
    Evalua el ejercicio correspondiente
    """
    from lab.infrastructure.adapters.registry_adapter import RegistryAdapter
    from lab.infrastructure.ui.progress_notifier_adapter import ProgressNotifierAdapter
    if debug:
        logger.setLevel(logging.DEBUG)

    registry = RegistryAdapter()
    graders_map = registry.auto_discover_graders()
    cls = graders_map.get(exercisename.lower())
    if not cls:
        typer.secho(
            f"\n❌ Error: Ejercicio '{exercisename}' no existe.\n",
            fg=typer.colors.RED,
            bold=False
        )
        raise typer.Exit(code=1)
    # Creamos instancia de Grader con el nombre pasado
    grader = cls(exercisename)
    notifier = ProgressNotifierAdapter()
    grader.grade(notifier)


@app.command()
def finish(
    exercisename: Annotated[str, typer.Argument(help="Nombre del ejercicio a finalizar.")],
    debug: bool = typer.Option(False, "--debug", "-d")
):
    """
    Libera las dependencias del ejercicio correspondiente
    """
    from lab.infrastructure.adapters.registry_adapter import RegistryAdapter
    if debug:
        logger.setLevel(logging.DEBUG)

    registry = RegistryAdapter()
    exercises_map = registry.auto_discover_exercises()
    cls = exercises_map.get(exercisename.lower())
    if not cls:
        typer.secho(
            f"\n❌ Error: Ejercicio '{exercisename}' no existe.\n",
            fg=typer.colors.RED,
            bold=False
        )
        raise typer.Exit(code=1)
    # Creamos instancia de Exercise con el nombre pasado
    exercise = cls(exercisename)
    notifier = ProgressNotifierAdapter()
    exercise.finish(notifier)


if __name__ == '__main__':
    app()