"""
Parser LL(1): FIRST, FOLLOW, tabla de prediccion, ASDR
Uso: python3 recursividad.py gramatica.txt
"""

import sys
from collections import defaultdict

EPSILON = "epsilon"
SEP     = "=" * 70


# ─────────────────────────── LECTURA ───────────────────────────

def leer_gramatica(ruta):
    producciones  = defaultdict(list)
    no_terminales = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or "->" not in linea:
                continue
            izq, der = linea.split("->", 1)
            izq = izq.strip()
            if izq not in producciones:
                no_terminales.append(izq)
            for alt in der.split("|"):
                producciones[izq].append(alt.strip().split())
    return producciones, no_terminales


def detectar_terminales(producciones):
    t = set()
    for alts in producciones.values():
        for alt in alts:
            for s in alt:
                if s not in producciones and s != EPSILON:
                    t.add(s)
    return sorted(t)


# ─────────────────── ELIMINACION RECURSION ─────────────────────

def nombre_prima(base, ocupados):
    prima = base + "'"
    while prima in ocupados:
        prima += "'"
    return prima


def tiene_rec_izq(producciones, nt_set):
    return any(
        alt and alt[0] == nt and alt != [EPSILON]
        for nt, alts in producciones.items() if nt in nt_set
        for alt in alts
    )


def tiene_rec_der(producciones, nt_set):
    return any(
        alt and alt[-1] == nt and alt != [EPSILON]
        for nt, alts in producciones.items() if nt in nt_set
        for alt in alts
    )


def eliminar_rec_izq(producciones, no_terminales):
    """A -> A a | b  =>  A -> b A' / A' -> a A' | epsilon"""
    nuevas   = defaultdict(list)
    nuevos   = list(no_terminales)
    ocupados = set(no_terminales)

    for nt in no_terminales:
        rec    = [a for a in producciones[nt] if a and a[0] == nt and a != [EPSILON]]
        no_rec = [a for a in producciones[nt] if not a or a[0] != nt or a == [EPSILON]]

        if not rec:
            nuevas[nt] = list(producciones[nt])
            continue

        prima = nombre_prima(nt, ocupados)
        ocupados.add(prima)
        nuevos.append(prima)

        # A -> b  queda A -> b A'
        for a in no_rec:
            nuevas[nt].append(a + [prima] if a != [EPSILON] else [EPSILON, prima])
        if not no_rec:
            nuevas[nt].append([prima])

        # A' -> a A' | epsilon
        for a in rec:
            nuevas[prima].append(a[1:] + [prima])
        nuevas[prima].append([EPSILON])

    return nuevas, nuevos


def eliminar_rec_der(producciones, no_terminales, nt_originales):
    """A -> a A | b  =>  A -> b A' / A' -> a A' | epsilon"""
    nuevas   = defaultdict(list)
    nuevos   = list(no_terminales)
    ocupados = set(no_terminales)

    for nt in no_terminales:
        if nt not in nt_originales:
            nuevas[nt] = list(producciones[nt])
            continue

        rec    = [a for a in producciones[nt] if a and a[-1] == nt and a != [EPSILON]]
        no_rec = [a for a in producciones[nt] if not a or a[-1] != nt or a == [EPSILON]]

        if not rec:
            nuevas[nt] = list(producciones[nt])
            continue

        prima = nombre_prima(nt, ocupados)
        ocupados.add(prima)
        nuevos.append(prima)

        for a in no_rec:
            nuevas[nt].append(a + [prima] if a != [EPSILON] else [EPSILON, prima])
        if not no_rec:
            nuevas[nt].append([prima])

        for a in rec:
            nuevas[prima].append(a[:-1] + [prima])
        nuevas[prima].append([EPSILON])

    return nuevas, nuevos


# ─────────────────── FIRST / FOLLOW / TABLA ────────────────────

def calcular_first(producciones):
    first = defaultdict(set)
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


def first_cadena(cadena, first):
    r = set()
    for s in cadena:
        r |= (first[s] - {EPSILON})
        if EPSILON not in first[s]:
            break
    else:
        r.add(EPSILON)
    return r


def calcular_follow(producciones, no_terminales, first):
    follow = defaultdict(set)
    follow[no_terminales[0]].add("$")

    cambia = True
    while cambia:
        cambia = False
        for nt, alts in producciones.items():
            for alt in alts:
                for i, s in enumerate(alt):
                    if s not in producciones:
                        continue
                    antes = len(follow[s])
                    beta  = alt[i + 1:]
                    fb    = first_cadena(beta, first) if beta else {EPSILON}
                    follow[s] |= (fb - {EPSILON})
                    if EPSILON in fb:
                        follow[s] |= follow[nt]
                    if len(follow[s]) != antes:
                        cambia = True
    return follow


