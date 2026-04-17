# Punto 2 — Casos de prueba del parser CRUD NoSQL
# Ejecutar: python3 test_cases.py

from parser import parse

# (descripcion, input, debe_ser_valido)
TEST_CASES = [
    # ── Casos válidos ──────────────────────────────────────────────────────
    (
        "INSERT básico",
        'INSERT INTO users {"name": "Ana", "age": 22};',
        True
    ),
    (
        "INSERT documento anidado",
        'INSERT INTO orders {"id": "001", "item": {"name": "Laptop", "price": 1200}};',
        True
    ),
    (
        "FIND sin filtro",
        'FIND IN products;',
        True
    ),
    (
        "FIND con filtro simple",
        'FIND IN users WHERE name == "Ana";',
        True
    ),
    (
        "FIND con múltiples condiciones AND",
        'FIND IN users WHERE age >= 18 AND active == true;',
        True
    ),
    (
        "UPDATE con WHERE",
        'UPDATE users SET "age": 23 WHERE name == "Ana";',
        True
    ),
    (
        "UPDATE sin WHERE",
        'UPDATE products SET "available": true;',
        True
    ),
    (
        "DELETE",
        'DELETE FROM users WHERE age < 18;',
        True
    ),
    (
        "Múltiples sentencias",
        '''
        INSERT INTO users {"name": "Juan"};
        FIND IN users WHERE name == "Juan";
        DELETE FROM users WHERE name == "Juan";
        ''',
        True
    ),
    (
        "Valor booleano en documento",
        'INSERT INTO settings {"darkMode": true, "notifications": false};',
        True
    ),

    # ── Casos inválidos ────────────────────────────────────────────────────
    (
        "INSERT sin INTO",
        'INSERT users {"name": "Ana"};',
        False
    ),
    (
        "FIND sin IN",
        'FIND users;',
        False
    ),
    (
        "DELETE sin WHERE",
        'DELETE FROM users;',
        False
    ),
    (
        "Sentencia sin punto y coma",
        'FIND IN users',
        False
    ),
    (
        "Documento sin llave de cierre",
        'INSERT INTO users {"name": "Ana";',
        False
    ),
    (
        "Operador inválido",
        'FIND IN users WHERE age === 5;',
        False
    ),
    (
        "Keyword como colección (ambigüedad resuelta: falla en lexer/parser)",
        'FIND IN WHERE;',
        False
    ),
]


def run_tests():
    passed = 0
    failed = 0

    for desc, input_text, should_be_valid in TEST_CASES:
        try:
            ast = parse(input_text)
            is_valid = True
        except (SyntaxError, ValueError):
            is_valid = False

        ok = (is_valid == should_be_valid)
        status = "✓ PASS" if ok else "✗ FAIL"
        if ok:
            passed += 1
        else:
            failed += 1

        expected_str = "válido" if should_be_valid else "inválido"
        got_str = "válido" if is_valid else "inválido"
        print(f"{status} | {desc}")
        if not ok:
            print(f"       Esperado: {expected_str} | Obtenido: {got_str}")
            print(f"       Input: {input_text[:60].strip()}...")

    print(f"\nResultado: {passed}/{passed+failed} pruebas pasadas")


if __name__ == '__main__':
    run_tests()
