# ⚙️ Módulo 2: Fundamentos de Ansible

## 🎯 Objetivos

Al finalizar este módulo, serás capaz de:

1. Ejecutar **comandos ad-hoc** para realizar acciones rápidas sobre hosts gestionados.
2. Comprender la **estructura y sintaxis** de un playbook en YAML.
3. Crear y ejecutar **tareas simples y compuestas** dentro de un playbook.
4. Utilizar **módulos comunes** de Ansible en tareas cotidianas.
5. Diferenciar entre la **ejecución puntual (ad-hoc)** y la **automatización persistente (playbooks)**.

---

## 🧠 Teoría

### Comandos *Ad-hoc*: la forma más directa de automatizar

Los **comandos ad-hoc** son una forma rápida de ejecutar tareas simples en uno o varios hosts **sin escribir un playbook**.

Sintaxis general:

```bash
ansible <grupo_o_host> -m <módulo> -a "<argumentos>"
```

Ejemplos:

| Objetivo               | Comando                                                               |
| ---------------------- | --------------------------------------------------------------------- |
| Comprobar conectividad | `ansible all -m ping`                                                 |
| Ver versión del kernel | `ansible all -m command -a "uname -r"`                                |
| Crear un directorio    | `ansible all -m file -a "path=/tmp/demo state=directory"`             |
| Instalar un paquete    | `ansible webservers -m apt -a "name=nginx state=present become=true"` |

!!! note
Los comandos ad-hoc son ideales para pruebas o tareas simples, pero no son **repetibles ni versionables**.
Para automatización real, siempre se recomienda un *playbook*.

---

### Sintaxis de un Playbook

Un **playbook** es un archivo YAML que describe uno o más *plays*.
Cada *play* define:

1. **A qué hosts** se aplicará (`hosts:`)
2. **Qué tareas** se ejecutarán (`tasks:`)
3. **Con qué permisos** (`become:`)
4. Opcionalmente, **roles**, **variables**, o **handlers**

Ejemplo básico:

```yaml
---
- name: Instalar y habilitar Nginx
  hosts: webservers
  become: true
  tasks:
    - name: Instalar Nginx
      ansible.builtin.package:
        name: nginx
        state: present

    - name: Iniciar y habilitar el servicio
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true
```

!!! tip
YAML es **sensible a la indentación**.
Usa **espacios (no tabulaciones)** y asegúrate de mantener la jerarquía clara.

---

### Anatomía de un Playbook

Cada *playbook* se compone de **bloques lógicos**:

| Elemento    | Descripción                                               | Ejemplo                     |
| ----------- | --------------------------------------------------------- | --------------------------- |
| `hosts:`    | Define sobre qué grupo de servidores se ejecutará el play | `hosts: webservers`         |
| `become:`   | Permite ejecutar tareas como superusuario (sudo)          | `become: true`              |
| `tasks:`    | Lista de acciones a ejecutar                              | Ver ejemplo arriba          |
| `vars:`     | Define variables internas del playbook                    | `vars: { pkg_name: nginx }` |
| `handlers:` | Tareas que se ejecutan solo cuando se notifican           | `notify: Reiniciar Nginx`   |

---

### Módulos Comunes

Algunos módulos de uso frecuente:

| Módulo    | Propósito                               | Ejemplo                                                      |
| --------- | --------------------------------------- | ------------------------------------------------------------ |
| `ping`    | Verificar conexión y autenticación      | `ansible all -m ping`                                        |
| `command` | Ejecutar un comando sin shell           | `ansible all -m command -a "uptime"`                         |
| `shell`   | Ejecutar comandos dentro de una shell   | `ansible all -m shell -a "cat /etc/os-release"`              |
| `file`    | Gestionar archivos y permisos           | `ansible all -m file -a "path=/tmp/demo state=directory"`    |
| `copy`    | Copiar archivos locales a hosts remotos | `ansible all -m copy -a "src=./test.txt dest=/tmp/test.txt"` |
| `service` | Controlar servicios del sistema         | `ansible all -m service -a "name=nginx state=restarted"`     |

