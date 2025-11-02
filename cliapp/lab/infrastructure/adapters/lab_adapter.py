# lab/infrastructure/adapters/lab_adapter.py
from typing import Tuple, Dict
from lab.core.entities.lab import Lab
import logging

from lab.core.interfaces.container_port import ContainerPort

logger = logging.getLogger("lab")

class LabAdapter:

    def verify_context(self) -> Tuple[bool, str]:
        import subprocess
        import shutil
        failed: bool = False
        error_output: str = ''
        # comprobamos si el ejecutable `ansible` existe en PATH
        ansible_path = shutil.which("ansible")
        # if ansible_path is None:
        if ansible_path is None:
            failed = True
            error_output = 'Ansible no esta disponible en el entorno actual'
            return failed, error_output 
        try:
            result = subprocess.run(
                ["ansible", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            version_line = result.stdout.splitlines()[0]
            return failed, error_output
        except subprocess.CalledProcessError as e:
            failed = True
            error_output = "No se pudo ejecutar `ansible --version`. Verifica la instalacion"
            return failed, error_output 
        except FileNotFoundError:
            failed = True
            error_output = "No se encontro el ejecutable de Ansible en el PATH"
            return failed, error_output 

    
    def init(self, container_service: ContainerPort, LAB_IMAGES: Dict[str, Dict[str, str]]) -> Tuple[bool, str]:
        failed = False
        error_output = ''
        failed, error_output = container_service.init_client()
        if failed:
            return failed, error_output
        for image in LAB_IMAGES.items():
            failed, error_output = container_service.build_image(image)
            if failed:
                break
        return failed, error_output


