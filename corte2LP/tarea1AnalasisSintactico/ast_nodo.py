# ast_nodo.py
# Define la estructura de un nodo del Arbol de Sintaxis Abstracta (AST).

class NodoAST:
    """
    Representa un nodo dentro del AST.

    Un nodo puede ser:
      - Nodo interno: representa una produccion gramatical aplicada.
                      Tiene un simbolo (no-terminal) e hijos.
      - Nodo hoja:   representa un token de la cadena de entrada.
                      Tiene un simbolo (terminal) y ningún hijo.
    """

    def __init__(self, simbolo, hijos=None):
        self.simbolo = simbolo
        self.hijos = hijos if hijos is not None else []

    def es_hoja(self):
        """Retorna True si el nodo no tiene hijos (es un terminal)."""
        return len(self.hijos) == 0

    def __repr__(self):
        return f"NodoAST({self.simbolo})"


def imprimir_arbol(nodo, prefijo="", es_ultimo=True):
    """
    Imprime el AST en consola con una representacion visual de arbol.
    """
    conector = "└── " if es_ultimo else "├── "
    print(prefijo + conector + nodo.simbolo)

    nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
    for i, hijo in enumerate(nodo.hijos):
        imprimir_arbol(hijo, nuevo_prefijo, i == len(nodo.hijos) - 1)


def arbol_a_texto(nodo, prefijo="", es_ultimo=True):
    """
    Igual que imprimir_arbol pero retorna el arbol como cadena de texto.
    """
    conector = "└── " if es_ultimo else "├── "
    lineas = [prefijo + conector + nodo.simbolo]

    nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
    for i, hijo in enumerate(nodo.hijos):
        lineas.append(arbol_a_texto(hijo, nuevo_prefijo, i == len(nodo.hijos) - 1))

    return "\n".join(lineas)