!!! warning
Usa el módulo `shell` **solo cuando sea necesario**.
Prefiere módulos específicos (`user`, `package`, `service`, `copy`, etc.) que son **idempotentes** y más seguros.

---

## ⚙️ Ejemplo Práctico Paso a Paso

Vamos a practicar el flujo completo:
1️⃣ Ejecutar un comando ad-hoc
2️⃣ Crear un playbook con tareas equivalentes

### 1. Comando ad-hoc

Creamos un directorio `/tmp/webdemo` en `localhost`:

```bash
ansible localhost -m file -a "path=/tmp/webdemo state=directory" -c local
```

Salida esperada:

```
localhost | CHANGED => {
    "path": "/tmp/webdemo",
    "state": "directory",
    "changed": true
}
```

---

### 2. Crear el mismo resultado con un Playbook

Archivo `webdemo.yml`:

```yaml
---
- name: Crear estructura de demo web
  hosts: localhost
  connection: local
  tasks:
    - name: Crear directorio de trabajo
      ansible.builtin.file:
        path: /tmp/webdemo
        state: directory

    - name: Crear un index.html básico
      ansible.builtin.copy:
        dest: /tmp/webdemo/index.html
        content: "<h1>Servidor gestionado con Ansible</h1>"

    - name: Mostrar mensaje final
      ansible.builtin.debug:
        msg: "La estructura web se ha creado correctamente en /tmp/webdemo"
```

Ejecutar:

```bash
ansible-playbook webdemo.yml
```

Salida esperada:

```
PLAY [Crear estructura de demo web] *******************************************

TASK [Crear directorio de trabajo] ********************************************
changed: [localhost]

TASK [Crear un index.html básico] *********************************************
changed: [localhost]

TASK [Mostrar mensaje final] **************************************************
ok: [localhost] => {
    "msg": "La estructura web se ha creado correctamente en /tmp/webdemo"
}

PLAY RECAP ********************************************************************
localhost : ok=3  changed=2  failed=0
```

---

## 🚨 Errores Comunes y Buenas Prácticas

### Errores Comunes

1. **Indentación incorrecta (YAML)**

   ```
   ERROR! mapping values are not allowed here
   ```

   → Usa **2 espacios por nivel**, nunca tabulaciones.

2. **Error de conexión**

   ```
   UNREACHABLE! => Failed to connect via ssh
   ```

   → Verifica el `inventory` y los permisos de acceso.

3. **Uso indebido de `shell`**
   → Si puedes lograrlo con un módulo, **no uses `shell` o `command`**.

---

### Buenas Prácticas

!!! tip
- Los comandos ad-hoc son para **acciones rápidas**, no para automatizaciones permanentes.
- Los playbooks deben ser **claros y repetibles**, y siempre versionados en Git.
- Usa nombres descriptivos en las tareas (`name:`).
- Mantén un formato uniforme en YAML y agrupa tareas relacionadas.
- Añade comentarios y usa variables para evitar valores “hardcodeados”.

---

## 🧩 Ejercicio Propuesto

Crea un **playbook llamado `system_info.yml`** que:

1. Se ejecute sobre `localhost` (conexión local).
2. Obtenga y muestre la siguiente información:

   * Nombre del sistema operativo (`ansible_distribution`)
   * Versión (`ansible_distribution_version`)
   * Dirección IP principal (`ansible_default_ipv4.address`)
3. Guarde la información en un archivo `/tmp/system_info.txt` en formato de texto plano.
4. Muestre un mensaje final con `debug:` confirmando la creación del archivo.

Pistas:

* Usa el módulo `copy` con la opción `content:` para escribir directamente el texto.
* Puedes usar **facts** de Ansible (`{{ ansible_facts.<campo> }}`).

!!! note
Este ejercicio te enseña a combinar **módulos**, **facts** y **variables**, los tres pilares del trabajo diario con Ansible.
