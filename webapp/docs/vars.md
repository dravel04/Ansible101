# 🧩 3: Prioridad de variables en Ansible

## 🎯 Objetivos

Al finalizar este módulo, serás capaz de:

1. Definir variables en distintos niveles de Ansible (inventario, playbook, roles, etc.)
2. Comprender la **precedencia y prioridades** entre ellas
3. Utilizar **variables de entorno, facts y prompts** dentro de playbooks
4. Aplicar buenas prácticas en el uso de variables

---

## 🧠 Teoría

### ¿Qué son las Variables en Ansible?

Las **variables** permiten **parametrizar** los playbooks y tareas para que sean **reutilizables** y **flexibles**.
Pueden almacenar valores como rutas, nombres de paquetes, usuarios, direcciones IP, contraseñas, etc.

Ejemplo:

```yaml
- name: Instalar paquete configurable
  hosts: localhost
  vars:
    pkg_name: nginx
  tasks:
    - name: Instalar paquete
      ansible.builtin.package:
        name: "{{ pkg_name }}"
        state: present
```

!!! note
    Las variables se expanden con doble llave `{{ variable }}`

    Deben entrecomillarse cuando se usan al inicio:     
    `app_path: {{ base_path }}/22` ➜ `app_path: "{{ base_path }}/22"`

    Pueden usarse en cualquier parte de un playbook: rutas, nombres, comandos, etc.

---

## 📜 Dónde Definir Variables

Ansible permite definir variables en **muchos lugares**, según el contexto:

| Nivel                    | Ubicación                                          | Ejemplo o archivo                               | Comentario                                |
| :----------------------- | :------------------------------------------------- | :---------------------------------------------- | :---------------------------------------- |
| **Inventario**           | Archivo `inventory` o `group_vars/` / `host_vars/` | Define variables por host o grupo               | Ideal para información de infraestructura |
| **Playbook**             | Dentro de `vars:` o `vars_files:`                  | `vars: { pkg_name: nginx }`                     | Variables locales al playbook             |
| **Rol**                  | En `defaults/` o `vars/` del rol                   | `roles/webserver/defaults/main.yml`             | Prioridad distinta según carpeta          |
| **Variables de entorno** | Exportadas desde el sistema                        | `export ANSIBLE_VAR=value`                      | Se usan con `lookup('env', 'VAR')`        |
| **Línea de comandos**    | Usando `-e` o `--extra-vars`                       | `ansible-playbook play.yml -e "pkg_name=nginx"` | Máxima prioridad                          |
| **Facts del sistema**    | Recogidos automáticamente con `gather_facts`       | `ansible_hostname`, `ansible_distribution`      | Variables especiales del sistema remoto   |

!!! abstract
    [Link](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) a la documentación oficial

---

### Ejemplo Práctico — Variables por Niveles

Supongamos que tenemos este inventario:

```ini
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11
[webservers:vars]
app_port=80
```

Y este playbook `vars_demo.yml`:

```yaml
---
- name: Demostración de variables
  hosts: webservers
  gather_facts: false

  vars:
    app_port: 8080

  tasks:
    - name: Mostrar el valor de app_port
      ansible.builtin.debug:
        msg: "El puerto definido es {{ app_port }}"
```

Ejecuta el playbook:

```bash
ansible-playbook -i inventory vars_demo.yml
```

**Salida esperada:**

```shell
TASK [Mostrar el valor de app_port] ********************************************
ok: [web1] => {
    "msg": "El puerto definido es 8080"
}
```

👉 Aunque en el *inventory* definimos `app_port=80`, el valor dentro del **playbook (`vars`) tiene prioridad** y sobreescribe el del inventario.

---

## 🧮 Prioridad de Variables (de menor a mayor)

La precedencia determina **cuál valor “gana”** cuando una variable se define en varios lugares. 

Un número más alto en la prioridad sobreescribe al resto

