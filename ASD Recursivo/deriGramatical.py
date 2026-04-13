"""
Parser LL(1): FIRST, FOLLOW y tabla de prediccion
Uso: python3 deriGramatical.py gramatica.txt

Formato gramatica.txt:
    S -> A B | c
    A -> a | epsilon
    B -> b
"""

import sys
from collections import defaultdict

EPSILON = "epsilon"


def leer_gramatica(ruta):
    producciones = defaultdict(list)
    no_terminales = []
    terminales = set()

    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or "->" not in linea:
                continue

            izq, der = linea.split("->", 1)
            izq = izq.strip()

            if izq not in producciones:
                no_terminales.append(izq)

            for alternativa in der.split("|"):
                simbolos = alternativa.strip().split()
                producciones[izq].append(simbolos)

    # detectar terminales
    for nt, alts in producciones.items():
        for alt in alts:
            for s in alt:
                if s not in producciones and s != EPSILON:
                    terminales.add(s)

    return producciones, no_terminales, sorted(terminales)


def calcular_first(producciones, no_terminales):
    first = defaultdict(set)

    # terminales: FIRST(a) = {a}
    todos = set()
    for alts in producciones.values():
        for alt in alts:
            todos.update(alt)
    for s in todos:
        if s not in producciones and s != EPSILON:
            first[s] = {s}

    cambia = True
    while cambia:
        cambia = False
        for nt, alts in producciones.items():
            for alt in alts:
                antes = len(first[nt])
                if alt == [EPSILON]:
                    first[nt].add(EPSILON)
                else:
                    for s in alt:
                        first[nt] |= (first[s] - {EPSILON})
                        if EPSILON not in first[s]:
                            break
                    else:
                        first[nt].add(EPSILON)
                if len(first[nt]) != antes:
                    cambia = True

    return first


def first_de_cadena(cadena, first):
    resultado = set()
    for s in cadena:
        resultado |= (first[s] - {EPSILON})
        if EPSILON not in first[s]:
            break
    else:
        resultado.add(EPSILON)
    return resultado


def calcular_follow(producciones, no_terminales, first):
    follow = defaultdict(set)
    inicio = no_terminales[0]
    follow[inicio].add("$")

    cambia = True
    while cambia:
        cambia = False
        for nt, alts in producciones.items():
            for alt in alts:
                for i, s in enumerate(alt):
                    if s not in producciones:
                        continue
                    antes = len(follow[s])
                    beta = alt[i + 1:]
                    if beta:
                        f_beta = first_de_cadena(beta, first)
                        follow[s] |= (f_beta - {EPSILON})
                        if EPSILON in f_beta:
                            follow[s] |= follow[nt]
                    else:
                        follow[s] |= follow[nt]
                    if len(follow[s]) != antes:
                        cambia = True

    return follow


def calcular_tabla(producciones, no_terminales, terminales, first, follow):
    tabla = defaultdict(dict)  # tabla[NT][terminal] = produccion
    errores = []

    for nt, alts in producciones.items():
        for alt in alts:
            f = first_de_cadena(alt, first)
            for t in f:
                if t != EPSILON:
                    if t in tabla[nt]:
                        errores.append(f"Conflicto en [{nt}, {t}]")
                    tabla[nt][t] = alt
            if EPSILON in f:
                for t in follow[nt]:
                    if t in tabla[nt]:
                        errores.append(f"Conflicto en [{nt}, {t}]")
                    tabla[nt][t] = alt

    return tabla, errores


def formatear_conjunto(s):
    return "{ " + ", ".join(sorted(s)) + " }"


def mostrar_salida(producciones, no_terminales, terminales, first, follow, tabla, errores):
    def p(s=""):
        print(s)

    p("=" * 60)
    p("GRAMATICA")
    p("=" * 60)
    for nt in no_terminales:
        for alt in producciones[nt]:
            p(f"  {nt} -> {' '.join(alt)}")

    p("\n" + "=" * 60)
    p("CONJUNTOS FIRST")
    p("=" * 60)
    for nt in no_terminales:
        p(f"  FIRST({nt}) = {formatear_conjunto(first[nt])}")

    p("\n" + "=" * 60)
    p("CONJUNTOS FOLLOW")
    p("=" * 60)
    for nt in no_terminales:
        p(f"  FOLLOW({nt}) = {formatear_conjunto(follow[nt])}")

    p("\n" + "=" * 60)
    p("TABLA DE PREDICCION (LL1)")
    p("=" * 60)

    cols = sorted(terminales) + ["$"]
    ancho_nt = max(len(nt) for nt in no_terminales) + 2
    ancho_col = 22

    encabezado = "NT".ljust(ancho_nt) + "".join(c.ljust(ancho_col) for c in cols)
    p(encabezado)
    p("-" * len(encabezado))

    for nt in no_terminales:
        fila = nt.ljust(ancho_nt)
        for col in cols:
            if col in tabla[nt]:
                celda = f"{nt} -> {' '.join(tabla[nt][col])}"
            else:
                celda = ""
            fila += celda.ljust(ancho_col)
        p(fila)

    if errores:
        p("\n" + "=" * 60)
        p("CONFLICTOS DETECTADOS (gramatica NO es LL1)")
        p("=" * 60)
        for e in errores:
            p(f"  {e}")
    else:
        p("\nGramatica es LL(1). Sin conflictos.")


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 deriGramatical.py <archivo_gramatica.txt>")
        sys.exit(1)

    entrada = sys.argv[1]

    producciones, no_terminales, terminales = leer_gramatica(entrada)
    first = calcular_first(producciones, no_terminales)
    follow = calcular_follow(producciones, no_terminales, first)
    tabla, errores = calcular_tabla(producciones, no_terminales, terminales, first, follow)
    mostrar_salida(producciones, no_terminales, terminales, first, follow, tabla, errores)


if __name__ == "__main__":
    main()
