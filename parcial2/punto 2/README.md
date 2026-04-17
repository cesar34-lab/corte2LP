# Punto 2 — Parser CRUD NoSQL

## Archivos

| Archivo | Descripción |
|---|---|
| `punto2_NoSQLCRUD.g4` | Gramática ANTLR4 (lexer + parser) |
| `punto2_parser.py` | Parser recursivo descendente en Python |
| `punto2_test_cases.py` | Suite de pruebas (17 casos) |

---

## Arquitectura

```
Texto fuente
    ↓
 Lexer         — tokeniza keywords, strings, números, operadores
    ↓
 Parser        — recursivo descendente, sigue directamente la CFG del Punto 1
    ↓
 AST (tuplas)  — Insert(...) | Find(...) | Update(...) | Delete(...)
```

### Lexer (`class Lexer`)
- Un solo paso lineal sobre el texto fuente.
- Tokens producidos: keywords, `ID`, `STRING`, `NUMBER`, `OP`, símbolos.
- `peek()` mira el token actual sin consumirlo.
- `consume(expected)` valida tipo y avanza; lanza `SyntaxError` si no coincide.

### Parser (`class Parser`)
- Cada método `_parse_X()` corresponde a la producción `X` de la gramática.
- Predicción basada en `lexer.peek()` — sin backtracking.
- `parse()` retorna lista de tuplas (el AST implícito).

---

## Cómo ejecutar

### Opción A — Python puro (sin instalaciones)
```bash
python punto2_test_cases.py
```

### Opción B — ANTLR4
```bash
pip install antlr4-tools
antlr4 -Dlanguage=Python3 punto2_NoSQLCRUD.g4
antlr4-parse punto2_NoSQLCRUD.g4 program -tree
# pegar sentencias y Ctrl+D
```

---

## Casos de prueba

### Válidos (10)
| Caso | Entrada |
|---|---|
| INSERT básico | `INSERT INTO users {"name": "Ana", "age": 22};` |
| INSERT anidado | `INSERT INTO orders {"id": "001", "item": {"name": "Laptop"}};` |
| FIND sin filtro | `FIND IN products;` |
| FIND con filtro | `FIND IN users WHERE name == "Ana";` |
| FIND multiples AND | `FIND IN users WHERE age >= 18 AND active == true;` |
| UPDATE con WHERE | `UPDATE users SET "age": 23 WHERE name == "Ana";` |
| UPDATE sin WHERE | `UPDATE products SET "available": true;` |
| DELETE | `DELETE FROM users WHERE age < 18;` |
| Múltiples sentencias | tres sentencias encadenadas |
| Boolean en doc | `INSERT INTO settings {"darkMode": true};` |

### Inválidos (7)
| Caso | Razón del fallo |
|---|---|
| INSERT sin INTO | falta keyword INTO |
| FIND sin IN | falta keyword IN |
| DELETE sin WHERE | WHERE es obligatorio en DELETE |
| Sin punto y coma | el `;` es requerido |
| Documento sin `}` | llave sin cerrar |
| Operador `===` | no está en la gramática |
| Keyword como colección | `WHERE` no es un ID válido |

---

## Resultado esperado
```
Resultado: 17/17 pruebas pasadas
```
