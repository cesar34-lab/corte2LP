# Punto 1 — Gramática CRUD NoSQL

## Diseño del DSL

DSL orientado a documentos (estilo MongoDB). Las operaciones son:
- `INSERT INTO collection document`
- `FIND IN collection [WHERE filter]`
- `UPDATE collection SET fields [WHERE filter]`
- `DELETE FROM collection WHERE filter`

---

## Gramática en BNF

```
program      ::= statement*

statement    ::= insert_stmt
               | find_stmt
               | update_stmt
               | delete_stmt

insert_stmt  ::= "INSERT" "INTO" ID document ";"
find_stmt    ::= "FIND" "IN" ID ("WHERE" filter)? ";"
update_stmt  ::= "UPDATE" ID "SET" field_list ("WHERE" filter)? ";"
delete_stmt  ::= "DELETE" "FROM" ID "WHERE" filter ";"

document     ::= "{" field_list? "}"
field_list   ::= field ("," field)*
field        ::= STRING ":" value

filter       ::= condition ("AND" condition)*
condition    ::= ID operator value

operator     ::= "==" | "!=" | "<" | ">" | "<=" | ">="

value        ::= STRING
               | NUMBER
               | BOOLEAN
               | document

ID           ::= [a-zA-Z][a-zA-Z0-9_]*
STRING       ::= '"' [^"]* '"'
NUMBER       ::= [0-9]+ ("." [0-9]+)?
BOOLEAN      ::= "true" | "false"
```

---

## Justificación de diseño

| Decisión | Razón |
|---|---|
| `field_list` sin recursión izquierda | Compatible con parsers LL |
| Solo `AND` en `filter` | Evita ambigüedad; `OR` se agrega con paréntesis en v2 |
| Claves de documento solo `STRING` | Evita colisión con keywords (`ID` podría ser `WHERE`) |
| `DELETE` siempre requiere `WHERE` | Previene borrado accidental de toda la colección |
| Punto y coma obligatorio | Permite múltiples sentencias en un programa |

---

## Ejemplos de sentencias válidas

```
INSERT INTO users {"name": "Ana", "age": 22};

FIND IN users WHERE name == "Ana";

UPDATE users SET "age": 23 WHERE name == "Ana";

DELETE FROM users WHERE age < 18;

FIND IN products;

INSERT INTO orders {"id": "001", "item": {"name": "Laptop", "price": 1200}};
```

---

## AST implícito

Cada sentencia mapea directamente a un nodo semántico:

```
Insert(collection: ID, document: Document)
Find(collection: ID, filter: Filter | None)
Update(collection: ID, fields: FieldList, filter: Filter | None)
Delete(collection: ID, filter: Filter)

Document(fields: List[Field])
Field(key: String, value: Value)
Filter(conditions: List[Condition])
Condition(field: ID, op: Operator, value: Value)
```
