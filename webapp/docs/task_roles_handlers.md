# 🧩 4: Manejo de *Tareas*, *Roles* y *Handlers*

## 🎯 Objetivos

Al finalizar este módulo serás capaz de:

1. Organizar tareas dentro de un playbook de forma limpia y estructurada.
2. Crear y utilizar **roles** para separar lógica y reutilizar código.
3. Definir y ejecutar **handlers** para gestionar reinicios, recargas o acciones condicionales.
4. Aplicar buenas prácticas de estructura en proyectos Ansible.

---

## 🧠 Teoría

### ¿Qué son las *Tasks*?

Las **tasks** son el conjuto de acciones que Ansible ejecuta sobre los hosts: instalar paquetes, crear archivos, gestionar servicios, etc, apoyandose en los diferentes módulos. Se definen dentro de `tasks:` en un playbook o en archivos externos.

Ejemplo básico:

```yaml
tasks:
  - name: Instalar Nginx
    ansible.builtin.package:
      name: nginx
      state: present
```

Las tareas se ejecutan **de arriba a abajo** en el orden en que aparecen.

---

### Separación de Tareas en Archivos

Para playbooks grandes, es común mover las tareas a archivos externos. Esto permite playbooks más limpios y estructurados:

#### `main.yml`

```yaml
- hosts: localhost
  tasks:
    - name: Incluir tareas
      ansible.builtin.include_tasks: tasks/web.yml
```

#### `tasks/web.yml`

```yaml
- name: Crear directorio web
  ansible.builtin.file:
    path: /tmp/web
    state: directory
```

---
## 🏗️ Roles

Los **roles** son la forma estándar y recomendada de **organizar, modularizar y reutilizar** lógica en Ansible.
Un rol encapsula:

- Defaults (Variables por defecto)
- Tareas (Tasks)
- Variables (Vars)
- Handlers
- Archivos (Files)
- Plantillas (Templates)

!!! abstract
    [Link](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_reuse_roles.html) a la documentación oficial

---

### Estructura interna de un rol

Estructura típica:

```
roles/
└── webserver/
    ├── tasks/
    │   ├── main.yml
    │   └── install.yml
    │   └── configure.yml
    ├── handlers/
    │   └── main.yml
    ├── templates/
    │   └── index.html.j2
    ├── files/
    │   └── static_file.txt
    ├── vars/
    │   └── main.yml
    ├── defaults/
    │   └── main.yml
    ├── meta/
    │   └── main.yml
    └── README.md
```

