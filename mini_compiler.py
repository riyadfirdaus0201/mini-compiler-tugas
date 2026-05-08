import re

# ============================================================
# BAGIAN 1: Definisi Node AST
# ============================================================

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, value):
        self.value = value

class Var(AST):
    def __init__(self, name):
        self.name = name

class ParserError(Exception):
    pass


# ============================================================
# BAGIAN 2: Implementasi MiniCompiler
# ============================================================

class MiniCompiler:
    def __init__(self, source, env):
        # TUGAS 1 ✅ — Tambahkan '\^' ke dalam regex agar '^' dikenali sebagai token
        self._tokens = iter(
            re.findall(r'[a-zA-Z_]\w*|\d+(?:\.\d+)?|[+*/()\-\^]', source) + ['?']
        )
        self._current = None
        self._env = env
        self._temp_count = 0
        self.advance()

    def advance(self):
        try:
            self._current = next(self._tokens)
        except StopIteration:
            self._current = None

    def expect(self, expected):
        if self._current != expected and not (expected == "ID" and self._current.isalnum()):
            raise ParserError(f"Expected {expected}, found {self._current}")
        token = self._current
        self.advance()
        return token

    def factor(self):
        token = self._current
        if token is not None and token.replace('.', '', 1).isdigit():
            self.advance()
            return Num(float(token) if '.' in token else int(token))
        elif token and token.isalpha():
            if token not in self._env:
                raise ParserError(f"Semantic Error: Undefined variable '{token}'")
            self.advance()
            return Var(token)
        elif token == '(':
            self.advance()
            node = self.expr()
            self.expect(')')
            return node
        raise ParserError(f"Unexpected token: {token}")

    # TUGAS 2 ✅ — Implementasi fungsi power()
    def power(self):
        node = self.factor()
        while self._current == '^':
            op = self._current
            self.advance()
            # Pangkat bersifat right-associative: 2^3^2 = 2^(3^2)
            # Maka sisi kanan memanggil power() lagi (rekursif), bukan factor()
            node = BinOp(left=node, op=op, right=self.power())
        return node

    # TUGAS 3 ✅ — Hubungkan term() ke power()
    def term(self):
        node = self.power()  # <-- diganti dari self.factor() ke self.power()
        while self._current in ('*', '/'):
            op = self._current
            self.advance()
            node = BinOp(left=node, op=op, right=self.power())  # <-- kanan juga power()
        return node

    def expr(self):
        node = self.term()
        while self._current in ('+', '-'):
            op = self._current
            self.advance()
            node = BinOp(left=node, op=op, right=self.term())
        return node

    def generate_tac(self, node):
        if isinstance(node, Num):
            return str(node.value)
        if isinstance(node, Var):
            return node.name

        left_val = self.generate_tac(node.left)
        right_val = self.generate_tac(node.right)

        self._temp_count += 1
        temp_name = f"t{self._temp_count}"
        print(f"{temp_name} = {left_val} {node.op} {right_val}")
        return temp_name


# ============================================================
# BAGIAN 3: Uji Coba
# ============================================================

source_code = "a ^ 2 + b * c"
symbol_table = {'a': 5, 'b': 10, 'c': 2}

try:
    print(f"Input: {source_code}")
    compiler = MiniCompiler(source_code, symbol_table)
    ast_root = compiler.expr()

    print("\n--- Output Three Address Code (TAC) ---")
    compiler.generate_tac(ast_root)
except Exception as e:
    print(f"Error: {e}")