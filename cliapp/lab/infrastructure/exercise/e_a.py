# lab/infrastructure/exercise/e_a.py
from lab.core.entities.exercise import Exercise
from lab.infrastructure.ui.console_utils import run_with_spinner,append_msg_with_datatime
from lab.infrastructure.services.container_service import ContainerService

import logging
logger = logging.getLogger("lab")

class ExerciseA(Exercise):
    
    def create_containers(self):
        service = ContainerService(engine="docker")
        container, failed, error_output = service.run_container(
            image="ssh-ol:8.10",
            name="machine-a",
            ports={"22/tcp": 2223, "80/tcp": 8080},
        )
        if logger.isEnabledFor(logging.DEBUG) and container:
            append_msg_with_datatime(instance=self,msg=f"Name: {container.name}, Status: {container.status}, Image: {container.image}",last=True)
        return failed,error_output

    def install_packages(self):
        failed = False
        error_output = ''
        return failed,error_output

    def delete_containers(self):
        service = ContainerService(engine="docker")
        output, failed, error_output = service.remove_container('machine-a')
        failed = False
        error_output = ''
        if logger.isEnabledFor(logging.DEBUG):
            append_msg_with_datatime(instance=self,msg=f"Output: {output}",last=True)
        return failed,error_output

    def start(self):
        checks = [
            ("Creating podman containers",self.create_containers),
            ("Installing required packages",self.install_packages),
        ]
        # 🔹 logica especifica de este ejercicio
        print(f"Iniciando ejercicio {self.name}...\n")
        run_with_spinner('start', checks, instance=self)


    def finish(self):
        checks = [
            ("Removing podman containers",self.delete_containers),
        ]
        # 🔹 limpieza especifica de este ejercicio
        print(f"Finalizando ejercicio {self.name}...\n")
        run_with_spinner('finish', checks, instance=self)
