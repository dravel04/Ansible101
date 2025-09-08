from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.spinner import Spinner
from rich.table import Table
import time

console = Console()
min_line_width = 50
table = Table(show_header=False, box=None, padding=(0, 1))
table.add_column("status", width=7)  # ancho fijo
table.add_column("description")

def check_exercise_status(failed, check_text, row_index, live):
    # Simula validación que tarda
    time.sleep(2)

    # Sustituye el spinner por el estado final
    if failed:
        status = Text("FAILED", style="red")
    else:
        status = Text("SUCCESS", style="green")

    print('row_index:',row_index)
    table.rows[row_index]._cells = (status, Text(check_text,style='default bold'))
    live.update(table)



def run_validations():
    checks = [
        "Checking lab systems",
        "Restoring the student user password",
        "Verifying network connectivity",
        "Installing required packages",
    ]

    console.print("\nIniciando validación de ejercicios...\n", highlight=False)

    # Usamos Live con la tabla completa
    for i, check_text in enumerate(checks):
        spinner = Spinner("dots")
        table.add_row(spinner, Text(check_text, style="default bold"))
        failed = (i % 2 == 0)
        with Live(table, console=console,refresh_per_second=10) as live:
            check_exercise_status(failed, check_text, i, live)

    console.print("\nValidación completada.", highlight=False)


if __name__ == "__main__":
    run_validations()
