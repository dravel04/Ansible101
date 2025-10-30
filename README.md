# Ansible101
Para mayor facilidad exportaremos nuestro paquete mediante `pip`.

## Compilar el programa
```shell
python -m nuitka \
  --standalone \
  --onefile \
  --static-libpython=no \
  --include-data-dir=lab/infrastructure/containerfiles=lab/infrastructure/containerfiles \
  lab/main.py \
  --output-filename=lab-cli
```


<details>
<summary><h2>Laboratorio - CLI</h2></summary>

### Estructura de carpeta
```
.
├── lab
│   ├── __init__.py
│   ├── grade
│   │   ├── __init__.py
│   │   ├── grade_functions.py
│   │   ├── grade.py
│   │   └── scripts
│   │       ├── __init__.py
│   │       ├── grade_error.py
│   │       ├── grade_ok.py
│   │       └── grade_rich.py
│   └── main.py
└── pyproject.toml
```


## Apuntes

### Live

Lo usas como un gestor de contexto (`with` Live(...) as live:):
- Cuando entras al bloque `with`: Rich "captura" la línea actual de la terminal. Cualquier cosa que live.console.print() (o console.print() si no estás usando live.console explícitamente dentro del Live para ese contenido específico) imprima dentro de ese bloque, se mostrará en el área "en vivo" y se actualizará.
- Dentro del bloque `with`: Puedes cambiar el contenido que se muestra en el área de Live simplemente volviendo a llamar a live.update() (aunque a menudo no es necesario, ya que console.print dentro del contexto de Live ya actualiza el contenido).
- Cuando sales del bloque `with`:
  + Si `transient=True` (como lo tenemos), el contenido de Live desaparece, dejando la terminal limpia como estaba antes de que Live se activara. Esto es ideal para barras de progreso o spinners que solo quieres ver mientras la tarea se ejecuta.
  + Si `transient=False` (por defecto), el contenido final de Live permanece en la terminal.



### Enlaces de interés
- [Libreria click](https://click.palletsprojects.com/en/8.1.x/)
- [click-completion](https://github.com/click-contrib/click-completion?tab=readme-ov-file)
- [Packaging Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
