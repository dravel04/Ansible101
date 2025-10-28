# Lab - CLI framework

```mermaid
flowchart TB
    %% Main CLI
    subgraph Main["main.py - CLI Entry"]
        CLI["Typer CLI - comandos: init, start, grade, finish"]
    end

    %% Core / Domain
    subgraph Core["Core Layer / Domain"]
        Entities["Entities - Lab, Exercise, Grader"]
        Ports["Ports / Protocols - LabPort, LabRepository, ExercisePort, GraderPort, ProgressNotifierPort, RegistryPort"]
    end

    %% Application / Use Cases
    subgraph App["Application Layer / Use Cases"]
        LabInit["LabInitializer - inicializa lab y ejecuta adapters"]
        ExerciseUC["Exercise Use Cases - ExerciseA, ExerciseC, ..."]
        GraderUC["Grader Use Cases - GraderA, GraderC, ..."]
    end

    %% Infrastructure / Adapters
    subgraph Infra["Infrastructure Layer / Adapters"]
        LabAdapter["LabAdapter -> implementa LabPort"]
        RepoAdapter["LabRepositoryAdapter -> implementa LabRepository"]
        RegistryAdapter["RegistryAdapter -> implementa RegistryPort"]
        ContainerAdapter["ContainerAdapter -> implementa ContainerPort"]
        UIHelpers["ProgressNotifierAdapter -> implementa ProgressNotifierPort"]
    end

    %% External Tools
    subgraph External["External Tools / Libs"]
        Rich["Rich (Spinner, Text, Console)"]
        Logging["Python Logging / RichHandler"]
    end

    %% Relaciones
    CLI --> LabInit
    CLI --> ExerciseUC
    CLI --> GraderUC

    LabInit --> LabAdapter
    LabInit --> RepoAdapter
    LabInit --> Entities
    LabInit --> UIHelpers

    ExerciseUC --> Entities
    ExerciseUC --> Ports
    ExerciseUC --> ContainerAdapter

    GraderUC --> Entities
    GraderUC --> Ports

    ContainerAdapter --> External
    UIHelpers --> External

```

---

- **main.py / CLI Entry**
  + Solo coordina la ejecución, invoca servicios o entidades según el comando.

- **Core Layer**
  + `Entities`: clases puras del dominio (`Exercise`, `Grader`).
  + `Services`: opcional, orquesta operaciones complejas sobre las entidades.

- **Infrastructure / Adapters**
  + `exercise_*` y `grader_*`: implementaciones concretas de cada ejercicio y grader.
  + `console_utils.py`: helpers de UI (spinners, logging).

- **External Tools**
  + Librerías externas usadas por infrastructure y main (Rich, logging).

### Mejoras
- En modo DEBUG, si varios mensajes tienen el mismo timestamp, agruparlos:
```python
prefix = Text(" " * len(f"[{datetime.now().strftime("%m/%d/%y %H:%M:%S")}]"), style="default")
instance.debug_msg.append(
  Text.assemble(
    prefix,
    (" DEBUG    ", "green"),
    (msg, "default"),
  )
)
```