def calcular_tabla(producciones, no_terminales, first, follow):
    tabla   = defaultdict(dict)
    errores = []
    for nt, alts in producciones.items():
        for alt in alts:
            f = first_cadena(alt, first)
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


# ──────────────────── CONTEO DE ARBOLES ────────────────────────

def contar_arboles(producciones, no_terminales, first):
    memo = {}

    def arboles_nt(nt, visitados=None):
        if visitados is None:
            visitados = set()
        if nt in memo:
            return memo[nt]
        if nt in visitados:
            return 1
        visitados = visitados | {nt}
        total = 0
        for alt in producciones.get(nt, []):
            if alt == [EPSILON]:
                total += 1
                continue
            prod_n = 1
            for s in alt:
                if s in producciones:
                    prod_n *= arboles_nt(s, visitados)
            total += prod_n
        memo[nt] = total
        return total

    return {nt: arboles_nt(nt) for nt in no_terminales}


# ──────────────────────────── ASDR ─────────────────────────────

def nt_a_fn(nt):
    return "parse_" + nt.replace("'", "_prima")


def generar_asdr(producciones, no_terminales, tabla, first):
    L  = []
    ap = L.append

    ap("# " + "─" * 54)
    ap("# ANALIZADOR SINTACTICO DESCENDENTE RECURSIVO (ASDR)")
    ap("# Generado automaticamente desde la gramatica LL(1)")
    ap("# " + "─" * 54)
    ap("")
    ap("tokens = []   # asignar lista de tokens antes de analizar()")
    ap("pos    = 0")
    ap("")
    ap("")
    ap("def token_actual():")
    ap('    return tokens[pos] if pos < len(tokens) else "$"')
    ap("")
    ap("")
    ap("def consumir(esperado):")
    ap("    global pos")
    ap("    if token_actual() == esperado:")
    ap("        pos += 1")
    ap("    else:")
    ap("        raise SyntaxError(")
    ap('            f"Error: esperaba \'{esperado}\'"')
    ap('            f" pero hay \'{token_actual()}\' en pos {pos}"')
    ap("        )")
    ap("")
    ap("")

    for nt in no_terminales:
        fn         = nt_a_fn(nt)
        alts_tabla = tabla.get(nt, {})
        ap(f"def {fn}():")

        if not alts_tabla:
            ap(f"    pass  # {nt} no tiene entradas en la tabla")
            ap("")
            continue

        grupos = defaultdict(list)
        for tok, prod in alts_tabla.items():
            if list(prod) != [EPSILON]:
                grupos[tuple(prod)].append(tok)

        puede_epsilon = EPSILON in first[nt]

        if not grupos:
            ap("    pass  # siempre deriva epsilon")
            ap("")
            continue

        primer_if = True
        for prod, toks in grupos.items():
            cond = " or ".join(f'token_actual() == "{t}"' for t in sorted(toks))
            kw   = "if" if primer_if else "elif"
            ap(f"    {kw} {cond}:")
            primer_if = False
            for s in prod:
                if s in producciones:
                    ap(f"        {nt_a_fn(s)}()")
                else:
                    ap(f'        consumir("{s}")')

        ap("    else:")
        if puede_epsilon:
            ap("        pass  # epsilon: derivacion vacia")
        else:
            ap("        raise SyntaxError(")
            ap(f'            f"Error en {nt}: token inesperado \'{{token_actual()}}\'"')
            ap("        )")
        ap("")

    inicio = no_terminales[0]
    ap("")
    ap("def analizar(entrada):")
    ap('    """entrada: lista de tokens, ej: ["dos", "tres"]"""')
    ap("    global tokens, pos")
    ap("    tokens = entrada")
    ap("    pos    = 0")
    ap(f"    {nt_a_fn(inicio)}()")
    ap('    if token_actual() != "$":')
    ap('        raise SyntaxError(f"Tokens sobrantes desde pos {pos}")')
    ap('    print("Cadena aceptada.")')

    return "\n".join(L)


# ─────────────────────────── SALIDA ────────────────────────────

def fmt_set(s):
    items = sorted(s)
    return "{ " + ", ".join(items) + " }" if items else "{  }"


def imprimir_seccion(titulo):
    print(SEP)
    print(titulo)
    print(SEP)


def imprimir_gramatica(producciones, no_terminales, titulo):
    imprimir_seccion(titulo)
    for nt in no_terminales:
        for alt in producciones[nt]:
            print(f"  {nt} -> {' '.join(alt)}")


