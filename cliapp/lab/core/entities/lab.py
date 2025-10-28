# lab/core/entities/lab.py

class Lab:
    """
    Representa el estado del Laboratorio
    """
    VALID_ENGINES = ["docker", "podman"]

    def __init__(self, engine: str = "docker"):
        # Regla de Dominio: validar el motor
        if engine.lower() not in self.VALID_ENGINES:
            raise ValueError(f"Motor '{engine}' no soportado por las reglas del Lab.") 
        
        self.engine = engine.lower()

    # Se pueden añadir métodos para la lógica de negocio, ej:
    # def register_exercise(self, name: str): ...