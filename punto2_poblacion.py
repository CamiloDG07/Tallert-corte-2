"""Punto 2 - Poblacion inicial y funcion de aptitud.

Genera una poblacion inicial de N = 20 individuos y muestra, para
cada uno, el cromosoma, los proyectos seleccionados, el costo, el
beneficio, el valor de aptitud y si la solucion es valida.
"""

from algoritmo_genetico import generar_poblacion, describir_individuo

if __name__ == "__main__":
    poblacion = generar_poblacion(20)

    encabezado = (
        f"{'Ind.':<5}{'Cromosoma':<13}{'Proyectos':<28}"
        f"{'Costo':>7}{'Beneficio':>11}{'Aptitud':>10}{'Valido':>9}"
    )
    print(encabezado)
    print("-" * len(encabezado))

    for i, individuo in enumerate(poblacion, start=1):
        info = describir_individuo(individuo)
        proyectos_str = ", ".join(info["proyectos"]) or "(ninguno)"
        print(
            f"{i:<5}{info['cromosoma']:<13}{proyectos_str:<28}"
            f"{info['costo']:>7}{info['beneficio']:>11}"
            f"{info['aptitud']:>10.1f}{str(info['valido']):>9}"
        )
