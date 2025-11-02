# lab/core/dtos/EventInfo.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class EventInfo:
    """
    Data Transfer Object (DTO) para la informacion de un evento.
    Se utiliza para transferir datos de estado entre capas
    """
    name: str
    failed: bool = False
    error_msg: Optional[str] = None
