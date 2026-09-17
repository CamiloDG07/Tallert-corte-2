# Taller: Diseño e implementación de un algoritmo genético

Introducción a la Inteligencia Artificial — Corte 2

## Descripción

Implementación de un algoritmo genético para resolver el problema
de **selección óptima de proyectos**: elegir el subconjunto de 10
proyectos de innovación que maximiza el beneficio total sin superar
un presupuesto de 50 unidades monetarias. El problema corresponde a
una variante del problema de la mochila 0/1.

## Requisitos

- Python 3.10 o superior
- `matplotlib`

Instalación de dependencias:

```bash
pip install matplotlib
```

## Estructura del proyecto

```
Taller-corte-2/
├── algoritmo_genetico.py     # Modulo principal: representacion,
│                              # poblacion, aptitud, operadores
│                              # geneticos y algoritmo completo
├── punto2_poblacion.py       # Punto 2: poblacion inicial y tabla
│                              # de aptitud
├── punto3_manual.py          # Punto 3: ejemplo manual de
│                              # seleccion, cruce y mutacion
├── experimentos.py           # Puntos 4 y 5: ejecuciones repetidas
│                              # y experimentos A, B, C
├── resultados/                # Graficas y tablas CSV generadas
├── informe/                   # Informe en PDF (formulacion,
│                              # diseno, resultados y conclusiones)
└── README.md
```

## Ejecución

Ejecutar el algoritmo genético con la configuración inicial
(N = 20, 100 generaciones, `pc` = 0.80, `pm` = 0.05):

```bash
python algoritmo_genetico.py
```

Mostrar la población inicial y la tabla de aptitud (Punto 2):

```bash
python punto2_poblacion.py
```

Mostrar el ejemplo manual de selección, cruce y mutación
(Punto 3):

```bash
python punto3_manual.py
```

Ejecutar las cinco corridas con la configuración inicial y los
experimentos A, B y C (Punto 4 y Punto 5). Genera las tablas CSV y
las gráficas de convergencia en `resultados/`:

```bash
python experimentos.py
```

## Datos del problema

| Proyecto | Costo | Beneficio |
|----------|-------|-----------|
| P1       | 12    | 24        |
| P2       | 7     | 13        |
| P3       | 11    | 23        |
| P4       | 8     | 15        |
| P5       | 9     | 16        |
| P6       | 14    | 28        |
| P7       | 6     | 11        |
| P8       | 10    | 19        |
| P9       | 5     | 9         |
| P10      | 13    | 25        |

Presupuesto máximo: 50 unidades monetarias.

## Reproducibilidad

El script fija `random.seed(42)` al importar `algoritmo_genetico`,
de modo que la secuencia completa de ejecuciones (`experimentos.py`)
es reproducible de principio a fin, aunque cada corrida individual
dentro de esa secuencia produce resultados distintos, como
corresponde a un algoritmo estocástico.

## Autores

Mario Jiménez, Juan David Andrade, Camilo Díaz — Introducción a la
Inteligencia Artificial.
