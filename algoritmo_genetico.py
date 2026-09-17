"""Algoritmo genetico para la seleccion optima de proyectos.

Taller Corte 2 - Introduccion a la Inteligencia Artificial.

El problema corresponde a una variante del problema de la mochila
0/1: seleccionar el subconjunto de proyectos de innovacion que
maximiza el beneficio total sin superar el presupuesto disponible.
"""

import random
import time

random.seed(42)

# ---------------------------------------------------------------
# Datos del problema
# ---------------------------------------------------------------
PROYECTOS = ["P1", "P2", "P3", "P4", "P5",
             "P6", "P7", "P8", "P9", "P10"]
COSTOS = [12, 7, 11, 8, 9, 14, 6, 10, 5, 13]
BENEFICIOS = [24, 13, 23, 15, 16, 28, 11, 19, 9, 25]
PRESUPUESTO = 50
NUM_GENES = len(PROYECTOS)


# ---------------------------------------------------------------
# Representacion e inicializacion de la poblacion
# ---------------------------------------------------------------
def generar_individuo():
    """Genera un cromosoma binario aleatorio de longitud 10."""
    return [random.randint(0, 1) for _ in range(NUM_GENES)]


def generar_poblacion(tamano):
    """Genera una poblacion inicial de ``tamano`` individuos."""
    return [generar_individuo() for _ in range(tamano)]


# ---------------------------------------------------------------
# Evaluacion de individuos
# ---------------------------------------------------------------
def calcular_costo(individuo):
    """Calcula el costo total C(X) de un individuo."""
    return sum(c * x for c, x in zip(COSTOS, individuo))


def calcular_beneficio(individuo):
    """Calcula el beneficio total B(X) de un individuo."""
    return sum(b * x for b, x in zip(BENEFICIOS, individuo))


def calcular_aptitud(individuo, lam=5):
    """Calcula la aptitud de un individuo con penalizacion lineal.

    Si el costo no supera el presupuesto, la aptitud es igual al
    beneficio. En caso contrario, se penaliza el exceso de costo
    multiplicandolo por el factor ``lam``.
    """
    costo = calcular_costo(individuo)
    beneficio = calcular_beneficio(individuo)
    if costo <= PRESUPUESTO:
        return beneficio
    return beneficio - lam * (costo - PRESUPUESTO)


def es_valido(individuo):
    """Indica si un individuo respeta la restriccion de presupuesto."""
    return calcular_costo(individuo) <= PRESUPUESTO


def proyectos_seleccionados(individuo):
    """Devuelve los nombres de los proyectos activos en el cromosoma."""
    return [p for p, x in zip(PROYECTOS, individuo) if x == 1]


def describir_individuo(individuo, lam=5):
    """Construye un diccionario con la informacion de un individuo,
    util para mostrar tablas de la poblacion (Punto 2)."""
    return {
        "cromosoma": "".join(str(g) for g in individuo),
        "proyectos": proyectos_seleccionados(individuo),
        "costo": calcular_costo(individuo),
        "beneficio": calcular_beneficio(individuo),
        "aptitud": calcular_aptitud(individuo, lam),
        "valido": es_valido(individuo),
    }


# ---------------------------------------------------------------
# Operadores geneticos
# ---------------------------------------------------------------
def seleccionar_padre(poblacion, aptitudes, tam_torneo=3):
    """Selecciona un padre mediante seleccion por torneo.

    Se eligen ``tam_torneo`` individuos al azar y se retorna aquel
    con mayor aptitud entre los participantes del torneo.
    """
    participantes = random.sample(range(len(poblacion)), tam_torneo)
    mejor = max(participantes, key=lambda i: aptitudes[i])
    return poblacion[mejor]


def cruzar(padre1, padre2, prob_cruce=0.8):
    """Aplica cruce de un punto entre dos padres.

    Con probabilidad ``prob_cruce`` se selecciona una posicion de
    corte al azar y se intercambian los segmentos finales de ambos
    padres. Si no ocurre cruce, los hijos son copias de los padres.
    """
    if random.random() > prob_cruce:
        return padre1[:], padre2[:]
    punto = random.randint(1, NUM_GENES - 1)
    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]
    return hijo1, hijo2


def mutar(individuo, pm=0.05):
    """Aplica mutacion binaria: cada gen cambia con probabilidad pm."""
    return [1 - gen if random.random() < pm else gen
            for gen in individuo]


