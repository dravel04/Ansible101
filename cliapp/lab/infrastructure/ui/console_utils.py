from rich.text import Text
from rich.console import Console, Group
from rich.spinner import Spinner
from rich.text import Text
from rich.live import Live
import time

def check_status(failed, check_text, live_renderable):
    # Mostrar el spinner durante la "validacion"
    time.sleep(2)

    # Al terminar, mostrar texto plano con el resultado
    if failed:
        final_text = (
            Text("FAILED\t", style="red")
            + Text(check_text, style="default bold")
        )
    else:
        final_text = (
            Text("SUCCESS\t", style="green")
            + Text(check_text, style="default bold")
        )

    live_renderable.update(final_text)
    return True


def run_with_spinner(action, checks):
    console = Console()

    for check_text, check_fn in checks:
        spinner_line = Group(
            Spinner("dots", text=Text(check_text, style="default not bold"))
        )
        with Live(spinner_line, console=console, refresh_per_second=10) as live:
            failed = check_fn()
            check_status(failed, check_text, live)

    if action == 'grader':
        console.print("\nValidacion completada", highlight=False)
