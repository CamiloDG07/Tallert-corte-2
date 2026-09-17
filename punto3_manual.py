"""Punto 3 - Ejemplo manual de seleccion, cruce y mutacion.

Se genera una poblacion inicial pequena, se seleccionan dos padres
mediante seleccion por torneo, se les aplica cruce de un punto y
mutacion binaria, y se registra cada paso del proceso.
"""

import random

from algoritmo_genetico import (
    calcular_aptitud,
    calcular_beneficio,
    calcular_costo,
    cruzar,
    generar_poblacion,
    mutar,
    seleccionar_padre,
)


def mostrar(etiqueta, individuo):
    cromosoma = "".join(str(g) for g in individuo)
    print(
        f"{etiqueta}: {cromosoma}  "
        f"(costo={calcular_costo(individuo)}, "
        f"beneficio={calcular_beneficio(individuo)}, "
        f"aptitud={calcular_aptitud(individuo):.1f})"
    )


if __name__ == "__main__":
    random.seed(2)

    poblacion = generar_poblacion(20)
    aptitudes = [calcular_aptitud(ind) for ind in poblacion]

    print("Poblacion inicial (para el ejemplo manual):")
    for i, ind in enumerate(poblacion, start=1):
        mostrar(f"  Ind. {i:2d}", ind)

    print("\nPaso 1: seleccion por torneo (tam_torneo = 3)")
    padre1 = seleccionar_padre(poblacion, aptitudes, tam_torneo=3)
    padre2 = seleccionar_padre(poblacion, aptitudes, tam_torneo=3)
    mostrar("  Padre 1", padre1)
    mostrar("  Padre 2", padre2)

    print("\nPaso 2: cruce de un punto")
    punto = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]
    print(f"  Punto de cruce: posicion {punto}")
    mostrar("  Hijo 1 (antes de mutar)", hijo1)
    mostrar("  Hijo 2 (antes de mutar)", hijo2)

    print("\nPaso 3: mutacion binaria (pm = 0.05)")
    hijo1_mutado = mutar(hijo1, pm=0.05)
    hijo2_mutado = mutar(hijo2, pm=0.05)
    genes_cambiados_1 = [
        i for i in range(len(hijo1))
        if hijo1[i] != hijo1_mutado[i]
    ]
    genes_cambiados_2 = [
        i for i in range(len(hijo2))
        if hijo2[i] != hijo2_mutado[i]
    ]
    mostrar("  Hijo 1 (despues de mutar)", hijo1_mutado)
    print(f"    Genes mutados (indices 0-9): {genes_cambiados_1}")
    mostrar("  Hijo 2 (despues de mutar)", hijo2_mutado)
    print(f"    Genes mutados (indices 0-9): {genes_cambiados_2}")
