# lab/application/use_cases/exercise/exercise_a.py
from typing import Tuple, Union, List
from rich.text import Text
import logging
import sys
import time
from pathlib import Path

from lab.core.dtos.EventInfo import EventInfo
from lab.core.interfaces.container_port import ContainerPort
from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort
from lab.infrastructure.adapters.container_adapter import ContainerAdapter

logger = logging.getLogger("lab")

class ExerciseFinal:
    """
    Logica para inicializacion del ejercicio "Proyecto Final"
    """
    def __init__(self, name: str, debug_msg: List[Union[str, Text]] = []):
        self.name = name
        self.debug_msg = debug_msg

    def _create_containers(self, container_provider: ContainerPort) -> Tuple[bool, str]:
        """
        Implementa la creacion del contenedor web y de base de datos
        """
        container, failed, error_output = container_provider.run_container(
            image="lab-ssh-ol8",
            name="web1",
            ports={"22/tcp": 2232, "80/tcp": 8080},
        )
        container, failed, error_output = container_provider.run_container(
            image="lab-ssh-ol8",
            name="db1",
            ports={"22/tcp": 2233},
        )
        return failed, error_output

    def _config_ssh_env(self) -> Tuple[bool, str]:
        """
        Configura el entorno SSH creando o actualizando una entrada 'web1'
        al final de ~/.ssh/config. Si falla, devuelve failed=True y un mensaje.
        """
        import textwrap
        failed = False
        error_output = ''
        time.sleep(1)
        try:
            entry_names = ["web1", "db1"]
            desired_entries = [
                textwrap.dedent("""\
                    Host web1
                        Hostname localhost
                        Port 2232
                        User ansible
                        IdentityFile ~/.ssh/id_lab
                        StrictHostKeyChecking no
                        UserKnownHostsFile /dev/null
                """),
                textwrap.dedent("""\
                    Host db1
                        Hostname localhost
                        Port 2233
                        User ansible
                        IdentityFile ~/.ssh/id_lab
                        StrictHostKeyChecking no
                        UserKnownHostsFile /dev/null
                """)
            ]
            # --- Crear ~/.ssh/config si no existe ---
            ssh_dir = Path.home() / ".ssh"
            config_file = ssh_dir / "config"
            if not config_file.exists():
                config_file.touch(mode=0o600)
            for i in range(2):
                # --- Leer contenido actual ---
                content = config_file.read_text().splitlines(keepends=False)
                new_lines = []
                inside_target = False
                # --- Procesar cada línea ---
                for line in content:
                    stripped = line.strip()
                    # Si empieza un bloque Host...
                    if stripped.startswith("Host "):
                        # Si veníamos de un bloque a eliminar
                        if inside_target:
                            inside_target = False
                        # Si es el Host que queremos reemplazar
                        if stripped == f"Host {entry_names[i]}":
                            inside_target = True
                            continue  # saltamos este bloque
                    # Si estamos dentro del bloque objetivo, no copiamos nada
                    if inside_target:
                        continue
                    # Si no estamos dentro, mantenemos la línea
                    new_lines.append(line)
                # --- Añadir bloque actualizado ---
                new_lines.extend(desired_entries[i].splitlines())
                # --- Guardar el fichero final ---
                config_file.write_text("\n".join(new_lines) + "\n")
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"Error configurando ~/.ssh/config: {e}"
            return failed, error_output
    
    def _ansible_config(self) -> Tuple[bool, str]:
        import textwrap
        failed = False
        error_output = ""
        inventory_text = textwrap.dedent("""\
            [webservers]
            web1 ansible_host=web1
            [dbservers]
            db1 ansible_host=db1
            [app:children]
            webservers
            dbservers
        """)
        try:
            config_file = Path.cwd() / "ansible.cfg"
            config_file.touch(exist_ok=True)
            config_file.write_text("[defaults]\ninventory = ./inventory\nhost_key_checking = False\n")
            config_file = Path.cwd() / "inventory"
            config_file.touch(exist_ok=True)
            config_file.write_text(inventory_text)
            time.sleep(1)
        except: 
            failed = True
            error_output = "Fallo en la configuracion del entorno"
        return failed, error_output

    def _role_creation(self, role_name: str) -> Tuple[bool, str]:
        """Crea un role de Ansible usando ansible-galaxy init."""
        import subprocess
        failed = False
        error_output = ""
        time.sleep(0.5)
        roles_dir = Path.cwd() / "roles"
        roles_dir.mkdir(exist_ok=True)
        role_path = roles_dir / role_name
        if not role_path.exists():
            res = subprocess.run(
                ["ansible-galaxy", "init", role_path],
                capture_output=True,
                text=True,
                check=False  # No lanza excepcion si falla
            )
            if res.returncode != 0:
                failed = True
                error_output = (
                    f"{res.stderr.strip()}"
                )
        return failed, error_output

    def _role_cleanup(self, role_name: str) -> Tuple[bool, str]:
        """Crea un role de Ansible usando ansible-galaxy init."""
        import shutil
        from pathlib import Path
        time.sleep(0.5)
        failed = False
        error_output = ""
        try:
            role_path = Path.cwd() / "roles"/ role_name
            subdirs = ["files", "meta", "tests", "vars"]
            for sub in subdirs:
                sub_path = role_path / sub
                if sub_path.exists():
                    shutil.rmtree(sub_path)
            return failed, error_output
        except Exception as e:
            failed = True
            error_output = f"Error eliminando el role '{role_name}': {e}"
            return failed, error_output
        
    def _create_playbook(self) -> Tuple[bool, str]:
        failed = False
        error_output = ""
        try:
            file_path = Path.cwd() / "site.yml"
            file_path.touch(exist_ok=True)
            time.sleep(1)
        except: 
            failed = True
            error_output = "Fallo en la creacion del fichero: site.yml"
        return failed, error_output

    def _delete_containers(self, container_provider: ContainerPort) -> Tuple[bool, str]:
        failed = False
        error_output = ''
        for container in ['web1','db1']:
            failed, error_output = container_provider.remove_container(container)
        return failed, error_output

    def start(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion del inicio: Define la secuencia de eventos.
        """
        container_service = ContainerAdapter()
        container_service.init_client()
        event_info = EventInfo(name='Creando containers: web1, db1')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._create_containers(container_service)
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Configurando ~/.ssh para acceder al contenedor')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._config_ssh_env()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Preprando el entorno de Ansible')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._ansible_config()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        for role_name in ['apache','nginx','postgresql']:
            event_info = EventInfo(name=f'Creando ansible role: {role_name.capitalize()}')
            spinner_handle, finished_event = notifier.start(event_info)
            failed, error_output = self._role_creation(role_name=role_name)
            event_info.failed = failed; event_info.error_msg = error_output
            notifier.finish(spinner_handle, finished_event)
            sys.exit(1) if event_info.failed else None

            event_info = EventInfo(name=f'Limpiando carpetas NO necesarias del rol {role_name.capitalize()}')
            spinner_handle, finished_event = notifier.start(event_info)
            failed, error_output = self._role_cleanup(role_name=role_name)
            event_info.failed = failed; event_info.error_msg = error_output
            notifier.finish(spinner_handle, finished_event)
            sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Creacion del playbook principal: site.yml')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._create_playbook()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

    
    def finish(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion de finalizacion: Define la secuencia de eventos.
        """
        container_service = ContainerAdapter()
        container_service.init_client()
        event_info = EventInfo(name='Eliminando containers: web1, db1')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = self._delete_containers(container_service)
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None
