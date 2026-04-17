# Punto 2 — Parser recursivo descendente para el DSL CRUD NoSQL
# Implementación directa de la gramática del Punto 1
# Ejecutar: python punto2_parser.py

class Lexer:
    KEYWORDS = {
        'INSERT', 'INTO', 'FIND', 'IN', 'UPDATE',
        'SET', 'DELETE', 'FROM', 'WHERE', 'AND', 'true', 'false'
    }

    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.pos = 0
        self._tokenize()

    def _tokenize(self):
        i = 0
        text = self.text

        while i < len(text):
            # Espacios
            if text[i].isspace():
                i += 1

            # Comentarios de línea
            elif text[i:i+2] == '//':
                while i < len(text) and text[i] != '\n':
                    i += 1

            # Strings entre comillas
            elif text[i] == '"':
                j = i + 1
                while j < len(text) and text[j] != '"':
                    j += 1
                self.tokens.append(('STRING', text[i:j+1]))
                i = j + 1

            # Números
            elif text[i].isdigit():
                j = i
                while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                    j += 1
                self.tokens.append(('NUMBER', text[i:j]))
                i = j

            # Identificadores y keywords
            elif text[i].isalpha() or text[i] == '_':
                j = i
                while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                word = text[i:j]
                tok_type = word if word in self.KEYWORDS else 'ID'
                self.tokens.append((tok_type, word))
                i = j

            # Operadores de dos caracteres
            elif text[i:i+2] in ('==', '!=', '<=', '>='):
                self.tokens.append(('OP', text[i:i+2]))
                i += 2

            # Operadores de un carácter
            elif text[i] in '<>':
                self.tokens.append(('OP', text[i]))
                i += 1

            # Símbolos
            elif text[i] in '{},:;':
                self.tokens.append((text[i], text[i]))
                i += 1

            else:
                raise SyntaxError(f"Carácter no reconocido: '{text[i]}' en posición {i}")

        self.tokens.append(('EOF', 'EOF'))

    def peek(self):
        return self.tokens[self.pos]

    def consume(self, expected_type=None):
        tok = self.tokens[self.pos]
        if expected_type and tok[0] != expected_type:
            raise SyntaxError(
                f"Error en token #{self.pos}: esperado '{expected_type}', "
                f"encontrado '{tok[0]}' (valor: '{tok[1]}')"
            )
        self.pos += 1
        return tok

    def match(self, *types):
        return self.peek()[0] in types


class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)

    def parse(self):
        statements = []
        while not self.lexer.match('EOF'):
            statements.append(self._parse_statement())
        return statements

    def _parse_statement(self):
        tok = self.lexer.peek()
        if tok[0] == 'INSERT':
            return self._parse_insert()
        elif tok[0] == 'FIND':
            return self._parse_find()
        elif tok[0] == 'UPDATE':
            return self._parse_update()
        elif tok[0] == 'DELETE':
            return self._parse_delete()
        else:
            raise SyntaxError(f"Sentencia inválida: '{tok[1]}'")

    def _parse_insert(self):
        self.lexer.consume('INSERT')
        self.lexer.consume('INTO')
        collection = self.lexer.consume('ID')[1]
        doc = self._parse_document()
        self.lexer.consume(';')
        return ('INSERT', collection, doc)

    def _parse_find(self):
        self.lexer.consume('FIND')
        self.lexer.consume('IN')
        collection = self.lexer.consume('ID')[1]
        filter_ = None
        if self.lexer.match('WHERE'):
            self.lexer.consume('WHERE')
            filter_ = self._parse_filter()
        self.lexer.consume(';')
        return ('FIND', collection, filter_)

    def _parse_update(self):
        self.lexer.consume('UPDATE')
        collection = self.lexer.consume('ID')[1]
        self.lexer.consume('SET')
        assignment = self._parse_field_list()
        filter_ = None
        if self.lexer.match('WHERE'):
            self.lexer.consume('WHERE')
            filter_ = self._parse_filter()
        self.lexer.consume(';')
        return ('UPDATE', collection, assignment, filter_)

    def _parse_delete(self):
        self.lexer.consume('DELETE')
        self.lexer.consume('FROM')
        collection = self.lexer.consume('ID')[1]
        self.lexer.consume('WHERE')
        filter_ = self._parse_filter()
        self.lexer.consume(';')
        return ('DELETE', collection, filter_)

    def _parse_document(self):
        self.lexer.consume('{')
        fields = []
        if not self.lexer.match('}'):
            fields = self._parse_field_list()
        self.lexer.consume('}')
        return ('DOCUMENT', fields)

    def _parse_field_list(self):
        fields = [self._parse_field()]
        while self.lexer.match(','):
            self.lexer.consume(',')
            fields.append(self._parse_field())
        return fields

    def _parse_field(self):
        key = self.lexer.consume('STRING')[1]
        self.lexer.consume(':')
        value = self._parse_value()
        return (key, value)

    def _parse_filter(self):
        conditions = [self._parse_condition()]
        while self.lexer.match('AND'):
            self.lexer.consume('AND')
            conditions.append(self._parse_condition())
        return conditions

    def _parse_condition(self):
        field = self.lexer.consume('ID')[1]
        op = self.lexer.consume('OP')[1]
        value = self._parse_value()
        return (field, op, value)

    def _parse_value(self):
        tok = self.lexer.peek()
        if tok[0] == 'STRING':
            return self.lexer.consume('STRING')[1]
        elif tok[0] == 'NUMBER':
            return float(self.lexer.consume('NUMBER')[1])
        elif tok[0] == 'true':
            self.lexer.consume('true')
            return True
        elif tok[0] == 'false':
            self.lexer.consume('false')
            return False
        elif tok[0] == '{':
            return self._parse_document()
        else:
            raise SyntaxError(f"Valor no reconocido: '{tok[1]}'")


def parse(text):
    """Retorna el AST si la entrada es válida, lanza SyntaxError si no."""
    return Parser(text).parse()