| Prioridad | Nivel                                                        | Ejemplo                                           |
| :-------: | :------------------------------------------------------------| :------------------------------------------------ |
|    1      | `defaults/` dentro de un rol                                 | Valores por defecto, seguros pero sobrescribibles |
|    2      | Variables del inventario (`group_vars`, `host_vars`)         | Valores específicos de infraestructura            |
|    3      | Variables definidas en el playbook (`vars:` o `vars_files:`) | Definiciones locales                              |
|    4      | Variables de registro (`set_fact`)                           | Variables dinámicas dentro de tareas              |
|    5      | Variables de entorno (`lookup('env')`)                       | Valores del entorno del sistema                   |
|    6      | Variables pasadas por línea de comandos (`-e`)               | Tienen **máxima prioridad**                       |

!!! note
    Cuando dos variables con el mismo nombre existen en distintos niveles, **Ansible usa la de mayor prioridad**, ignorando el resto.

---

### Ejemplo — Sobrescritura de Variables

Creamos el archivo `inventory`:

```ini
[all]
localhost app_name=nginx
```

Y el playbook `vars_priority.yml`:

```yaml
---
- name: Prioridades de variables
  hosts: localhost
  connection: local
  vars:
    app_name: apache2
  tasks:
    - name: Mostrar variable definida
      ansible.builtin.debug:
        msg: "Aplicación: {{ app_name }}"
```

#### Valor desde el playbook:

```bash
ansible-playbook vars_priority.yml
```

Salida:

```shell
"msg": "Aplicación: apache2"
```

#### Sobrescribir desde la línea de comandos:

```bash
ansible-playbook vars_priority.yml -e "app_name=nginx"
```

Salida:

```shell
"msg": "Aplicación: nginx"
```

Las variables pasadas con `-e` tienen **máxima prioridad**.

---

## ⚙️ Variables de Entorno

Puedes acceder a variables del sistema con el *lookup plugin*:

```yaml
- name: Mostrar usuario actual
  ansible.builtin.debug:
    msg: "Usuario: {{ lookup('env','USER') }}"
```

Ejemplo de uso práctico en una ruta dinámica:

```yaml
- name: Copiar archivo al home del usuario
  ansible.builtin.copy:
    src: test.txt
    dest: "{{ lookup('env','HOME') }}/test.txt"
```

---

## 💡 Variables Dinámicas y Facts

Ansible puede recopilar automáticamente información del sistema remoto (facts) si `gather_facts: true`.

Ejemplo:

```yaml
- name: Mostrar información del host
  hosts: localhost
  gather_facts: true
  tasks:
    - debug:
        msg: "Sistema operativo: {{ ansible_distribution }} {{ ansible_distribution_version }}"
```

También puedes definir variables dinámicas durante la ejecución con `set_fact`:

```yaml
- name: Calcular ruta temporal
  set_fact:
    tmp_file: "/tmp/{{ ansible_hostname }}_{{ ansible_date_time.hour }}.log"
```

---

## 🚨 Errores Comunes y Buenas Prácticas

### Errores Comunes

1. **Variables no definidas**

    ```
    ERROR! 'pkg_name' is undefined
    The task includes an option with an undefined variable.
    The error was: 'pkg_name' is undefined
    ```

    → Usa `default()` en tus expresiones: `{{ pkg_name | default('nginx',true) }}`
    
    → Añadir la `true` hace que se asigne el valor default ante cadenas vacías

2. **Indentación incorrecta**

    → Afecta especialmente en bloques `vars:` y `vars_files:`.

---

### Buenas Prácticas

!!! tip
    - Define variables **al nivel más bajo posible** (local antes que global).
    - Usa `defaults/main.yml` en roles para asegurar valores seguros.
    - Evita nombres genéricos (`port`, `user`); usa prefijos (`web_port`, `db_user`).
    - Documenta el propósito de las variables.

---

## 📚 Ejercicio Práctico

Crea un playbook llamado `vars_lab.yml` que:

1. Se ejecute sobre `localhost`
2. Defina las variables:

    ```yaml
    web_port: 8080
    web_root: /tmp/demo
    ```
3. Crea el directorio `{{ web_root }}` y dentro de este un archivo `index.html` con el contenido:

    ```
    Servidor escuchando en el puerto {{ web_port }}
    ```
4. Prueba sobrescribir `web_port` desde la línea de comandos con `-e`.

🔬 **Desafío adicional:**

  - Agrega una tarea que muestre con `debug:` la ruta completa del archivo creado
  - Agrega una tarea que muestre con `debug:` el contenido del archivo creado (se puede hacer en varios pasos)
