# lab/infrastructure/adapters/container_adapter.py
from typing import Dict, Tuple, Optional, Any
import logging

logger = logging.getLogger("lab")

class ContainerAdapter:
    def __init__(self, engine="docker"):
        self.engine = engine
        self.client = None

    def init_client(self) -> Tuple[bool, str]:
        import shutil
        import subprocess
        failed = False
        error_output = ''
        if not shutil.which(self.engine):
            failed = True
            error_output = f"El cliente '{self.engine}' no se cuentra instalado"
            return failed, error_output
        try:
            result = subprocess.run(
                [self.engine, "info"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                failed = True
                error_output = f"No se puede contactar con la API del cliente '{self.engine}'. Revise que este inicializado con el comando `{self.engine} ps`"
                return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"No se puede contactar con la API del cliente '{self.engine}'. Revise que este inicializado con el comando `{self.engine} ps`"
            return failed, error_output

        if self.engine == "docker":
            import docker
            self.client = docker.from_env()
        # elif engine == "podman":
        #     import podman
        #     self.client = podman.from_env()
        return failed, error_output

    def build_image(
        self,
        image: Tuple[str, Dict[str, str]]
    ) -> Tuple[bool, str]:
        name, info = image
        failed = False
        error_output = ''

        try:
            import tempfile
            assert self.client is not None
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='Containerfile') as tmp_file:
                tmp_file.write(info['content'])
                tmp_file.flush()  # aseguramos que todo se escriba
                dockerfile_path = tmp_file.name

            # Construir la imagen usando el Containerfile temporal
            self.client.images.build(
                path=".",  # contexto actual
                dockerfile=dockerfile_path,
                tag=info['tag'],
                rm=True
            )
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"

        return failed, error_output

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
            assert self.client is not None
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
            assert self.client is not None
            container = self.client.containers.get(name)
            container.remove(force=True)
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return failed, error_output
