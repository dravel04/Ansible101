import click
# from click_completion import init

from lab.grade import grade_func

# Inicializa la extensión de autocompletación de Click
# init()

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
# @click.argument('exercisename', autocompletion=None)
@click.argument('exercisename')
def start(exercisename):
    """Inicia las dependencias del ejercicio correspondiente."""
    click.echo(f"Iniciando ejercicio: {exercisename}")

@cli.command()
# @click.argument('exercisename', autocompletion=None)
@click.argument('exercisename')
def grade(exercisename):
    """Evalua el ejercicio correspondiente"""
    grade_func(exercisename)

@cli.command()
# @click.argument('exercisename', autocompletion=None)
@click.argument('exercisename')
def finish(exercisename):
    """Libera las dependencias del ejercicio correspondiente"""
    click.echo(f"Fininalizando ejercicio: {exercisename}")

if __name__ == '__main__':
    cli()