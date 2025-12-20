<!-- This file is part of LAB CLI. -->
<!-- Copyright (C) 2025 Rafael Marín Sánchez (dravel04 - rafa marsan) -->
<!-- Licensed under the GNU GPLv3. See LICENSE file for details. -->

# 🧩 2: Fundamentos de Ansible

## 🎯 Objetivos

Al finalizar este módulo, serás capaz de:

1. Entender que son los **inventarios** y cómo se usan
2. Ejecutar **comandos ad-hoc** para realizar acciones rápidas
3. Comprender la **estructura y sintaxis** de un playbook en YAML
4. Crear y ejecutar **tareas simples y compuestas** dentro de un playbook
5. Utilizar **módulos comunes** de Ansible
6. Diferenciar entre la **ejecución puntual (ad-hoc)** y la **automatización persistente (playbooks)**

---

## 🧠 Teoría

### Inventarios

En **Ansible**, un **inventario** es un fichero donde se define **qué máquinas vamos a gestionar** y cómo conectarnos a ellas. Permite organizar tus servidores en **grupos** y asignarles variables específicas.

Los inventarios pueden estar en varios formatos:

- **INI** (el más clásico)
- **YAML**
- **JSON**

#### Ejemplo de inventario en formato INI

```ini
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[dbservers]
db1 ansible_host=192.168.1.20

[app:children]
webservers
dbservers
```

- `webservers` y `dbservers` son **grupos de hosts**.
- `app` es un **grupo que agrupa otros grupos** (children).
- `ansible_host` indica la IP o DNS al que conectarse.
- Podemos definir variables de grupo o de host dentro del inventario, por ejemplo:

```ini
[webservers:vars]
ansible_user=ubuntu
apache_port=8080
```

#### Ejemplo de inventario en formato YAML

```yaml
all:
  children:
    webservers:
      hosts:
        web1:
          ansible_host: 192.168.1.10
        web2:
          ansible_host: 192.168.1.11
      vars:
        ansible_user: ubuntu
        apache_port: 8080
    dbservers:
      hosts:
        db1:
          ansible_host: 192.168.1.20
    app:
      children:
        webservers: {}
        dbservers: {}
```
!!! info "Resumen"
    El inventario **define el inventario físico y lógico de tus hosts**, permite **agruparlao**, asignar **variables por host o por grupo**. Es **la base para ejecutar cualquier playbook o comando ad-hoc**.


### Comandos *Ad-hoc*

Los **comandos ad-hoc** son una forma rápida de ejecutar tareas simples en uno o varios máquinas **sin escribir un playbook**

Sintaxis general:

```bash
ansible -i <fichero_inventario> <grupo_o_host> -m <módulo> -a "<argumentos>"
```
!!! info
    Para evitar tener que usar el `-i <inventory_file>` todo el rato es recomendable definir la linea `inventory = ./inventory` en el fichero **ansible.cfg**.      
    Al usar tanto `ansible` como `ansible-playbook` en el directorio donde tengamos el fichero, no hará falta usar el `-i`

Ejemplos:

| Objetivo               | Comando                                                               |
| ---------------------- | --------------------------------------------------------------------- |
| Comprobar conectividad | `ansible -i inventory all -m ping`                                                 |
| Ver versión del kernel | `ansible -i inventory all -m command -a "uname -r"`                                |
| Crear un directorio    | `ansible -i inventory all -m file -a "path=/tmp/demo state=directory"`             |
| Instalar un paquete    | `ansible -i inventory webservers -m apt -a "name=nginx state=present become=true"` |

!!! note
    Los **comandos ad-hoc** sirven para pruebas o tareas simples, pero no son **repetibles ni versionables**.       
    Para automatización completa, siempre se recomienda un **playbook**

---

### Sintaxis de un Playbook

