# Configuración de WSL2 y Podman

## Preparación del Motor (WSL2 y Virtualización)

Antes de instalar nada, el hardware y el sistema operativo deben estar listos.

1. **Tener Virtualización habilitada:** Evitar el error `0x80370102`. Desde la **BIOS** y activar la virtualización (`Intel VT-x` o `AMD-V (SVM)`)
2. **Instalar WSL (Windows 10):** Abre PowerShell como administrador y ejecuta:
```powershell
wsl --install
wsl --update
wsl --set-default-version 2
```
3. **Instalación de la distro:** Recomendada, Ubuntu 22 LTS [docs Microsoft](https://learn.microsoft.com/es-es/windows/wsl/install)

---

## Configuración Rootless Podman

Para que Podman funcione sin `sudo`, necesitamos configurar los **User Namespaces**. Esto permite que tu usuario de Linux mapee IDs para los contenedores.

1. **Asignar rangos de IDs (SubUIDs/SubGIDs):**
Ejecuta esto reemplazando `usuario` por tu nombre en Linux:
```bash
sudo usermod --add-subuids 100000-165535 usuario
sudo usermod --add-subgids 100000-165535 usuario
```

2. **Corregir permisos de herramientas de mapeo:**
```bash
sudo chmod u+s /usr/bin/newuidmap /usr/bin/newgidmap
```

3. **Migrar configuración:**
```bash
podman system migrate
```

---

## Activación de Systemd y Montajes

WSL no inicia servicios por defecto. Necesitamos **Systemd** para que el socket de Podman esté siempre disponible para Ansible.

1. **Configurar el arranque de WSL:**
  ```bash
  sudo nano /etc/wsl.conf
  ```
  Pega este contenido:
  ```ini
  [boot]
  systemd=true
  ```

2. **Reiniciar WSL:** Sal de la terminal y en **PowerShell de Windows** ejecuta:
```powershell
wsl --shutdown
```

3. **Solucionar el "Shared Mount":** Podman necesita que la raíz sea compartida para gestionar volúmenes. Añade esto a tu `~/.bashrc`:
```bash
echo 'sudo mount --make-rshared /' >> ~/.bashrc
```
