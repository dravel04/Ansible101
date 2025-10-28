# lab/infrastructure/ui/progress_notifier_adapter.py
from rich.text import Text
from rich.console import Console, Group
from rich.spinner import Spinner
from rich.text import Text
from rich.live import Live
from typing import Tuple, Callable

CheckFunc = Callable[[], Tuple[bool, str]]

class ProgressNotifierAdapter:

    # def _append_msg_with_datatime(self, instance: Exercise, msg, last=False) -> Optional[Exercise]:
    #     instance.debug_msg.append(
    #         Text.assemble(
    #             (f"[{datetime.now().strftime('%m/%d/%y %H:%M:%S')}]", "dim cyan"),
    #             (" DEBUG    ", "green"),
    #             (msg, "default"),
    #         )
    #     )
    #     if last:
    #         instance.debug_msg.append('')

    def _check_status(self, check_text: str, failed: bool, error_output: str) -> Text:
        # Mostrar el spinner durante la "validacion"
        import time
        time.sleep(2)

        # Al terminar, mostrar texto plano con el resultado
        if failed:
            final_text = (
                Text("FAILED\t", style="red")
                + Text(check_text, style="default bold")
            )
            final_text.append(Text(f"\n{error_output}", style="italic yellow"))
        else:
            final_text = (
                Text("SUCCESS\t", style="green")
                + Text(check_text, style="default bold")
            )
        return final_text


    # def run_checks(self, action: str, checks: list[Tuple[str, CheckFunc]], instance: Exercise) -> None:
    def run_checks(self, action: str, checks: list[Tuple[str, CheckFunc]]) -> None:
        console = Console()
        failed = False

        for check_text, check_fn in checks:
            spinner_line = Group(
                Spinner("dots", text=Text(check_text, style="default not bold"))
            )
            with Live(console=console, refresh_per_second=10) as live:
                live.update(spinner_line)
                failed,error_output = check_fn()
                final_text = self._check_status(check_text,failed,error_output)
                # if instance.debug_msg:
                #     group = Group(
                #             final_text,
                #             *[line for line in instance.debug_msg],
                #         )
                #     instance.debug_msg.clear()
                #     live.update(group)
                # else:
                live.update(final_text)
                
                if failed:
                    break

        if action == 'grader' and not failed:
            console.print("\nValidacion completada", highlight=False)

        print("\n")