def imprimir_tabla(no_terminales, terminales, tabla):
    imprimir_seccion("TABLA DE PREDICCION (LL1)")

    cols      = sorted(terminales) + ["$"]
    ancho_nt  = max(len(nt) for nt in no_terminales) + 2
    # ancho de columna: suficiente para la celda mas larga
    ancho_col = max(
        max(
            len(f"{nt} -> {' '.join(tabla[nt][col])}")
            for nt in no_terminales
            for col in cols
            if col in tabla[nt]
        ) + 2,
        max(len(c) for c in cols) + 4
    )

    # encabezado
    enc = "NT".ljust(ancho_nt)
    for c in cols:
        enc += c.center(ancho_col) + " "
    print(enc)
    print("─" * len(enc))

    for nt in no_terminales:
        fila = nt.ljust(ancho_nt)
        for col in cols:
            if col in tabla[nt]:
                celda = f"{nt} -> {' '.join(tabla[nt][col])}"
            else:
                celda = ""
            fila += celda.center(ancho_col) + " "
        print(fila)


def mostrar_todo(prod_orig, nt_orig, producciones, no_terminales,
                 terminales, first, follow, tabla, errores,
                 elim_izq, elim_der, arboles, codigo_asdr):
    p = print

    # ── Gramatica original
    imprimir_gramatica(prod_orig, nt_orig, "GRAMATICA ORIGINAL")

    # ── Advertencias de recursion
    if elim_izq:
        p("[!] Recursion izquierda detectada y eliminada")
    if elim_der:
        p("[!] Recursion derecha detectada y eliminada")

    # ── Gramatica transformada (solo si hubo cambio)
    if elim_izq or elim_der:
        imprimir_gramatica(producciones, no_terminales, "GRAMATICA TRANSFORMADA")

    # ── FIRST
    imprimir_seccion("CONJUNTOS FIRST")
    for nt in no_terminales:
        p(f"  FIRST({nt}) = {fmt_set(first[nt])}")

    # ── FOLLOW
    imprimir_seccion("CONJUNTOS FOLLOW")
    for nt in no_terminales:
        p(f"  FOLLOW({nt}) = {fmt_set(follow[nt])}")

    # ── Tabla
    imprimir_tabla(no_terminales, terminales, tabla)

    # ── Analisis LL(1)
    imprimir_seccion("ANALISIS LL(1)")
    if not errores:
        p("  La gramatica ES LL(1).")
    else:
        p("  La gramatica NO es LL(1).")
        p(f"  Conflictos encontrados: {len(errores)}")
        for e in errores:
            p(f"    {e}")

    # ── Arboles
    imprimir_seccion("ARBOLES DE DERIVACION POR NO TERMINAL")
    if arboles:
        for nt in no_terminales:
            n     = arboles[nt]
            marca = "  <- simbolo inicial" if nt == no_terminales[0] else ""
            p(f"  {nt}: {n} arbol(es) posible(s){marca}")
        p("")
        inicio = no_terminales[0]
        total  = arboles[inicio]
        p(f"  numero de arboles generados: {total}")
        p(f"  Gramatica es LL(1): {'si' if not errores else 'no'}")
        # LL(1) garantiza exactamente 1 arbol por cadena => no ambigua
        p("  Gramatica NO es ambigua (es LL(1))")
    else:
        p("  No se calculan arboles: gramatica no es LL(1).")

    # ── ASDR
    imprimir_seccion("ANALIZADOR SINTACTICO DESCENDENTE RECURSIVO (ASDR)")
    if codigo_asdr:
        p(codigo_asdr)
    else:
        p("  ASDR no generado: gramatica no es LL(1).")


# ──────────────────────────── MAIN ─────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 recursividad.py <gramatica.txt>")
        sys.exit(1)

    producciones, no_terminales = leer_gramatica(sys.argv[1])
    prod_orig   = defaultdict(list, {k: list(v) for k, v in producciones.items()})
    nt_orig     = list(no_terminales)
    nt_orig_set = set(nt_orig)

    elim_izq = tiene_rec_izq(producciones, nt_orig_set)
    elim_der = tiene_rec_der(producciones, nt_orig_set)

    if elim_izq:
        producciones, no_terminales = eliminar_rec_izq(producciones, no_terminales)
    if elim_der:
        producciones, no_terminales = eliminar_rec_der(producciones, no_terminales, nt_orig_set)

    terminales     = detectar_terminales(producciones)
    first          = calcular_first(producciones)
    follow         = calcular_follow(producciones, no_terminales, first)
    tabla, errores = calcular_tabla(producciones, no_terminales, first, follow)

    arboles     = contar_arboles(producciones, no_terminales, first) if not errores else {}
    codigo_asdr = generar_asdr(producciones, no_terminales, tabla, first) if not errores else ""

    mostrar_todo(prod_orig, nt_orig, producciones, no_terminales,
                 terminales, first, follow, tabla, errores,
                 elim_izq, elim_der, arboles, codigo_asdr)


if __name__ == "__main__":
    main()
