# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

import typer
from typing_extensions import Annotated
from rich.logging import RichHandler
import logging
import sys

from lab.infrastructure.ui.progress_notifier_adapter import ProgressNotifierAdapter
from lab.infrastructure.adapters.registry_adapter import RegistryAdapter

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

# Funciones de autocompletado dinamico
def exercises_autocomplete(ctx: typer.Context, args: list, incomplete: str):
    registry = RegistryAdapter()
    exercises_map = registry.auto_discover_exercises()
    return [name for name in exercises_map.keys() if name.startswith(incomplete)]

def graders_autocomplete(ctx: typer.Context, args: list, incomplete: str):
    registry = RegistryAdapter()
    graders_map = registry.auto_discover_graders()
    return [name for name in graders_map.keys() if name.startswith(incomplete)]

@app.command()
def init(
    # Un argumento posicional se define simplemente con el tipo
    # y typer.Argument() si quieres añadir metadatos (como la ayuda)
    engine: Annotated[str, typer.Argument(help="Container engine a usar")] = "podman",
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
    exercisename: Annotated[str, typer.Argument(
        help="Nombre del ejercicio a iniciar",
        autocompletion=exercises_autocomplete
        )],
    debug: bool = typer.Option(False, "--debug", "-d")
):
    """
    Inicia las dependencias del ejercicio correspondiente
    """
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
    exercisename: Annotated[str, typer.Argument(
        help="Nombre del ejercicio a evaluar",
        autocompletion=graders_autocomplete
        )],
    debug: bool = typer.Option(False, "--debug", "-d")
):
    """
    Evalua el ejercicio correspondiente
    """
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

def version_callback(value: bool):
    if value:
        from importlib.metadata import version
        print('version :',version("lab"))
        raise typer.Exit()

@app.callback()
def root(
    version: bool = typer.Option(
        None,
        "--version","-version",
        callback=version_callback,
        is_eager=True,
        help="Muestra la version",
    )
):
    pass



if __name__ == '__main__':
    app()