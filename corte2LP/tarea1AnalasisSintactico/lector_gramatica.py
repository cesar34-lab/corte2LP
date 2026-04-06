# lector_gramatica.py
# Lee el archivo .txt con la gramatica y la cadena de entrada.
#
# La cadena SIEMPRE se escribe como texto crudo:
#   cadena_raw: holaComoEstas = 2 + 3
#
# Opcionalmente se puede definir una seccion [lexer] con reglas personalizadas:
#   [lexer]
#   NOMBRE_TOKEN : patron_regex

from lexer import tokenizar, leer_reglas_lexer


def leer_archivo(ruta):
    """
    Lee el archivo de gramatica y retorna:
        - producciones:    dict { no_terminal -> [ [simbolo, ...], ... ] }
        - simbolo_inicial: str  (no-terminal de la primera produccion)
        - cadena:          list [ token, token, ... ]  (resultado del lexer)
        - cadena_raw:      str  con el texto original escrito en el archivo
    """
    producciones = {}
    simbolo_inicial = None
    cadena_raw = None

    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    # Extraer reglas del lexer si existen en el archivo
    reglas_lexer = leer_reglas_lexer(lineas)

    dentro_lexer = False

    for linea in lineas:
        linea_limpia = linea.strip()

        if not linea_limpia or linea_limpia.startswith("#"):
            continue

        if linea_limpia == "[lexer]":
            dentro_lexer = True
            continue

        if dentro_lexer:
            es_produccion = "->" in linea_limpia
            es_cadena     = linea_limpia.startswith("cadena_raw:")
            es_seccion    = linea_limpia.startswith("[")
            if es_produccion or es_cadena or es_seccion:
                dentro_lexer = False
            else:
                continue

        if linea_limpia.startswith("cadena_raw:"):
            cadena_raw = linea_limpia[len("cadena_raw:"):].strip()
            continue

        if "->" in linea_limpia:
            izquierda, derecha = linea_limpia.split("->", maxsplit=1)
            no_terminal = izquierda.strip()

            if simbolo_inicial is None:
                simbolo_inicial = no_terminal

            alternativas = derecha.split("|")
            cuerpos = []
            for alternativa in alternativas:
                cuerpo = alternativa.strip().split()
                if cuerpo:
                    cuerpos.append(cuerpo)

            if no_terminal not in producciones:
                producciones[no_terminal] = []
            producciones[no_terminal].extend(cuerpos)

    if cadena_raw is None:
        raise ValueError(
            "El archivo no contiene 'cadena_raw:'. "
            "La cadena debe escribirse como texto: cadena_raw: 2 + 3 * x"
        )

    cadena = tokenizar(cadena_raw, reglas_lexer)
    return producciones, simbolo_inicial, cadena, cadena_raw


def obtener_terminales(producciones, simbolo_inicial):
    """
    Clasifica los simbolos en terminales y no-terminales.
    Un simbolo es terminal si nunca aparece como cabeza de una produccion.
    """
    no_terminales = set(producciones.keys())
    terminales = set()

    for cuerpos in producciones.values():
        for cuerpo in cuerpos:
            for simbolo in cuerpo:
                if simbolo not in no_terminales:
                    terminales.add(simbolo)

    return terminales, no_terminales
