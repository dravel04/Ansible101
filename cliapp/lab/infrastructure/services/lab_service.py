# lab/infrastructure/services/lab_service.py
import logging
from pathlib import Path
from lab.core.entities.lab import Lab
from lab.core.interfaces.lab_provider import LabProvider

logger = logging.getLogger("lab")

class LabService(LabProvider):
    def __init__(self, lab: Lab):
        self.context = lab
        if self.context.engine == "docker":
            import docker
            self.client = docker.from_env()
        elif self.context.engine == "podman":
            # import podman
            # self.client = podman.from_env()
            pass
        else:
            raise ValueError(f"Unsupported engine: {self.context.engine}")

    def build_image(self, dockerfile_name: str, tag: str):
        pass
        # dockerfile_path = self.dockerfiles_dir / dockerfile_name
        # try:
        #     logger.debug(f"Building image {tag} from {dockerfile_name}...")
        #     image, logs = self.client.images.build(
        #         path=str(dockerfile_path.parent),
        #         dockerfile=dockerfile_path.name,
        #         tag=tag,
        #     )
        #     for chunk in logs:
        #         if "stream" in chunk:
        #             logger.debug(chunk["stream"].strip())
        #     logger.debug(f"Image {tag} built successfully")
        #     return image, False, ""
        # except Exception as e:
        #     return None, True, f"{type(e).__name__}: {e}"

    def build_all_images(self):
        pass
        # images_to_build = [
        #     ("ssh-ol.Dockerfile", "ssh-ol:8.10"),
        #     # ("nginx.Dockerfile", "nginx:latest"), ...
        # ]
        # results = []
        # for dockerfile, tag in images_to_build:
        #     results.append(self.build_image(dockerfile, tag))
        # return results

    def init(self):
        pass
