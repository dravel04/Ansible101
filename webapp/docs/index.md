# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.


## Habilitar el socket API de Podman

Ejecuta:

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