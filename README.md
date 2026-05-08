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
# 1. Mengapa `power()` harus dipanggil di dalam `term()`, bukan sebaliknya?

Ini berkaitan langsung dengan **Operator Precedence (Hierarki Operator)**.

Dalam matematika, urutan prioritas dari terendah ke tertinggi adalah:

```
+ dan -   (paling rendah)
* dan /
^         (paling tinggi)
( )  dan  angka/variabel
```

Struktur fungsi dalam parser mencerminkan hierarki ini secara terbalik — fungsi yang menangani prioritas lebih rendah memanggil fungsi yang menangani prioritas lebih tinggi:

```
expr()   → memanggil → term()
term()   → memanggil → power()
power()  → memanggil → factor()
```

Jika `term()` tidak memanggil `power()` melainkan sebaliknya, maka ekspresi seperti `a ^ 2 * 3` akan diparse sebagai `a ^ (2 * 3)` — salah. Dengan struktur yang benar, parser akan menghasilkan `(a ^ 2) * 3` sesuai aturan matematika.

---

# 2. Apa yang terjadi jika variabel `z` digunakan tapi tidak ada di `symbol_table`?

Pada fase **Analisis Semantik**, fungsi `factor()` mengecek apakah variabel terdaftar di `self._env`:

```python
elif token and token.isalpha():
    if token not in self._env:
        raise ParserError(f"Semantic Error: Undefined variable '{token}'")
```

Jika `z` tidak ada di `symbol_table`, maka akan muncul:

```
Error: Semantic Error: Undefined variable 'z'
```

Ini adalah contoh **Semantic Error** — kode sintaksnya benar, tapi maknanya tidak valid karena variabel belum dideklarasikan.

---

# 3. Mengapa instruksi `a ^ 2` harus muncul sebelum `+` di TAC?

Karena fungsi `generate_tac()` bekerja secara **rekursif post-order** (kiri → kanan → root):

1. Untuk node `+`, fungsi pertama memanggil `generate_tac(node.left)` → yaitu node `a ^ 2`
2. Baru kemudian `generate_tac(node.right)` → yaitu node `b * c`
3. Setelah keduanya selesai, barulah instruksi `t3 = t1 + t2` dihasilkan

Ini sesuai prinsip TAC: **setiap operan harus sudah dihitung sebelum digunakan**. Komputer tidak bisa menjalankan `t3 = t1 + t2` jika `t1` belum diketahui nilainya.