# ---------------------------------------------------------------
# Algoritmo genetico completo (Punto 4)
# ---------------------------------------------------------------
def ejecutar_algoritmo_genetico(
        tamano_poblacion=20,
        num_generaciones=100,
        prob_cruce=0.8,
        prob_mutacion=0.05,
        tam_torneo=3,
        num_elite=1,
        lam=5,
        verbose=False):
    """Ejecuta el algoritmo genetico completo.

    Devuelve un diccionario con el mejor individuo encontrado, sus
    metricas y el historial generacion a generacion (mejor aptitud,
    aptitud promedio, beneficio y costo de la mejor solucion).
    """
    poblacion = generar_poblacion(tamano_poblacion)
    historial = []
    mejor_individuo_global = None
    mejor_aptitud_global = float("-inf")
    generacion_mejor = 0

    inicio = time.time()

    for generacion in range(num_generaciones):
        aptitudes = [calcular_aptitud(ind, lam) for ind in poblacion]

        indice_mejor = max(
            range(tamano_poblacion), key=lambda i: aptitudes[i])
        mejor_aptitud_gen = aptitudes[indice_mejor]
        mejor_individuo_gen = poblacion[indice_mejor]
        aptitud_promedio = sum(aptitudes) / tamano_poblacion

        if mejor_aptitud_gen > mejor_aptitud_global:
            mejor_aptitud_global = mejor_aptitud_gen
            mejor_individuo_global = mejor_individuo_gen[:]
            generacion_mejor = generacion

        historial.append({
            "generacion": generacion,
            "mejor_aptitud": mejor_aptitud_gen,
            "aptitud_promedio": aptitud_promedio,
            "mejor_beneficio": calcular_beneficio(mejor_individuo_gen),
            "mejor_costo": calcular_costo(mejor_individuo_gen),
            "mejor_cromosoma": mejor_individuo_gen[:],
        })

        if verbose:
            print(
                f"Gen {generacion:3d} | "
                f"Aptitud: {mejor_aptitud_gen:6.2f} | "
                f"Beneficio: {calcular_beneficio(mejor_individuo_gen):3d} "
                f"| Costo: {calcular_costo(mejor_individuo_gen):3d} | "
                f"Promedio: {aptitud_promedio:6.2f}"
            )

        # Elitismo: se conservan los mejores individuos sin cambios
        indices_ordenados = sorted(
            range(tamano_poblacion),
            key=lambda i: aptitudes[i],
            reverse=True,
        )
        elite = [poblacion[i][:] for i in indices_ordenados[:num_elite]]

        nueva_poblacion = elite[:]
        while len(nueva_poblacion) < tamano_poblacion:
            padre1 = seleccionar_padre(poblacion, aptitudes, tam_torneo)
            padre2 = seleccionar_padre(poblacion, aptitudes, tam_torneo)
            hijo1, hijo2 = cruzar(padre1, padre2, prob_cruce)
            hijo1 = mutar(hijo1, prob_mutacion)
            hijo2 = mutar(hijo2, prob_mutacion)
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < tamano_poblacion:
                nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion

    tiempo_ejecucion = time.time() - inicio

    return {
        "mejor_individuo": mejor_individuo_global,
        "mejor_aptitud": mejor_aptitud_global,
        "mejor_beneficio": calcular_beneficio(mejor_individuo_global),
        "mejor_costo": calcular_costo(mejor_individuo_global),
        "proyectos": proyectos_seleccionados(mejor_individuo_global),
        "generacion_mejor": generacion_mejor,
        "tiempo_ejecucion": tiempo_ejecucion,
        "aptitud_promedio_final": historial[-1]["aptitud_promedio"],
        "historial": historial,
    }


if __name__ == "__main__":
    resultado = ejecutar_algoritmo_genetico(verbose=True)
    print("\nMejor solucion encontrada:")
    print("Cromosoma:", resultado["mejor_individuo"])
    print("Proyectos:", resultado["proyectos"])
    print("Beneficio:", resultado["mejor_beneficio"])
    print("Costo:", resultado["mejor_costo"])
    print("Generacion en la que aparecio:", resultado["generacion_mejor"])
    print(f"Tiempo de ejecucion: {resultado['tiempo_ejecucion']:.4f} s")
