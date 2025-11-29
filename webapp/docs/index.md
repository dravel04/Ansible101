# Bienvenido a Ansible101 Lab

## Requisitos

!!! info
    Actualmente **SOLO** se sorpota en Linux y en Windows con WSL

Es necesario instalar Podman: [https://podman.io/docs/installation#installing-on-linux](https://podman.io/docs/installation#installing-on-linux)


## Habilitar el socket API de Podman

Verificar que el socket existe:

```bash
ls -l /run/user/$UID/podman/podman.sock
```

Si aparece, la API está habilitada.

Si no existe, ejecuta:

```bash
systemctl --user enable --now podman.socket
```

Esto crea el socket:

```
/run/user/$UID/podman/podman.sock
```

Comprueba que está activo:

```bash
systemctl --user status podman.socket
```

Debes ver algo como:

```
Active: active (listening)
```

Verificar que el socket existe:

```bash
ls -l /run/user/$UID/podman/podman.sock
```

Si aparece, la API está habilitada.

## Comandos

- `lab [OPTIONS] COMMAND [ARGS]...  ` - Comando para interactuar con el laboratorio
```
--install-completion       Install completion for the current shell.                                                          │
--show-completion          Show completion for the current shell, to copy it or customize the installation.                   │
--help                -h   Show this message and exit.       

init     Inicia el laboratorio y sus dependencias
start    Inicia las dependencias del ejercicio correspondiente
grade    Evalua el ejercicio correspondiente
finish   Libera las dependencias del ejercicio correspondiente
```