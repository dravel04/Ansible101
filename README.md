# Ansible101
Para mayor facilidad exportaremos nuestro paquete mediante `pip`.


<details>
<summary><h2>Laboratorio - CLI</h2></summary>

### Estructura de carpeta
```
lab
├── packages
│   ├── __init__.py
│   ├── grade
│   │   ├── __init__.py
│   │   ├── grade.py
│   │   └── scripts
│   │       ├── __init__.py
│   │       ├── grade_error.py
│   │       └── grade_ok.py
│   └── lab.py
└── setup.py
```

### Creación de la interfaz CLI
- [lab.py](./lab/packages/lab.py)
    - Las triple comilla doble (`"""`) se utilizan en Python para definir cadenas de texto multilínea. En el contexto de las funciones de Click (la biblioteca que estás utilizando para la interfaz de línea de comandos), estas cadenas de texto multilínea se utilizan como documentación de ayuda para los comandos.
- [setup.py](./lab/setup.py)
    - `name`: Especifica el nombre del paquete. En este caso, el paquete se llama `lab`.
    - `version`: Define la versión del paquete. Aquí, el paquete tiene la versión `1.0.0`.
    - `py_modules`: Una lista de módulos de Python que están incluidos en el paquete. En este caso, solo hay un módulo llamado `lab`.
    - `install_requires`: Enumera las dependencias que debe instalar pip cuando se instala el paquete. En este ejemplo, el paquete requiere la biblioteca `Click`.
    - `entry_points`: Define puntos de entrada para el paquete. En este caso, está utilizando la sección `'console_scripts'`, que es específica de la creación de scripts de consola.
    - `console_scripts`: Indica que estás creando scripts de consola ejecutables.
    - `lab = lab:cli`: Define el nombre del script de consola (`lab`) y el punto de entrada al que apunta (`lab:cli`). Esto significa que cuando ejecutas el script de consola `lab`, se llamará a la función cli en el módulo `lab`.

### Entorno de pruebas
``` shell
# Creamos entorno virtual para pruebas
python3 -m venv pyenv # pyenv -> nombre del entorno a crear (puede ser una carpeta oculta .pyenv)
```
- `-m venv`: Utiliza el módulo venv que viene incluido en la biblioteca estándar de Python para crear un entorno virtual.
- `pyenv`: Especifica el nombre del directorio donde se creará el entorno virtual. En este caso, se ha elegido el nombre `pyenv`, pero puedes usar otro nombre si lo prefieres.
``` shell
. pyenv/bin/activate
```
- `.`: El primer punto (.) es un comando de la shell que se utiliza para ejecutar el script de activación. Este script se encuentra en el directorio `pyenv/bin/` y se llama `activate`.
- `pyenv/bin/activate`: Es la ruta al script de activación del entorno virtual. Cuando ejecutas este comando, activa el entorno virtual y configura tu sesión de shell para usar la versión de Python y las herramientas del entorno virtual.

```shell
# Instalamos nuestro paquete
pip install --editable . 
```

</details>



<details>
<summary><h2>Laboratorio - Web</h2></summary>

### Estructura de carpeta

</details>

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
