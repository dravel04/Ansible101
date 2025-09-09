import typer
from typing_extensions import Annotated

# Typer usa un objeto Typer principal en lugar de @appck.group()
app = typer.Typer(help="Un app para tus herramientas de laboratorio.") # Puedes añadir una descripción general

@app.command()
def start(
    # Un argumento posicional se define simplemente con el tipo
    # y typer.Argument() si quieres añadir metadatos (como la ayuda)
    exercisename: Annotated[str, typer.Argument(help="Nombre del ejercicio a iniciar")]
):
    """
    Inicia las dependencias del ejercicio correspondiente
    """
    typer.echo(f"Iniciando ejercicio: {exercisename}") # typer.echo es el equivalente a appck.echo


@app.command()
def grade(
    exercisename: Annotated[str, typer.Argument(help="Nombre del ejercicio a evaluar")]
):
    """
    Evalua el ejercicio correspondiente
    """
    from lab.grade import grade_func
    grade_func(exercisename)


@app.command()
def finish(
    exercisename: Annotated[str, typer.Argument(help="Nombre del ejercicio a finalizar.")]
):
    """
    Libera las dependencias del ejercicio correspondiente
    """
    typer.echo(f"Fininalizando ejercicio: {exercisename}")


if __name__ == '__main__':
    # En lugar de app(), llamas a la instancia de Typer
    app()