# 🧩 6: Configuración de Servidores Web

## 🎯 Objetivo general

Al finalizar este módulo, serás capaz de:

1. Instalar y configurar Apache usando un **rol completo**
2. Instalar y configurar Nginx como **reverse proxy** hacia Apache
3. Usar **templates**, **handlers**, **variables** y **roles**
4. Ejecutar todo en un **playbook** que orquesta ambos roles

---

## 📘 **Instalación y configuración de Apache usando roles**

### 🏗️ Estructura del rol

```
roles/
  apache/
    tasks/
      main.yml
      install.yml
    templates/
      apache.conf.j2
    handlers/
      main.yml
    defaults/
      main.yml
```

**defaults/main.yml**

```yaml
apache_port: 80
apache_docroot: /var/www/html
```

**templates/httpd.conf.j2**

```jinja2
Listen {{ apache_port }}

<VirtualHost *:{{ apache_port }}>
  DocumentRoot "{{ apache_docroot }}"
  ErrorLog /var/log/httpd/error.log
  CustomLog /var/log/httpd/access.log combined
</VirtualHost>
```

**tasks/main.yml**
```yaml
- name: Cargamos modulo de instalacion
  ansible.builtin.include_tasks: install.yml
```

**tasks/install.yml**

```yaml
- name: Instalar Apache
  package:
    name: httpd
    state: present

- name: Copiar configuracion de Apache
  template:
    src: httpd.conf.j2
    dest: /etc/httpd/conf/httpd.conf
  notify: "Reiniciar Apache"

- name: Asegurar que Apache esta habilitado y activo
  service:
    name: httpd
    enabled: yes
    state: started
```

**handlers/main.yml**

```yaml
- name: Reiniciar Apache
  service:
    name: httpd
    state: restarted
```

---

## 📘 **Instalación y configuración de Nginx reverse proxy**

### 🏗️ Estructura del rol

```
roles/
  nginx/
    tasks/
      main.yml
      install.yml
    templates/
      reverse-proxy.conf.j2
    handlers/
      main.yml
    defaults/
      main.yml
```

**defaults/main.yml**

```yaml
nginx_listen_port: 8080
nginx_upstream_host: "127.0.0.1"
nginx_upstream_port: 80
```

**templates/reverse-proxy.conf.j2**

```jinja
server {
    listen {{ nginx_listen_port }};
    location / {
      proxy_pass http://{{ nginx_upstream_host }}:{{ nginx_upstream_port }};
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**tasks/main.yml**
```yaml
- name: Cargamos modulo de instalacion
  ansible.builtin.include_tasks: install.yml
```

**tasks/install.yml**
```yaml
- name: Instalar Nginx
  package:
    name: nginx
    state: present

- name: Copiar config reverse proxy
  template:
    src: reverse-proxy.conf.j2
    dest: /etc/nginx/conf.d/reverse-proxy.conf
  notify: "Recargar Nginx"

- name: Asegurar Nginx activo
  service:
    name: nginx
    enabled: yes
    state: started
```

**handlers/main.yml**

```yaml
- name: Recargar Nginx
  service:
    name: nginx
    state: reloaded
```

---

## 📘 **Playbook principal**

Encargado de orquestar la ejecución de los roles

**webservers.yml**
```yaml
---
- hosts: webservers
  gather_facts: false
  become: yes
  roles:
    - role: apache
    - role: nginx
```

Puntos clave:

- Cómo **un rol depende de la salida del otro** (`apache_port` → reverse proxy '`nginx_upstream_port`')
- Cómo **pasar variables al rol** correctamente (su scope es a nivel de play)
- Cómo manejar **handlers independientes**
- Cómo separar responsabilidades: **Apache** sirve contenido, **Nginx** lo expone

---

## 📚 **Ejercicio 1 — Cambiar el puerto de Apache**

Cambiar el puerto por defecto de Apache:
```yaml
apache_port: 9090
```
→ Comprobar que Nginx lo respeta automáticamente. Modificar 

---

## 📚 **Ejercicio 2 — Añadir una página HTML desde template**

Añadir en el rol Apache:

```
templates/index.html.j2
tasks/main.yml → copiar plantilla
```

---

## 📚 **Ejercicio 3 — Añadir health-check en Nginx**

Añadir en la plantilla:

```
location /health {
  return 200 "OK\n";
}
```
