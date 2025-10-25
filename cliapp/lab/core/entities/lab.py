# core/entities/lab.py
import json
from pathlib import Path

class Lab:
    CONFIG_PATH = Path.home() / ".lab_config.json"
    def __init__(self, engine: str = "docker"):
        self.engine = engine

    def save(self):
        self.CONFIG_PATH.write_text(json.dumps({"engine": self.engine}))

    @classmethod
    def load(cls, force):
        exists = True
        # Si no hay archivo, devolvemos un Lab por defecto
        if force or not cls.CONFIG_PATH.exists():
            exists = False
            return exists, cls()
        # Lo leemos como texto y convertimos a diccionario
        data = json.loads(cls.CONFIG_PATH.read_text())
        # Creamos un objeto Lab con esos datos
        # '*' → Desempaqueta iterables (listas, tuplas, diccionarios) como argumentos posicionales. Si es un diccionario, solo toma las keys, no los values.
        # '**' → Desempaqueta un diccionario como argumentos por nombre, donde las keys deben coincidir con los nombres de los parámetros de la función y los values se asignan a esos parámetros.
        return exists, cls(**data)
