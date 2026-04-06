# lexer.py
# Convierte una cadena de texto cruda en una lista de tokens.
# Funciona igual que un lexer de ANTLR4: recorre la cadena caracter
# a caracter y aplica reglas en orden de prioridad.

import re

# Reglas predeterminadas disponibles sin necesidad de definir [lexer].
# El orden importa: las reglas mas especificas deben ir primero.
# Por ejemplo RELOP (<=, >=, ==) debe ir antes que EQUALS (=).
REGLAS_DEFAULT = [
    ("RELOP",      r'<=|>=|==|!=|<|>'),
    ("NUMBER",     r'\d+(\.\d+)?'),
    ("STRING",     r'"[^"]*"|\'[^\']*\''),
    ("ID",         r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("PLUS",       r'\+'),
    ("MINUS",      r'-'),
    ("TIMES",      r'\*'),
    ("DIVIDE",     r'/'),
    ("EQUALS",     r'='),
    ("LPAREN",     r'\('),
    ("RPAREN",     r'\)'),
    ("LBRACKET",   r'\['),
    ("RBRACKET",   r'\]'),
    ("LBRACE",     r'\{'),
    ("RBRACE",     r'\}'),
    ("SEMICOLON",  r';'),
    ("COMMA",      r','),
    ("DOT",        r'\.'),
    ("WHITESPACE", r'\s+'),
]


def tokenizar(cadena_cruda, reglas=None):
    """
    Convierte una cadena de texto en una lista de nombres de tokens.

    Parametros:
        cadena_cruda -- texto a tokenizar, ej: "holaComoEstas = 2 + 3"
        reglas       -- lista de tuplas (NOMBRE, patron_regex).
                        Si es None se usan las reglas predeterminadas.

    Retorna:
        lista de strings, ej: ["ID", "EQUALS", "NUMBER", "PLUS", "NUMBER"]

    Lanza:
        ValueError si encuentra un caracter que ninguna regla reconoce.
    """
    if reglas is None:
        reglas = REGLAS_DEFAULT

    # Compilamos todas las reglas en un solo patron con grupos nombrados.
    # Esto permite saber que regla coincidio usando match.lastgroup.
    patron_combinado = "|".join(
        f"(?P<{nombre}>{patron})" for nombre, patron in reglas
    )
    regex = re.compile(patron_combinado)

    tokens = []
    pos = 0

    while pos < len(cadena_cruda):
        match = regex.match(cadena_cruda, pos)

        if match is None:
            raise ValueError(
                f"Caracter no reconocido en posicion {pos}: '{cadena_cruda[pos]}'"
            )

        nombre_token = match.lastgroup

        # WHITESPACE se ignora (equivalente a -> skip en ANTLR4)
        if nombre_token != "WHITESPACE":
            tokens.append(nombre_token)

        pos = match.end()

    return tokens


def leer_reglas_lexer(lineas):
    """
    Extrae las reglas del lexer de la seccion [lexer] del archivo.

    Formato esperado:
        [lexer]
        NOMBRE_TOKEN : patron_regex

    Retorna lista de tuplas (NOMBRE, patron) o None si no hay seccion [lexer].
    """
    reglas = []
    dentro_seccion = False

    for linea in lineas:
        linea = linea.strip()

        if linea == "[lexer]":
            dentro_seccion = True
            continue

        if not dentro_seccion:
            continue

        # Salir de la seccion al encontrar otra seccion, una produccion o cadena
        if linea.startswith("[") or "->" in linea or linea.startswith("cadena"):
            break

        if not linea or linea.startswith("#"):
            continue

        if ":" in linea:
            nombre, patron = linea.split(":", maxsplit=1)
            reglas.append((nombre.strip(), patron.strip()))

    return reglas if reglas else None
