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

---
## 1. Mengapa fungsi power() harus dipanggil di dalam term(), bukan sebaliknya?
Karena operator precedence (tingkat prioritas operator). Dalam hirarki matematika:

Pangkat (^) memiliki precedence lebih tinggi daripada perkalian (*) dan pembagian (/)

Perkalian/bagian memiliki precedence lebih tinggi daripada penjumlahan/pengurangan

Dengan memanggil power() di dalam term(), maka:

term() akan memproses operator * dan /

Sebelum memproses * atau /, term() terlebih dahulu memanggil power() yang memproses ^

Akibatnya, ekspresi seperti a ^ 2 * b akan diparsing sebagai (a ^ 2) * b, bukan a ^ (2 * b)

Jika sebaliknya (term() dipanggil di dalam power()), maka hierarki precedence akan terbalik dan pangkat akan dievaluasi setelah perkalian, yang salah secara matematika.

## 2. Apa yang terjadi pada fase Analisis Semantik jika variabel z digunakan tetapi tidak ada di symbol_table?
Fase analisis semantik akan mendeteksi error dan program akan berhenti dengan pesan error. Pada kode di atas, di method factor():

python
elif token and token.isalpha():
    if token not in self._env:
        raise ParserError(f"Semantic Error: Undefined variable '{token}'")
Ini adalah semantic checking yang memverifikasi keberadaan variabel dalam symbol table sebelum diizinkan digunakan. Tanpa ini, compiler akan menghasilkan kode yang merujuk ke variabel tidak terdefinisi, menyebabkan runtime error.

## 3. Mengapa dalam TAC, instruksi untuk a ^ 2 harus muncul sebelum instruksi untuk +?
Karena evaluasi expression mengikuti aturan operator precedence dan grammar recursive-descent:

expr() memanggil term() untuk operand kiri

term() memanggil power() untuk operand kiri

power() mendeteksi ^ dan langsung menghasilkan TAC untuk operasi pangkat

Barulah expr() memproses operator + setelah term() selesai

Alur parsing:

text
a ^ 2 + b * c
→ expr() memanggil term()
  → term() memanggil power()
    → power() melihat 'a ^ 2' → generate TAC t1 = a ^ 2
  → term() melihat '*' → generate TAC t2 = b * c
→ expr() melihat '+' → generate TAC t3 = t1 + t2
Ini sesuai dengan post-order traversal AST: anak dievaluasi sebelum induk, sehingga operasi pangkat dan perkalian dievaluasi terlebih dahulu sebelum penjumlahan.

