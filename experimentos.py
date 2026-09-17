"""Puntos 4 y 5 - Ejecucion repetida del algoritmo y experimentos.

Ejecuta la configuracion inicial cinco veces para evidenciar la
naturaleza estocastica del algoritmo, y luego corre los tres
experimentos (A, B, C) que varian el tamano de poblacion, el
numero de generaciones y la tasa de mutacion. Genera una tabla de
resultados en CSV y graficas de convergencia en la carpeta
``resultados``.
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from algoritmo_genetico import ejecutar_algoritmo_genetico  # noqa: E402

CARPETA_RESULTADOS = os.path.join(
    os.path.dirname(__file__), "resultados")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

CONFIG_BASE = {
    "tamano_poblacion": 20,
    "num_generaciones": 100,
    "prob_cruce": 0.80,
    "prob_mutacion": 0.05,
    "tam_torneo": 3,
    "num_elite": 1,
    "lam": 5,
}

EXPERIMENTOS = {
    "A": {"tamano_poblacion": 10, "num_generaciones": 50,
          "prob_mutacion": 0.01},
    "B": {"tamano_poblacion": 20, "num_generaciones": 100,
          "prob_mutacion": 0.05},
    "C": {"tamano_poblacion": 50, "num_generaciones": 200,
          "prob_mutacion": 0.10},
}


def graficar_convergencia(historial, titulo, archivo):
    """Grafica la mejor aptitud y la aptitud promedio por
    generacion y guarda la figura en ``resultados``."""
    generaciones = [h["generacion"] for h in historial]
    mejor = [h["mejor_aptitud"] for h in historial]
    promedio = [h["aptitud_promedio"] for h in historial]

    plt.figure(figsize=(7, 4.5))
    plt.plot(generaciones, mejor, label="Mejor aptitud")
    plt.plot(generaciones, promedio, label="Aptitud promedio",
             linestyle="--")
    plt.xlabel("Generacion")
    plt.ylabel("Aptitud")
    plt.title(titulo)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    ruta = os.path.join(CARPETA_RESULTADOS, archivo)
    plt.savefig(ruta, dpi=150)
    plt.close()
    return ruta


def ejecuciones_repetidas(num_ejecuciones=5):
    """Ejecuta la configuracion base varias veces (Punto 4) y
    devuelve la lista de resultados junto con el historial de la
    primera ejecucion, usado para la grafica de convergencia."""
    filas = []
    historial_referencia = None

    for i in range(1, num_ejecuciones + 1):
        resultado = ejecutar_algoritmo_genetico(**CONFIG_BASE)
        if historial_referencia is None:
            historial_referencia = resultado["historial"]
        filas.append({
            "ejecucion": i,
            "mejor_beneficio": resultado["mejor_beneficio"],
            "mejor_costo": resultado["mejor_costo"],
            "proyectos": ", ".join(resultado["proyectos"]),
            "generacion_mejor": resultado["generacion_mejor"],
            "tiempo_s": round(resultado["tiempo_ejecucion"], 5),
            "aptitud_promedio_final": round(
                resultado["aptitud_promedio_final"], 2),
        })

    return filas, historial_referencia


def correr_experimentos():
    """Ejecuta los experimentos A, B y C (Punto 5) y devuelve sus
    resultados junto con el historial de cada uno."""
    filas = []
    historiales = {}

    for nombre, cambios in EXPERIMENTOS.items():
        config = dict(CONFIG_BASE)
        config.update(cambios)
        resultado = ejecutar_algoritmo_genetico(**config)
        historiales[nombre] = resultado["historial"]
        filas.append({
            "experimento": nombre,
            "poblacion": config["tamano_poblacion"],
            "generaciones": config["num_generaciones"],
            "mutacion": config["prob_mutacion"],
            "mejor_beneficio": resultado["mejor_beneficio"],
            "mejor_costo": resultado["mejor_costo"],
            "proyectos": ", ".join(resultado["proyectos"]),
            "generacion_mejor": resultado["generacion_mejor"],
            "tiempo_s": round(resultado["tiempo_ejecucion"], 5),
            "aptitud_promedio_final": round(
                resultado["aptitud_promedio_final"], 2),
        })

    return filas, historiales


def guardar_csv(filas, campos, archivo):
    ruta = os.path.join(CARPETA_RESULTADOS, archivo)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)
    return ruta


def imprimir_tabla(filas, campos):
    ancho = {c: max(len(c), *(len(str(f[c])) for f in filas)) + 2
             for c in campos}
    encabezado = "".join(c.ljust(ancho[c]) for c in campos)
    print(encabezado)
    print("-" * len(encabezado))
    for fila in filas:
        print("".join(str(fila[c]).ljust(ancho[c]) for c in campos))


if __name__ == "__main__":
    print("=" * 70)
    print("Punto 4: cinco ejecuciones con la configuracion inicial")
    print("=" * 70)
    filas_base, historial_base = ejecuciones_repetidas(5)
    campos_base = ["ejecucion", "mejor_beneficio", "mejor_costo",
                   "proyectos", "generacion_mejor", "tiempo_s",
                   "aptitud_promedio_final"]
    imprimir_tabla(filas_base, campos_base)
    guardar_csv(filas_base, campos_base, "punto4_ejecuciones.csv")
    graficar_convergencia(
        historial_base,
        "Convergencia - configuracion base (ejecucion 1)",
        "convergencia_base.png",
    )

    print("\n" + "=" * 70)
    print("Punto 5: experimentos A, B y C")
    print("=" * 70)
    filas_exp, historiales_exp = correr_experimentos()
    campos_exp = ["experimento", "poblacion", "generaciones",
                  "mutacion", "mejor_beneficio", "mejor_costo",
                  "proyectos", "generacion_mejor", "tiempo_s",
                  "aptitud_promedio_final"]
    imprimir_tabla(filas_exp, campos_exp)
    guardar_csv(filas_exp, campos_exp, "punto5_experimentos.csv")

    for nombre, historial in historiales_exp.items():
        graficar_convergencia(
            historial,
            f"Convergencia - experimento {nombre}",
            f"convergencia_experimento_{nombre}.png",
        )

    # Grafica comparativa de la mejor aptitud entre experimentos
    plt.figure(figsize=(7, 4.5))
    for nombre, historial in historiales_exp.items():
        generaciones = [h["generacion"] for h in historial]
        mejor = [h["mejor_aptitud"] for h in historial]
        plt.plot(generaciones, mejor, label=f"Experimento {nombre}")
    plt.xlabel("Generacion")
    plt.ylabel("Mejor aptitud")
    plt.title("Comparacion de la mejor aptitud por experimento")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        os.path.join(CARPETA_RESULTADOS, "comparacion_experimentos.png"),
        dpi=150,
    )
    plt.close()

    print(f"\nResultados guardados en: {CARPETA_RESULTADOS}")
