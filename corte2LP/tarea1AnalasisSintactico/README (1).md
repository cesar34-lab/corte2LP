# Analizador Sintáctico con AST

Implementación de un analizador sintáctico **LL(1) descendente predictivo** en Python. Dado un archivo `.txt` con una gramática libre de contexto y una cadena de texto crudo, el sistema la tokeniza automáticamente y genera el **Árbol de Sintaxis Abstracta (AST)** correspondiente.

---

## Estructura del proyecto

```
proyecto/
├── main.py                    # Punto de entrada, orquesta todo el flujo
├── lexer.py                   # Tokeniza la cadena de texto crudo
├── lector_gramatica.py        # Lee y parsea el archivo .txt
├── parser_ll1.py              # Lógica LL(1): PRIMERO, SIGUIENTE, tabla y análisis
├── ast_nodo.py                # Clase NodoAST e impresión del árbol
├── gramatica.txt              # Archivo de entrada de ejemplo
├── ejemplo_declaraciones.txt
├── ejemplo_booleanos.txt
├── ejemplo_listas.txt
├── ejemplo_funciones.txt
└── salida.txt                 # Salida generada automáticamente al ejecutar
```

---

## Cómo ejecutar

### Requisitos

Solo se necesita **Python 3.8 o superior**. El proyecto no usa librerías externas.

### Pasos

**1.** Colocar todos los archivos `.py` en la misma carpeta.

**2.** Crear o editar el archivo `.txt` con la gramática y la cadena (ver formato más abajo).

**3.** Ejecutar desde la terminal:

```bash
python main.py gramatica.txt
```

**4.** El programa imprime en consola cada etapa del proceso y guarda el resultado en `salida.txt`.

> Para usar otro archivo:
> ```bash
> python main.py ruta/al/archivo.txt
> ```

---

## Formato del archivo de entrada

El archivo `.txt` tiene tres partes: producciones de la gramática, una sección opcional `[lexer]` y la cadena a analizar.

### Producciones

```
no_terminal -> cuerpo1 | cuerpo2 | ...
```

- Los símbolos en **MAYÚSCULAS** son terminales (tokens).
- Los símbolos en **minúsculas** son no-terminales.
- La cadena vacía se representa con `eps`.
- La **primera producción** define el símbolo inicial.
- Las líneas que empiezan con `#` son comentarios.

### Cadena de entrada

La cadena **siempre** se escribe como texto crudo. El lexer la tokeniza automáticamente:

```
cadena_raw: holaComoEstas = 2 + 3 * x
```

### Sección `[lexer]` (opcional)

Si no se define, el lexer usa reglas predeterminadas que reconocen los tokens más comunes. Si se necesitan palabras reservadas o tokens específicos, se define esta sección:

```
[lexer]
NOMBRE_TOKEN : patron_regex
```

> **Importante:** las reglas se aplican en orden. Las palabras reservadas deben ir **siempre antes** que `ID`.

```
# Correcto: INT se reconoce antes de intentar ID
[lexer]
INT  : int
ID   : [a-zA-Z_][a-zA-Z0-9_]*

# Incorrecto: ID capturaría "int" antes de llegar a INT
[lexer]
ID   : [a-zA-Z_][a-zA-Z0-9_]*
INT  : int
```

### Tokens predeterminados (sin sección `[lexer]`)

| Token | Reconoce |
|---|---|
| `NUMBER` | Enteros y decimales: `42`, `3.14` |
| `ID` | Identificadores: `x`, `holaComoEstas`, `_var` |
| `STRING` | Cadenas entre comillas: `"texto"`, `'texto'` |
| `RELOP` | Operadores relacionales: `<=`, `>=`, `==`, `!=`, `<`, `>` |
| `PLUS` | `+` |
| `MINUS` | `-` |
| `TIMES` | `*` |
| `DIVIDE` | `/` |
| `EQUALS` | `=` |
| `LPAREN` | `(` |
| `RPAREN` | `)` |
| `LBRACKET` | `[` |
| `RBRACKET` | `]` |
| `LBRACE` | `{` |
| `RBRACE` | `}` |
| `SEMICOLON` | `;` |
| `COMMA` | `,` |
| `DOT` | `.` |
| `WHITESPACE` | Espacios e indentación (se ignoran automáticamente) |

---

## Ejemplos de archivos de entrada

### Expresiones aritméticas

```
expr    -> term expr_r
expr_r  -> PLUS term expr_r | MINUS term expr_r | eps
term    -> factor term_r
term_r  -> TIMES factor term_r | DIVIDE factor term_r | eps
factor  -> LPAREN expr RPAREN | NUMBER | ID

cadena_raw: resultado + 3 * (x - 2)
```

### Declaraciones de variables (con palabras reservadas)

```
programa    -> declaracion programa | eps
declaracion -> tipo ID SEMICOLON
tipo        -> INT | FLOAT | BOOL

[lexer]
INT        : int
FLOAT      : float
BOOL       : bool
ID         : [a-zA-Z_][a-zA-Z0-9_]*
SEMICOLON  : ;
WHITESPACE : \s+

cadena_raw: int miVariable ; float otroValor ;
```

### Expresiones booleanas

```
bool_expr   -> bool_term bool_expr_r
bool_expr_r -> OR bool_term bool_expr_r | eps
bool_term   -> bool_factor bool_term_r
bool_term_r -> AND bool_factor bool_term_r | eps
bool_factor -> NOT bool_factor | TRUE | FALSE | ID

[lexer]
TRUE       : true
FALSE      : false
AND        : and
OR         : or
NOT        : not
ID         : [a-zA-Z_][a-zA-Z0-9_]*
WHITESPACE : \s+

cadena_raw: true and false or not true
```