Un **playbook** es un archivo YAML que describe uno o más [*plays*](./introduction.md#plays).
Cada *play* define:

1. **A qué hosts** se aplicará (`hosts:`)
2. **Qué tareas** se ejecutarán (`tasks:`)
3. **Con qué permisos** (`become:`)
4. Opcionalmente, **roles**, **variables**, o **handlers**

Ejemplo:

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
    YAML es **sensible a la indentación** y Ansible, por defecto, requiere el uso de **espacios** (no tabulaciones).

    **Recomendación:** Configura tu editor de código para que **`TAB`** inserte **dos espacios** en lugar de un carácter de tabulación. Esto previene la mayoría de los errores de sintaxis.

---

Cada *playbook* se compone de **bloques lógicos**:

| Elemento    | Descripción                                               | Ejemplo                     |
| ----------- | --------------------------------------------------------- | --------------------------- |
| `hosts:`    | Define sobre qué grupo de servidores se ejecutará el play | `hosts: webservers`         |
| `become:`   | Permite ejecutar tareas como superusuario (sudo)          | `become: true`              |
| `gather_facts:`| Recopila automáticamente información del sistema       | `gather_facts: true`        |
| `tasks:`    | Lista de acciones a ejecutar                              | Ver ejemplo arriba          |
| `vars:`     | Define variables internas del playbook                    | `vars: { pkg_name: nginx }` |
| `handlers:` | Tareas que se ejecutan solo cuando se notifican           | `notify: Reiniciar Nginx`   |

---
**`gather_facts`**

Por defecto, cuando ejecutas un playbook, Ansible **recopila automáticamente información del sistema** de cada host antes de ejecutar las tareas. Esta información se llama **facts** y contiene detalles como:

- Nombre del sistema operativo (`ansible_distribution`)
- Versión (`ansible_distribution_version`)
- Arquitectura (`ansible_architecture`)
- IPs, interfaces de red, CPU, memoria, etc.

Esta recopilación se realiza con el módulo [`setup`](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_vars_facts.html#ansible-facts) y se activa automáticamente **porque `gather_facts: true` por defecto**.

**Ejemplo de facts comunes:**

```yaml
ansible_distribution: Ubuntu
ansible_distribution_version: "22.04"
ansible_architecture: x86_64
ansible_default_ipv4:
  address: 192.168.1.10
```

**Cuándo poner `gather_facts: false`**

- Si tu playbook no necesita información del sistema (por ejemplo, copia de archivos estáticos o instalación de paquetes conocidos)
- Para **ahorrar tiempo**, sobre todo si gestionas muchos hosts
- Para **evitar errores** en entornos donde la conexión no permite recopilar facts

!!! info "Resumen"
    - `gather_facts` es útil cuando necesitas datos dinámicos del host, pero **ponerlo a `false` mejora el rendimiento** de la ejecución 
    - Está activado por defecto si no pones explicitamente `gather_facts: false`

---

### Módulos Comunes

Los módulos más usados en **comandos ad-hoc** serían:

| Módulo    | Descripción                             | Ejemplo                                                      |
| --------- | --------------------------------------- | ------------------------------------------------------------ |
| `ping`    | Verificar conexión y autenticación      | `ansible all -m ping`                                        |
| `command` | Ejecutar un comando sin shell           | `ansible all -m command -a "uptime"`                         |
| `shell`   | Ejecutar comandos dentro de una shell   | `ansible all -m shell -a "cat /etc/os-release"`              |
| `file`    | Gestionar archivos y permisos           | `ansible all -m file -a "path=/tmp/demo state=directory"`    |
| `copy`    | Copiar archivos locales a hosts remotos | `ansible all -m copy -a "src=./test.txt dest=/tmp/test.txt"` |
| `service` | Controlar servicios del sistema         | `ansible all -m service -a "name=nginx state=restarted"`     |

!!! warning
    Usa el módulo `shell` **solo cuando sea necesario**

    Intenta usar módulos específicos (`user`, `package`, `service`, `copy`, etc.) para asegurar la **idempotencia** (obtener el mismo resultado aunque se aplique múltiples veces)

---

## ⚙️ Ejemplo Práctico

Vamos a practicar el flujo completo:

- Ejecutar un comando ad-hoc
- Crear un playbook con tareas equivalentes

### 1. Comando ad-hoc

Creamos un directorio `/tmp/webdemo` en `localhost`:

```bash
ansible localhost -m file -a "path=/tmp/webdemo state=directory"
```

Salida esperada:

```shell
localhost | CHANGED => {
    "path": "/tmp/webdemo",
    "state": "directory",
    "changed": true
}
```

---

### 2. Crear Playbook con tareas extras

> Un **playbook** nos permite ejecutar varias tareas de forma secuencial

Archivo `webdemo.yml`:

```yaml
---
- name: Crear estructura de demo web
  hosts: localhost
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

```shell
ansible-playbook webdemo.yml
```

Salida esperada:

```shell
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
    Syntax Error while loading YAML.
        mapping values are not allowed in this context
    ```

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
    - Los **comandos ad-hoc** son para **acciones rápidas**, no para automatizaciones permanentes.
    - Los playbooks deben ser **claros y repetibles**, y versionados en Git.
    - Usa nombres descriptivos en las tareas (`name:`).
    - Mantén un formato uniforme en YAML y agrupa tareas relacionadas.
    - Añade comentarios y usa variables para evitar valores “hardcodeados”.

---

## 📚 Ejercicio Propuesto

Crea un **playbook llamado `system_info.yml`** que:

1. Se ejecute sobre `localhost` (conexión local).
2. Obtenga y muestre la siguiente información:
    * Nombre del sistema operativo (`ansible_distribution`)
    * Versión (`ansible_distribution_version`)
    * Dirección IP principal (`ansible_default_ipv4.address`)
3. Guarde la información en un archivo `/tmp/system_info.txt` en formato de texto plano.
4. Muestre un mensaje final con `debug:` confirmando la creación del archivo.


!!! tip
    - Usa el módulo `copy` con la opción `content:` para escribir texto directamente en un fichero
    - Puedes obtener información de un sistema usando el módulo `setup` o añadiendo `gather_facts: true` en el **play**
        - Esa información queda definida en variables especiales que empiezan por `ansible_` ➜ [link docs](https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html)

!!! note
    Este ejercicio te enseña a combinar **módulos**, **facts** y **variables**, los tres pilares del trabajo diario con Ansible.
