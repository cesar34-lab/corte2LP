# parser_ll1.py
# Implementa un analizador sintactico LL(1) descendente predictivo.
# Construye la tabla de analisis y genera el AST durante el recorrido.

from ast_nodo import NodoAST

EPSILON = "eps"
FIN     = "$"


# ─────────────────────────────────────────────────────────────────────────────
# Calculo de PRIMERO y SIGUIENTE
# ─────────────────────────────────────────────────────────────────────────────

def calcular_primero(producciones, terminales, no_terminales):
    """
    Calcula PRIMERO para cada simbolo de la gramatica.
    PRIMERO(X) = terminales que pueden aparecer al inicio de alguna
                 cadena derivada desde X.
    """
    primero = {s: set() for s in no_terminales}
    for t in terminales:
        primero[t] = {t}
    primero[EPSILON] = {EPSILON}
    primero[FIN]     = {FIN}

    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for cabeza, cuerpos in producciones.items():
            for cuerpo in cuerpos:
                antes = len(primero[cabeza])
                todos_epsilon = True
                for simbolo in cuerpo:
                    primero[cabeza] |= (primero.get(simbolo, set()) - {EPSILON})
                    if EPSILON not in primero.get(simbolo, set()):
                        todos_epsilon = False
                        break
                if todos_epsilon:
                    primero[cabeza].add(EPSILON)
                if len(primero[cabeza]) != antes:
                    hubo_cambio = True

    return primero


def calcular_siguiente(producciones, no_terminales, simbolo_inicial, primero):
    """
    Calcula SIGUIENTE para cada no-terminal.
    SIGUIENTE(A) = terminales que pueden aparecer inmediatamente
                  a la derecha de A en alguna forma sentencial.
    """
    siguiente = {nt: set() for nt in no_terminales}
    siguiente[simbolo_inicial].add(FIN)

    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for cabeza, cuerpos in producciones.items():
            for cuerpo in cuerpos:
                for i, simbolo in enumerate(cuerpo):
                    if simbolo not in no_terminales:
                        continue
                    antes  = len(siguiente[simbolo])
                    resto  = cuerpo[i + 1:]
                    prim_r = primero_de_cadena(resto, primero)
                    siguiente[simbolo] |= (prim_r - {EPSILON})
                    if not resto or EPSILON in prim_r:
                        siguiente[simbolo] |= siguiente[cabeza]
                    if len(siguiente[simbolo]) != antes:
                        hubo_cambio = True

    return siguiente


def primero_de_cadena(cadena, primero):
    """Calcula PRIMERO para una secuencia de simbolos."""
    resultado = set()
    for simbolo in cadena:
        prim = primero.get(simbolo, set())
        resultado |= (prim - {EPSILON})
        if EPSILON not in prim:
            break
    else:
        resultado.add(EPSILON)
    return resultado


# ─────────────────────────────────────────────────────────────────────────────
# Construccion de la tabla LL(1)
# ─────────────────────────────────────────────────────────────────────────────

def construir_tabla(producciones, no_terminales, terminales, primero, siguiente):
    """
    Construye la tabla de analisis predictivo M[A, a].

    Reglas:
      1. Para cada terminal a en PRIMERO(alfa): agregar A->alfa a M[A, a]
      2. Si eps en PRIMERO(alfa): agregar A->alfa a M[A, b] para b en SIGUIENTE(A)
    """
    tabla = {}

    for cabeza, cuerpos in producciones.items():
        for cuerpo in cuerpos:
            primero_cuerpo = primero_de_cadena(cuerpo, primero)

            for terminal in primero_cuerpo - {EPSILON}:
                clave = (cabeza, terminal)
                if clave in tabla:
                    raise ValueError(
                        f"La gramatica no es LL(1): conflicto en M[{cabeza}, {terminal}]"
                    )
                tabla[clave] = cuerpo

            if EPSILON in primero_cuerpo:
                for terminal in siguiente[cabeza]:
                    clave = (cabeza, terminal)
                    if clave in tabla:
                        raise ValueError(
                            f"La gramatica no es LL(1): conflicto en M[{cabeza}, {terminal}]"
                        )
                    tabla[clave] = [EPSILON]

    return tabla


# ─────────────────────────────────────────────────────────────────────────────
# Analisis LL(1) y construccion del AST
# ─────────────────────────────────────────────────────────────────────────────

def analizar(cadena, simbolo_inicial, tabla, no_terminales):
    """
    Ejecuta el analisis LL(1) sobre la cadena y construye el AST.

    La pila contiene pares (simbolo, nodo) para construir el arbol
    a medida que se aplican las producciones.

    Retorna el nodo raiz del AST si la cadena es valida.
    Lanza SyntaxError si la cadena no pertenece al lenguaje.
    """
    tokens = cadena + [FIN]
    indice = 0

    raiz  = NodoAST(simbolo_inicial)
    pila  = [(simbolo_inicial, raiz)]

    while pila:
        tope_simbolo, tope_nodo = pila[-1]
        token_actual = tokens[indice]

        if tope_simbolo == FIN:
            if token_actual == FIN:
                break
            raise SyntaxError(
                f"Error: se esperaba fin de cadena pero se encontro '{token_actual}'"
            )

        elif tope_simbolo in no_terminales:
            clave = (tope_simbolo, token_actual)
            if clave not in tabla:
                raise SyntaxError(
                    f"Error sintactico: no hay produccion para [{tope_simbolo}, {token_actual}]"
                )
            produccion = tabla[clave]
            pila.pop()

            if produccion != [EPSILON]:
                hijos = [NodoAST(s) for s in produccion]
                tope_nodo.hijos = hijos
                for hijo in reversed(hijos):
                    pila.append((hijo.simbolo, hijo))
            else:
                tope_nodo.hijos = [NodoAST(EPSILON)]

        else:
            if tope_simbolo == token_actual:
                pila.pop()
                indice += 1
            else:
                raise SyntaxError(
                    f"Error sintactico: se esperaba '{tope_simbolo}' pero se encontro '{token_actual}'"
                )

    if indice < len(tokens) - 1:
        raise SyntaxError(f"Error: tokens sobrantes desde '{tokens[indice]}'")

    return raiz
