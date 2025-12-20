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

Para tu curso, esta es la forma más clara y profesional de documentar este error en un **FAQ (Preguntas Frecuentes)**. Está diseñado para que el alumno identifique el problema visualmente y entienda la solución técnica.

---

## ❌ Error: `APIError: 500 ... error setting cgroup config`

Este error suele aparecer al ejecutar comandos como `lab start`, `podman run` o cuando Ansible intenta levantar un contenedor.

El mensaje en la terminal muestra líneas similares a estas:

> `runc create failed: unable to start container process`
> `error setting cgroup config for procHooks process`
> `openat2 /sys/fs/cgroup/.../pids.max: no such file or directory`

El motivo es porque en entornos WSL2 y sistemas Linux modernos, se utiliza **Cgroups v2** para gestionar los recursos (RAM, CPU). Por seguridad, el sistema no permite que un usuario común (rootless) modifique estos límites. Al intentar arrancar el contenedor, Podman busca archivos de control en `/sys/fs/cgroup` que no existen o para los que no tienes permiso, bloqueando el inicio del proceso.

**Solución**

Debemos forzar a Podman a usar un manejador de grupos de control más sencillo (`cgroupfs`) que no dependa de las jerarquías estrictas de Systemd.

**1. Crear el directorio de configuración del usuario:**

```bash
mkdir -p ~/.config/containers
```

**2. Crear/Editar el archivo `containers.conf`:**

```bash
nano ~/.config/containers/containers.conf
```

**3. Pegar el siguiente contenido:**

```ini
[engine]
cgroup_manager = "cgroupfs"
events_logger = "file"
```

**4. Resetear el almacenamiento de Podman:**
Para que los cambios se apliquen a contenedores que fallaron anteriormente, ejecuta:

```bash
podman system migrate
```

---

Si el error persiste y menciona `OCI runtime attempted to invoke a command that was not found`, asegúrate de tener instaladas las utilidades de mapeo de IDs:

* **En Oracle Linux / RHEL / Fedora:**
```bash
sudo dnf install -y shadow-utils
```

* **En Ubuntu / Debian:**
```bash
sudo apt install -y uidmap
```

## Script de validación del entorno

```shell
#!/bin/bash

# --- COLORES PARA EL OUTPUT ---
GREEN='\033[0-32m'
RED='\033[0-31m'
YELLOW='\033[0-33m'
BLUE='\033[0-34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===================================================${NC}"
echo -e "${BLUE}   DIAGNÓSTICO DE ENTORNO: WSL2 + PODMAN + ANSIBLE ${NC}"
echo -e "${BLUE}===================================================${NC}\n"

# 1. Verificar si es WSL2
echo -ne "1. Verificando WSL2... "
if grep -qi "microsoft" /proc/version; then
  echo -e "${GREEN}[OK]${NC}"
else
  echo -e "${YELLOW}[ADVERTENCIA] No parece ser WSL2.${NC}"
fi

# 2. Verificar Virtualización (vía lscpu)
echo -ne "2. Virtualización de CPU... "
VIRT=$(lscpu | grep -i "Virtualization" | awk '{print $2}')
if [ -z "$VIRT" ]; then
  echo -e "${RED}[ERROR] Virtualización no detectada. Revisa la BIOS.${NC}"
else
  echo -e "${GREEN}[OK] ($VIRT)${NC}"
fi

# 3. Verificar SubUIDs / SubGIDs (Rootless)
echo -ne "3. Configuración de SubUIDs (Rootless)... "
if [ -f /etc/subuid ] && grep -q "$USER" /etc/subuid; then
  echo -e "${GREEN}[OK]${NC}"
else
  echo -e "${RED}[FALLO] Usuario no encontrado en /etc/subuid.${NC}"
  echo -e "   -> Ejecuta: sudo usermod --add-subuids 100000-165535 $USER"
fi

# 4. Verificar Systemd
echo -ne "4. Estado de Systemd... "
if ps --no-headers -o comm 1 | grep -q "systemd"; then
  echo -e "${GREEN}[ACTIVO]${NC}"
else
  echo -e "${RED}[INACTIVO]${NC}"
  echo -e "   -> Revisa /etc/wsl.conf y haz 'wsl --shutdown' en Windows."
fi

# 5. Verificar Cgroup Manager (Solución al error 500)
echo -ne "5. Configuración de Cgroup Manager... "
if [ -f ~/.config/containers/containers.conf ] && grep -q "cgroupfs" ~/.config/containers/containers.conf; then
  echo -e "${GREEN}[CORRECTO (cgroupfs)]${NC}"
else
  echo -e "${YELLOW}[RECOMENDADO] Cambiar a cgroupfs en ~/.config/containers/containers.conf para evitar errores 500.${NC}"
fi

# 6. Probar Socket de Podman
echo -ne "6. Socket de Podman para Ansible... "
if [ -S "/run/user/$UID/podman/podman.sock" ]; then
  echo -e "${GREEN}[CONECTADO]${NC}"
else
  echo -e "${RED}[DESCONECTADO]${NC}"
  echo -e "   -> Ejecuta: systemctl --user enable --now podman.socket"
fi

# 7. Verificar Ansible
echo -ne "7. Instalación de Ansible... "
if command -v ansible &> /dev/null; then
  VERSION=$(ansible --version | head -n 1)
  echo -e "${GREEN}[OK] ($VERSION)${NC}"
else
  echo -e "${RED}[NO ENCONTRADO]${NC}"
fi

echo -e "\n${BLUE}===================================================${NC}"
echo -e "${BLUE}             FIN DEL DIAGNÓSTICO                  ${NC}"
echo -e "${BLUE}===================================================${NC}"
```
