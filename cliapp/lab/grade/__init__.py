# Me permite exponer las funciones definidas en grade.py sin tener que poner el nombre del fichero
# Ejemplo: en mi estructura `lab/grade/grade.py` puedo importar `from lab.grade import grade_func` en
# lugar de tener que poner `from lab.grade.grade import grade_func`
from .grade import grade_func