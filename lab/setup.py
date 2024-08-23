from setuptools import setup, find_packages

setup(
    name='lab',
    version='1.0.0',
    # py_modules=['packages.lab'],
    packages=find_packages(),
    install_requires=[
        'Click',
        # 'click-completion',
    ],
    entry_points={
        'console_scripts': [
            'lab = packages.lab:cli',
        ],
    },
)

# name: Especifica el nombre del paquete. En este caso, el paquete se llama lab.
# version: Define la versión del paquete. Aquí, el paquete tiene la versión 1.0.0.
# py_modules: Una lista de módulos de Python que están incluidos en el paquete. En este caso, solo hay un módulo llamado lab.
# install_requires: Enumera las dependencias que debe instalar pip cuando se instala el paquete. En este ejemplo, el paquete requiere la biblioteca Click.
# entry_points: Define puntos de entrada para el paquete. En este caso, está utilizando la sección 'console_scripts', que es específica de la creación de scripts de consola.
# 'console_scripts': Indica que estás creando scripts de consola ejecutables.
# 'lab = packages.lab:cli': Define el nombre del script de consola (lab) y el punto de entrada al que apunta (packages.lab:cli). Esto significa que cuando ejecutas el script de consola lab, se llamará a la función cli en el módulo lab.