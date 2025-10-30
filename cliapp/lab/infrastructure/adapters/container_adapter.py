# lab/infrastructure/adapters/container_adapter.py
from typing import Tuple, Optional, Any
import logging
import sys

logger = logging.getLogger("lab")

class ContainerAdapter:
    def __init__(self, engine="docker"):
        self.engine = engine
        self._init_client()
        if engine == "docker":
            import docker
            self.client = docker.from_env()
        # elif engine == "podman":
        #     import podman
        #     self.client = podman.from_env()

    def _init_client(self) -> None:
        import shutil
        import subprocess
        import sys
        if not shutil.which(self.engine):
            print(f"El cliente '{self.engine}' no se cuentra instalado")
            sys.exit(1)
        try:
            result = subprocess.run(
                [self.engine, "info"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                print(f"No se puede contantar con la API del cliente '{self.engine}'. Revise que este inicializado con el comando `{self.engine} ps`")
                sys.exit(1)
        except Exception as e:
            print(f"No se puede contantar con la API del cliente '{self.engine}'. Revise que este inicializado con el comando `{self.engine} ps`")
            sys.exit(1)

    def run_container(
        self,
        image: str,
        name: str,
        ports: Optional[dict] = None,
    ) -> Tuple[Any, bool, str]:
        failed = False
        error_output = ''
        container = None
        try:
            container = self.client.containers.run(
                image=image,
                detach=True,
                name=name,
                hostname=name,
                ports=ports,
            )
            return container, failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return container, failed, error_output

    def remove_container(
        self,
        name: str,
    ) -> Tuple[bool, str]:
        failed = False
        error_output = ''
        try:
            container = self.client.containers.get(name)
            container.remove(force=True)
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return failed, error_output
