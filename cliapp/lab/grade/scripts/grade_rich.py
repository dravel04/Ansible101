from rich.console import Console
from rich.live import Live
from rich.text import Text # Necesario si vas a crear objetos Text
import time

console = Console()

def run():
  checks = [
    "Checking lab systems",
    "Restoring the student user password",
    "Verifying network connectivity",
    "Installing required packages",
  ]

  min_line_width = 60
  console.print("\nIniciando chequeos del ejercicio...", highlight=False)

  for i, check_text in enumerate(checks):
    with Live(
      # renderable=f"  [yellow]·[/yellow] {check_text.ljust(min_line_width - 5, '.')}",
      renderable=Text("  -> ", style="bold yellow") + Text(check_text.ljust(min_line_width - 5, '.'), style="default"),
      console=console,
      refresh_per_second=8,
      transient=True,
    ) as live:
      time.sleep(1 + (i * 0.2))
      success = (i % 2 == 0)

      # Imprimimos la primera parte de la cadena, y luego el objeto Text separado
      if success:
        live.console.print(
          f"  [bold blue]·[/bold blue] {check_text.ljust(min_line_width - 5, '.')}",
          Text("OK", style="bold green"),
          highlight=False
        )
      else:
        live.console.print(
          f"  [bold blue]·[/bold blue] {check_text.ljust(min_line_width - 5, '.')}",
          Text("ERROR", style="bold red"),
          highlight=False
        )

  console.print("\nTodos los chequeos completados")

if __name__ == "__main__":
  run()