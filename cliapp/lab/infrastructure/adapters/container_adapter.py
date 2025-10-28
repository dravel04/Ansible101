# lab/infrastructure/adapters/container_adapter.py

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

    def run_container(self, image, name, ports=None):
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

    def remove_container(self, name):
        output = ''
        failed = False
        error_output = ''
        try:
            container = self.client.containers.get(name)
            output = container.remove(force=True)
            return output, failed, error_output
        except Exception as e:
            failed = True
            error_output = f"{type(e).__name__}: {e}"
            return output, failed, error_output
