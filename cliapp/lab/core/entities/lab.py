# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/core/entities/lab.py

class Lab:
    """
    Representa el estado del Laboratorio
    """
    # VALID_ENGINES = ["docker", "podman"]
    VALID_ENGINES = ["podman"]

    def __init__(self, engine: str = "podman"):
        self.engine = engine

    @property
    def engine(self) -> str:
        return self._engine

    # Usamos getter y setter para hacer validaciones en tiempo de ejecucion
    @engine.setter
    def engine(self, value: str) -> None:
        if value.lower() not in self.VALID_ENGINES:
            raise ValueError(f"Solo se soportan \"{self.VALID_ENGINES}\" como motores de contenedores para el laboratorio")
        self._engine = value.lower()
