# Ansible101

**Proyecto para iniciar a profesionales en el apasionante mundo de Ansible de forma práctica y dinámica.**

Este repositorio contiene:

- Material didáctico estructurado por módulos
- Laboratorio práctico ejecutable localmente
- Roles de ejemplo para aprender buenas prácticas en Ansible.
- Ejercicios que cubren desde variables hasta servidores web y bases de datos.

El curso comienza totalmente desde cero y utiliza un laboratorio local para practicar


## 🌐 Accede a la documentación completa

Toda la explicación detallada, ejemplos y guías paso a paso están disponibles en la **página del curso**:

👉 [Ver documentación completa](https://tu_usuario.github.io/Ansible101/)

> Sigue el enlace para empezar a aprender con el laboratorio interactivo.


## 🚀 Contenido

1. **Tema 1:** Introducción a Ansible
2. **Tema 2:** Fundamentos de Ansible  
3. **Tema 3:** Prioridad de variables en Ansible
4. **Tema 4:** Manejo de Tareas, Roles y Handlers  
5. **Tema 5:** Templates y Jinja2 en Ansible  
6. **Tema 6:** Configuración de Servidores Web con Apache / Nginx
7. **Tema 7:** Gestión de Bases de Datos con PostgreSQL
8. **Tema 8:** Proyecto final: Automatización Completa de una Aplicación Web

## 💻 Laboratorio Local

El proyecto incluye un CLI levantar un laboratorio de pruebas:
```shell
# Iniciar laboratorio
lab init

# Ejecutar ejercicios
lab start <nombre_ejercicio>

# Evaluar tu progreso
lab grade <nombre_ejercicio>
```

## 📦 Instalación / Uso

Para usuarios que solo quieran probar el proyecto:

- Descargar la última versión del binario
- Agregar al PATH el directorio donde hemos movido el binario lab

```shell
export PATH=$(pwd):$PATH
lab --help
```

> Para desarrolladores que quieran modificar o compilar desde el código fuente, revisar [DEVELOPMENT.md](DEVELOPMENT.md).

## 📚 Recursos

- [Documentación oficial de Ansible](https://docs.ansible.com/)
- [Guía de buenas prácticas de roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)

## 📝 [LICENSE](./LICENSE)

GNU GENERAL PUBLIC LICENSE Version 3