### Listas entre corchetes

```
lista     -> LBRACKET contenido RBRACKET
contenido -> elemento resto | eps
resto     -> COMMA elemento resto | eps
elemento  -> NUMBER | ID | STRING

cadena_raw: [ 10 , holaComoEstas , "texto" ]
```

### Llamadas a función

```
llamada    -> ID LPAREN argumentos RPAREN
argumentos -> argumento resto | eps
resto      -> COMMA argumento resto | eps
argumento  -> ID | NUMBER | STRING

[lexer]
STRING     : "[^"]*"
NUMBER     : \d+(\.\d+)?
ID         : [a-zA-Z_][a-zA-Z0-9_]*
LPAREN     : \(
RPAREN     : \)
COMMA      : ,
WHITESPACE : \s+

cadena_raw: calcularTotal(precioBase, 12, "descuento")
```

---

## Ejemplo de salida

Para `cadena_raw: resultado + 3 * (x - 2)`:

```
Texto original   : resultado + 3 * (x - 2)
Tokens generados : ID PLUS NUMBER TIMES LPAREN ID MINUS NUMBER RPAREN
```

**AST generado:**

```
└── expr
    ├── term
    │   ├── factor
    │   │   └── ID
    │   └── term_r
    │       └── eps
    └── expr_r
        ├── PLUS
        ├── term
        │   ├── factor
        │   │   └── NUMBER
        │   └── term_r
        │       ├── TIMES
        │       ├── factor
        │       │   ├── LPAREN
        │       │   ├── expr
        │       │   │   ├── term
        │       │   │   │   ├── factor
        │       │   │   │   │   └── ID
        │       │   │   │   └── term_r
        │       │   │   │       └── eps
        │       │   │   └── expr_r
        │       │   │       ├── MINUS
        │       │   │       ├── term
        │       │   │       │   ├── factor
        │       │   │       │   │   └── NUMBER
        │       │   │       │   └── term_r
        │       │   │       │       └── eps
        │       │   │       └── expr_r
        │       │   │           └── eps
        │       │   └── RPAREN
        │       └── term_r
        │           └── eps
        └── expr_r
            └── eps
```

**Cadena generada por el árbol:**

```
ID PLUS NUMBER TIMES LPAREN ID MINUS NUMBER RPAREN
```

---

## Descripción de los módulos

### `lexer.py`

Tokeniza el texto crudo carácter a carácter usando expresiones regulares. Todas las reglas se compilan en un solo patrón con grupos nombrados, lo que permite identificar qué regla coincidió. `WHITESPACE` siempre se ignora. Expone dos funciones: `tokenizar` para convertir texto en lista de tokens, y `leer_reglas_lexer` para extraer la sección `[lexer]` del archivo.

### `lector_gramatica.py`

Lee el archivo `.txt` línea por línea, ignora comentarios, extrae las producciones en un diccionario, detecta la sección `[lexer]` y finalmente llama al lexer con `cadena_raw`. Si el archivo no tiene `cadena_raw:`, el programa lanza un error y para.

### `parser_ll1.py`

Núcleo del analizador. Contiene cuatro funciones: `calcular_primero` y `calcular_siguiente` por punto fijo, `construir_tabla` que llena `M[A, a]` según las reglas LL(1) y reporta conflictos si la gramática no es LL(1), y `analizar` que ejecuta el algoritmo de pila construyendo el AST al mismo tiempo que consume la entrada.

### `ast_nodo.py`

Define la clase `NodoAST` con dos atributos: `simbolo` e `hijos`. Un nodo sin hijos es una hoja (terminal). Las funciones `imprimir_arbol` y `arbol_a_texto` recorren el árbol en profundidad y generan la representación visual con conectores `└──` y `├──`.

### `main.py`

Orquesta todo el flujo en orden: leer archivo → tokenizar → calcular PRIMERO/SIGUIENTE → construir tabla → analizar → imprimir árbol → guardar `salida.txt`. Imprime cada etapa en consola para verificar el proceso paso a paso.

---

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `El archivo no contiene 'cadena_raw:'` | Falta la línea o se usó el formato antiguo `cadena:` | Escribir la cadena con `cadena_raw:` |
| `Carácter no reconocido en posición N` | El lexer encontró un símbolo sin regla | Agregar la regla en la sección `[lexer]` |
| `conflicto en M[A, a]` | La gramática tiene recursión izquierda o ambigüedad | Transformar la gramática eliminando la recursión izquierda |
| `no hay producción para [A, a]` | La cadena no pertenece al lenguaje | Verificar que la cadena sea válida para la gramática |
| `tokens sobrantes desde '...'` | La cadena tiene más tokens de los que la gramática deriva | Revisar la cadena en `cadena_raw:` |
| `FileNotFoundError` | El archivo no existe en la ruta indicada | Verificar nombre y ruta del archivo |

---

## Limitaciones

- Solo soporta gramáticas **LL(1)**. Las que tienen recursión izquierda deben transformarse antes.
- El analizador es **sintáctico puro**: no realiza análisis semántico ni verificación de tipos.
- Las palabras reservadas deben definirse en `[lexer]` **antes** que `ID`, de lo contrario el lexer las trata como identificadores.
- `eps` solo se usa como alternativa completa de una producción, no en medio de un cuerpo.
