# 🧩 5: Templates y Jinja2 en Ansible

## 🎯 Objetivos

Al finalizar este módulo, serás capaz de:

1. Comprender qué es un **template** y por qué es fundamental en Ansible
2. Utilizar **Jinja2** para generar archivos dinámicos mediante variables, filtros y estructuras lógicas
3. Diferenciar entre templates simples y configuraciones avanzadas basadas en lógica
4. Integrar templates dentro de roles y playbooks correctamente
5. Aplicar buenas prácticas para mantener plantillas limpias, legibles y mantenibles

---

## 🧠 Teoría

### ¿Qué es un Template en Ansible?

Un **template** es un archivo de texto que usa la sintaxis de **Jinja2** para generar contenido dinámico.
Se utilizán típicamente para:

* Configuraciones de servicios (`nginx.conf`, `php.ini`, `my.cnf`, `sshd_config`, etc.)
* Scripts con parámetros
* Archivos de entorno `.env`
* Configuración multi-host

Se procesan con el módulo:

```yaml
ansible.builtin.template
```

Los templates *siempre* viven en:

```
templates/
```

dentro del rol o del proyecto.

---

### ¿Qué es Jinja2?

**Jinja2** es un motor de plantillas que permite:

* Insertar variables
* Crear condicionales (`if`)
* Iteraciones (`for`)
* Aplicar filtros (`| lower`, `| default()`, etc.)

Ejemplo básico:

```jinja2
server {
    listen {{ web_port }};
    root {{ web_root }};
}
```

---

## 📄 Sintaxis Jinja2 Esencial

### **Variables**

```jinja2
Usuario: {{ user_name }}
```

### **Condicionales**

```jinja2
{% if enable_ssl %}
ssl on;
{% else %}
ssl off;
{% endif %}
```

### **Bucles**

```jinja2
{% for host in groups['webservers'] %}
server {{ host }};
{% endfor %}
```

### **Filtros útiles**

```jinja2
{{ web_root | default('/var/www/html') }}

{{ app_name | upper }}

{{ servers | join(', ') }}
```

---

## ⚙️ Uso de Templates en Playbooks y Roles

### Ejemplo básico en un playbook

```yaml
- hosts: web
  tasks:
    - name: Generar archivo de configuración de Nginx
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        mode: '0644'
```

### Ejemplo dentro de un rol

```
roles/
└── webserver/
    ├── tasks/main.yml
    └── templates/nginx.conf.j2
```

`tasks/main.yml`:

```yaml
- name: Plantilla de configuración de Nginx
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: "/etc/nginx/conf.d/{{ inventory_hostname }}.conf"
```

---

## 📚 Ejemplos Reales de Jinja2 en Configuración

### 1. Configuración con lista de backends

Template:
```jinja2
upstream backend {
{% for srv in backend_servers %}
  server {{ srv }}:{{ backend_port }};
{% endfor %}
}
```

Playbook:
```yaml
vars:
  backend_servers:
    - 10.0.0.10
    - 10.0.0.11
  backend_port: 9000
```

---

### 2. Configuración condicional de logs

```jinja2
{% if enable_debug %}
error_log /var/log/nginx/error.log debug;
{% else %}
error_log /var/log/nginx/error.log warn;
{% endif %}
```

---

### 3. Crear un archivo `.env` dinámico

```jinja2
APP_ENV={{ app_env }}
DEBUG={{ debug | default(false) }}
DB_HOST={{ db.host }}
DB_USER={{ db.user }}
DB_PASS={{ db.pass }}
```

---

## 🚨 Errores Comunes y Buenas Prácticas

### Errores Comunes

1. **Variables no definidas**

  Solución: `{{ var | default('valor') }}`

2. **Espacios mal puestos en el delimitador**

    ```jinja2
    {%if enabled%}   # ❌ No hay espacios después de {%
    {% if enabled%}  # ❌ Falta el espacio antes de %}
    ```
    {% y %} deben estar unidos al contenido sin pegarse
    ```
    {% if enabled %}
    ```

---

### Buenas Prácticas

!!! tip
    - Usa `default()` en TODAS las variables críticas.
    - Usa comentarios dentro del template (`#`) para documentar decisiones.
    - Evita hardcodear rutas; usa variables (`{{ config_dir }}`).
    - Prefiere variables con nombre explícito: `nginx_log_format` en vez de `log`.
    - Prueba el template con `ansible-playbook --check` antes de recargar un servicio sensible.
