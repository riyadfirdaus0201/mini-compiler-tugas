# Mini Compiler — Teknik Kompilasi

Implementasi Mini Compiler dengan dukungan Lexer, Parser (EBNF), AST, dan TAC.

## Cara Menjalankan

```bash
python mini_compiler.py
```

## Output

```
Input: a ^ 2 + b * c

--- Output Three Address Code (TAC) ---
t1 = a ^ 2
t2 = b * c
t3 = t1 + t2
```

**1. Mengapa `power()` dipanggil di dalam `term()`, bukan sebaliknya?**

Ini berkaitan dengan *operator precedence*. Dalam parsing rekursif descent, fungsi yang dipanggil *lebih dalam* mengikat lebih ketat (prioritas lebih tinggi). Hirarki panggilan adalah:

```
expr() → term() → power() → factor()
```

Karena `term()` memanggil `power()`, artinya `^` akan dievaluasi *lebih dulu* dari `*` dan `/`. Jika dibalik (`power()` memanggil `term()`), maka `*` dan `/` justru akan punya prioritas lebih tinggi dari `^`, yang bertentangan dengan aturan matematika.

**2. Apa yang terjadi jika variabel `z` tidak ada di `symbol_table`?**

Fase *Semantic Analysis* akan mendeteksi bahwa `z` tidak terdefinisi. Pada kode ini, pemeriksaan dilakukan di fungsi `factor()`:
```python
if token not in self._env:
    raise ParserError(f"Semantic Error: Undefined variable '{z}'")
```
Program akan berhenti dan melempar `ParserError`. Ini adalah contoh *undeclared variable error* — secara sintaks valid, tapi secara semantik salah karena tidak ada nilai yang bisa dikaitkan.

**3. Mengapa instruksi `a ^ 2` harus muncul lebih dulu dari `+` di TAC?**

Karena TAC dihasilkan secara *post-order traversal* pada AST — anak-anak dievaluasi sebelum induknya. Untuk ekspresi `a ^ 2 + b * c`, AST-nya menempatkan `+` sebagai root, dengan `a^2` dan `b*c` sebagai subpohon. Sebelum bisa menghasilkan `t3 = t1 + t2`, kompiler harus tahu nilai `t1` (hasil `a^2`) dan `t2` (hasil `b*c`) terlebih dahulu. Urutan TAC yang benar:
```
t1 = a ^ 2
t2 = b * c
t3 = t1 + t2
```
