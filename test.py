import time
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.style import Style # Aunque no se usa directamente aquí, es bueno tenerlo si se va a estilizar más

console = Console()

# Secuencia de caracteres para nuestro spinner personalizado
CUSTOM_SPINNER_CHARS = ['/', '-', '\\', '|']
DOT_COUNT = 40 # Número de puntos a mostrar

def process_line_with_in_line_spinner(
    description: str,
    simulate_duration: float = 2,
    success: bool = True
):
    """
    Simula el procesamiento de una línea con un spinner de caracter giratorio al final de los puntos,
    reemplazándolo con OK o ERROR al finalizar.
    """
    spin_index = 0
    start_time = time.time()
    
    # Prepara el texto base con la descripción y los puntos
    base_text = Text(f" · {description}") # Ya es un objeto Text
    # Calcula cuántos puntos podemos añadir hasta DOT_COUNT para la alineación
    # Se le resta el prefijo " · " (3 caracteres) y la longitud de la descripción
    remaining_dots = max(0, DOT_COUNT - (len(description) + 3)) 
    base_text.append("." * remaining_dots, style="grey50")

    # Usamos Live para animar solo esta línea
    with Live(console=console, screen=False, refresh_per_second=10) as live:
        # Dentro del while se iteran los CUSTOM_SPINNER_CHARS
        while time.time() - start_time < simulate_duration:
            # ¡La corrección clave aquí! Usa .copy() para crear una copia mutable
            current_line_text = base_text.copy() 
            
            # Añade el carácter giratorio al final
            current_line_text.append(CUSTOM_SPINNER_CHARS[spin_index], style="cyan")
            
            live.update(current_line_text)
            
            spin_index = (spin_index + 1) % len(CUSTOM_SPINNER_CHARS)
            time.sleep(0.1) # Controla la velocidad de la animación del spinner

        # Una vez finalizada la simulación, reemplaza el spinner por OK/ERROR
        final_line_text = base_text.copy() # De nuevo, usa .copy() para la versión final
        
        if success:
            final_line_text.append(" OK", style="bold green")
        else:
            final_line_text.append(" ERROR", style="bold red")
        
        live.update(final_line_text)
        # Aseguramos que la última actualización se mantenga antes de que Live se cierre
        time.sleep(0.1) 


# --- Ejecución de las líneas ---

console.print("Iniciando chequeos del ejercicio...")

process_line_with_in_line_spinner("Checking lab systems", simulate_duration=2, success=True)
process_line_with_in_line_spinner("Restoring the student user password", simulate_duration=3, success=False)
process_line_with_in_line_spinner("Verifying network connectivity", simulate_duration=1.5, success=True)
process_line_with_in_line_spinner("Installing required packages", simulate_duration=2.5, success=False)

console.print("\nChequeos finalizados.")