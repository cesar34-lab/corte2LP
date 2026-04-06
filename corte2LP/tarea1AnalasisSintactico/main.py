# main.py
# Punto de entrada del analizador sintactico.
#
# Uso:
#   python main.py gramatica.txt
#
# La cadena SIEMPRE se escribe como texto crudo en el archivo:
#   cadena_raw: holaComoEstas = 2 + 3
#
# La salida se guarda en salida.txt.

import sys
from lector_gramatica import leer_archivo, obtener_terminales
from parser_ll1 import (
    calcular_primero,
    calcular_siguiente,
    construir_tabla,
    analizar,
)
from ast_nodo import imprimir_arbol, arbol_a_texto


def cadena_generada(nodo):
    """
    Recorre el AST y reconstruye la lista de terminales que genera
    (las hojas del arbol, excluyendo epsilon).
    """
    if nodo.es_hoja():
        return [nodo.simbolo] if nodo.simbolo != "eps" else []
    tokens = []
    for hijo in nodo.hijos:
        tokens.extend(cadena_generada(hijo))
    return tokens


def main():
    # ── 1. Leer el archivo de entrada ────────────────────────────────────────
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo_gramatica.txt>")
        sys.exit(1)

    ruta_archivo = sys.argv[1]

    try:
        producciones, simbolo_inicial, cadena, cadena_raw = leer_archivo(ruta_archivo)
    except FileNotFoundError:
        print(f"Error: no se encontro el archivo '{ruta_archivo}'")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not producciones:
        print("Error: el archivo no contiene ninguna produccion.")
        sys.exit(1)

    terminales, no_terminales = obtener_terminales(producciones, simbolo_inicial)

    print("=" * 60)
    print("GRAMATICA LEIDA")
    print("=" * 60)
    print(f"Simbolo inicial : {simbolo_inicial}")
    print(f"No-terminales   : {sorted(no_terminales)}")
    print(f"Terminales      : {sorted(terminales)}")
    print("\nProducciones:")
    for nt, cuerpos in producciones.items():
        for cuerpo in cuerpos:
            print(f"  {nt} -> {' '.join(cuerpo)}")

    print(f"\nTexto original   : {cadena_raw}")
    print(f"Tokens generados : {' '.join(cadena)}")

    # ── 2. Calcular PRIMERO y SIGUIENTE ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("CONJUNTOS PRIMERO y SIGUIENTE")
    print("=" * 60)

    primero   = calcular_primero(producciones, terminales, no_terminales)
    siguiente = calcular_siguiente(producciones, no_terminales, simbolo_inicial, primero)

    for nt in sorted(no_terminales):
        print(f"  PRIMERO({nt:12}) = {sorted(primero[nt])}")
    print()
    for nt in sorted(no_terminales):
        print(f"  SIGUIENTE({nt:12}) = {sorted(siguiente[nt])}")

    # ── 3. Construir la tabla LL(1) ───────────────────────────────────────────
    print("\n" + "=" * 60)
    print("TABLA DE ANALISIS LL(1)")
    print("=" * 60)

    try:
        tabla = construir_tabla(producciones, no_terminales, terminales, primero, siguiente)
    except ValueError as e:
        print(f"\n{e}")
        print("No es posible construir un analizador LL(1) para esta gramatica.")
        sys.exit(1)

    for (nt, terminal), produccion in sorted(tabla.items()):
        print(f"  M[{nt}, {terminal}] = {nt} -> {' '.join(produccion)}")

    # ── 4. Analizar la cadena y construir el AST ──────────────────────────────
    print("\n" + "=" * 60)
    print("ANALISIS SINTACTICO")
    print("=" * 60)

    try:
        raiz = analizar(cadena, simbolo_inicial, tabla, no_terminales)
    except SyntaxError as e:
        print(f"\n{e}")
        sys.exit(1)

    # ── 5. Mostrar resultados ─────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("ARBOL DE SINTAXIS ABSTRACTA (AST)")
    print("=" * 60)
    imprimir_arbol(raiz)

    tokens_generados = cadena_generada(raiz)
    cadena_reconstruida = " ".join(tokens_generados)

    print("\n" + "=" * 60)
    print("CADENA GENERADA POR EL ARBOL")
    print("=" * 60)
    print(cadena_reconstruida)

    # ── 6. Guardar la salida ──────────────────────────────────────────────────
    ruta_salida = "salida.txt"
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(f"Texto original   : {cadena_raw}\n")
        f.write(f"Tokens generados : {' '.join(cadena)}\n\n")
        f.write("ARBOL DE SINTAXIS ABSTRACTA (AST)\n")
        f.write("=" * 60 + "\n")
        f.write(arbol_a_texto(raiz) + "\n\n")
        f.write("CADENA GENERADA POR EL ARBOL\n")
        f.write("=" * 60 + "\n")
        f.write(cadena_reconstruida + "\n")

    print(f"\nResultados guardados en '{ruta_salida}'")
    print("=" * 60)


if __name__ == "__main__":
    main()
