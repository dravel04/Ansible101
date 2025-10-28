# lab/infrastructure/adapters/container_adapter.py
from typing import Protocol, Tuple, Optional, Any

class ContainerAdapter:
    def __init__(self, engine="docker"):
        self.engine = engine
        if engine == "docker":
            import docker
            self.client = docker.from_env()
        # elif engine == "podman":
        #     import podman
        #     self.client = podman.from_env()
        else:
            raise ValueError(f"Unsupported engine: {engine}")

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