No es obligatorio usar todas las carpetas, pero **tasks/** y **templates/** suelen ser esenciales.

---

### **¿Cómo funciona un rol internamente?**

**El punto de entrada es siempre `tasks/main.yml`**. Es equivalente al `main()` de un programa.

Ejemplo:

```yaml
# roles/webserver/tasks/main.yml
- name: Instalar paquetes
  ansible.builtin.include_tasks: install.yml

- name: Configurar archivos
  ansible.builtin.include_tasks: configure.yml
```

`main.yml` **orquesta** internamente el rol, ejecutando **secuencialmente** otros archivos de tareas. También puede contener toda la lógica directamente, pero no es una práctica recomendable por mantenibilidad.

Esto permite dividir la lógica:

- `install.yml` → instalación de paquetes
- `configure.yml` → plantillas, permisos, etc.
- `validate.yml` → comprobaciones finales

Orden típico:

1. `tasks/main.yml`
2. Cualquier include/import dentro del main
3. handlers *al final del play*, si fueron notificados

---

### **Variables internas del rol**

**`defaults/main.yml`**

- Prioridad **más baja** de Ansible.
- Perfecto para valores por defecto que el usuario puede sobrescribir.

Ejemplo:

```yaml
# roles/webserver/defaults/main.yml
web_port: 80
web_root: /var/www/html
```

**`vars/main.yml`**

- Alta prioridad.
- Poco recomendado salvo casos especiales.

Ejemplo:

```yaml
# roles/webserver/vars/main.yml
nginx_package_name: nginx
```

---

### **Plantillas y archivos del rol**

Se acceden dentro del rol sin rutas relativas:

```yaml
ansible.builtin.template:
  src: index.html.j2
  dest: "{{ web_root }}/index.html"
```

```yaml
ansible.builtin.copy:
  src: static_file.txt
  dest: /tmp/static_file.txt
```

---

### **Dependencias entre roles**

Se declaran en: `roles/webserver/meta/main.yml`

```yaml
dependencies:
  - role: common
  - role: firewall
```

---

### **Ejemplo completo de rol**
Tenemos el role `webserver`, las partes de este serían:

1. `roles/webserver/tasks/main.yml`

```yaml
- name: Incluir instalacion
  ansible.builtin.include_tasks: install.yml

- name: Incluir configuracion
  ansible.builtin.include_tasks: configure.yml
```

2. `roles/webserver/tasks/install.yml`

```yaml
- name: Instalar nginx
  ansible.builtin.package:
    name: nginx
    state: present
```

3. `roles/webserver/tasks/configure.yml`

```yaml
- name: Deploy del index.html
  ansible.builtin.template:
    src: index.j2
    dest: "{{ web_root }}/index.html"
  notify: Recargar nginx
```

4. `roles/webserver/handlers/main.yml`

```yaml
- name: Recargar nginx
  ansible.builtin.service:
    name: nginx
    state: reloaded
```

---

### **Usar un rol en un playbook**

```yaml
- hosts: webservers
  roles:
    - webserver
```

O con parámetros:

```yaml
- hosts: webservers
  roles:
    - role: webserver
      web_port: 8080
```

---

## 🔥 Handlers

Los **handlers** son tareas especiales que se ejecutan **solo cuando son notificadas** por otra tarea.

**Ejemplo típico: reiniciar un servicio solo cuando hay cambios**

```yaml
tasks:
  - name: Copiar archivo de configuración
    ansible.builtin.template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Reiniciar nginx

handlers:
  - name: Reiniciar nginx
    ansible.builtin.service:
      name: nginx
      state: restarted
```

Características:

- Solo se ejecutan **si hubo cambios** en la tarea que los notifica
- Se ejecutan **al final del play**, después de todas las tareas
- Se pueden notificar varias veces, pero solo se ejecutan una vez
- Pueden estar dentro de un **rol** en su carpeta `handlers/`

!!! tip
    Se puede forzar que los handlers se ejecuten en un determinado momento usando
    ```yaml
    - meta: flush_handlers
    ```

---

### 🧬 Encadenamiento de Handlers

Se pueden **encadenar** handlers usando `notify` dentro de un handler:

```yaml
handlers:
  - name: Reload nginx
    ansible.builtin.service:
      name: nginx
      state: reloaded
    notify: Restart nginx

  - name: Restart nginx
    ansible.builtin.service:
      name: nginx
      state: restarted
```

---
## 🚨 Errores Comunes y Buenas Prácticas

### Errores Comunes
1. **Diferencia entre `include_tasks` y `import_tasks`**

    - `import_tasks` → **estático**, se carga en parse time
    - `include_tasks` → **dinámico**, se evalúa en runtime

    Ejemplo:
    ```yaml
    import_tasks: install.yml
    when: some_condition
    ```
    → No funciona: `import_tasks` ignora el `when`


### Buenas Prácticas

!!! tip
    - Divide `tasks/main.yml` en múltiples includes para mayor claridad
    - Pon variables modificables en `defaults/`, no en `vars/`
    - Usa nombres de variables con prefijo del rol: `webserver_port`, `webserver_root`
    - Mantén los roles autocontenidos: no dependas del proyecto
    - Usa handlers **solo** para acciones idempotentes y necesarias
    - Evita rutas absolutas dentro del rol cuando puedas parametrizar
    - Documenta el rol (README.md dentro del rol)

---

## 📚 Ejercicio Práctico

Crear un rol llamado `webdemo` que encapsule lo lógica del ejercicio del tema anterior.

Para iniciar el ejercicio, ejecuta:
```shell
lab start role
```
Esto generará la estructura:

```
webdemo/
├── defaults/
│   └── main.yml
├── tasks/
│   └── main.yml
└── ...
```

**1. Define las variables por defecto del rol**

En `webdemo/defaults/main.yml`:
```yaml
web_port: 8080
web_root: /tmp/demo
```

**2. Implementa las tareas del rol**

En `webdemo/tasks/main.yml`:
```yaml
---
- name: Incluimos la logica
  ansible.builtin.include_tasks: action.yml
```

En `webdemo/tasks/action.yml`:
```yaml
---
- name: Crear directorio web_root
  ansible.builtin.file:
    path: "{{ web_root }}"
    state: directory

- name: Crear archivo index.html
  ansible.builtin.copy:
    content: "Servidor escuchando en el puerto {{ web_port }}"
    dest: "{{ web_root }}/index.html"
```

**3. Crea un playbook que use el rol**

Crea `site.yml`:
```yaml
---
- name: Ejecutar rol webdemo
  hosts: localhost
  gather_facts: false
  roles:
    - role: webdemo
```

**4. Ejecuta playbook completo**

```bash
ansible-playbook site.yml -v
```

Para evaluar el ejercicio, ejecuta:
```shell
lab grade role
```

🔬 **Desafío adicional**

  - Agrega una tarea que muestre con `debug:` la ruta completa del archivo creado
  - Agrega una tarea que muestre con `debug:` el contenido del archivo creado (se puede hacer en varios pasos)

```yaml
- name: Mostrar ruta completa del archivo creado
  ansible.builtin.debug:
    msg: "Archivo creado: {{ web_root }}/index.html"

- name: Leer contenido del archivo creado
  ansible.builtin.slurp:
    src: "{{ web_root }}/index.html"
  register: index_raw

- name: Mostrar contenido del archivo creado
  ansible.builtin.debug:
    msg: "{{ index_raw.content | b64decode }}"
```

**5. Ejecuta y prueba sobrescribir variables con `-e`**

```bash
ansible-playbook site.yml -e web_port=9090
```
