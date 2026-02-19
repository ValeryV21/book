 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app.py b/app.py
new file mode 100644
index 0000000000000000000000000000000000000000..62ab3ad63befd6b30f4f20d76ce15529c935e80e
--- /dev/null
+++ b/app.py
@@ -0,0 +1,143 @@
+import sqlite3
+from pathlib import Path
+
+import streamlit as st
+
+DB_PATH = Path(__file__).with_name("books.db")
+
+
+def get_connection() -> sqlite3.Connection:
+    conn = sqlite3.connect(DB_PATH)
+    conn.row_factory = sqlite3.Row
+    return conn
+
+
+def init_db() -> None:
+    with get_connection() as conn:
+        conn.execute(
+            """
+            CREATE TABLE IF NOT EXISTS books (
+                id INTEGER PRIMARY KEY AUTOINCREMENT,
+                title TEXT NOT NULL,
+                author TEXT NOT NULL,
+                genre TEXT NOT NULL,
+                year INTEGER NOT NULL,
+                is_read INTEGER NOT NULL DEFAULT 0
+            )
+            """
+        )
+
+        has_rows = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
+        if has_rows:
+            return
+
+        bulgarian_books = [
+            ("Под игото", "Иван Вазов", "Класика", 1894, 1),
+            ("Тютюн", "Димитър Димов", "Роман", 1951, 0),
+            ("Железният светилник", "Димитър Талев", "Исторически", 1952, 0),
+            ("Бай Ганьо", "Алеко Константинов", "Сатира", 1895, 1),
+            ("Време разделно", "Антон Дончев", "Исторически", 1964, 0),
+        ]
+
+        conn.executemany(
+            "INSERT INTO books (title, author, genre, year, is_read) VALUES (?, ?, ?, ?, ?)",
+            bulgarian_books,
+        )
+
+
+def add_book(title: str, author: str, genre: str, year: int, is_read: bool) -> None:
+    with get_connection() as conn:
+        conn.execute(
+            "INSERT INTO books (title, author, genre, year, is_read) VALUES (?, ?, ?, ?, ?)",
+            (title.strip(), author.strip(), genre.strip() or "Неизвестен", year, int(is_read)),
+        )
+
+
+def load_books(search_query: str, unread_only: bool) -> list[dict]:
+    clauses: list[str] = []
+    params: list[str] = []
+
+    if search_query:
+        clauses.append("(title LIKE ? OR author LIKE ?)")
+        q = f"%{search_query.strip()}%"
+        params.extend([q, q])
+
+    if unread_only:
+        clauses.append("is_read = 0")
+
+    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
+    query = f"""
+        SELECT id, title, author, genre, year,
+               CASE WHEN is_read = 1 THEN 'Да' ELSE 'Не' END AS read_status
+        FROM books
+        {where_sql}
+        ORDER BY year DESC, title ASC
+    """
+
+    with get_connection() as conn:
+        rows = conn.execute(query, params).fetchall()
+
+    return [
+        {
+            "ID": row["id"],
+            "Заглавие": row["title"],
+            "Автор": row["author"],
+            "Жанр": row["genre"],
+            "Година": row["year"],
+            "Прочетена": row["read_status"],
+        }
+        for row in rows
+    ]
+
+
+def get_totals() -> tuple[int, int, int]:
+    with get_connection() as conn:
+        total, read = conn.execute(
+            "SELECT COUNT(*), COALESCE(SUM(is_read), 0) FROM books"
+        ).fetchone()
+
+    total = int(total)
+    read = int(read)
+    progress = int((read / total) * 100) if total else 0
+    return total, read, progress
+
+
+init_db()
+
+st.set_page_config(page_title="Списък с книги", page_icon="📚", layout="wide")
+st.title("📚 Списък с книги")
+st.caption("Приложение с база данни и начални български книги.")
+
+with st.sidebar:
+    st.header("Добави нова книга")
+    with st.form("add_book"):
+        title = st.text_input("Заглавие")
+        author = st.text_input("Автор")
+        genre = st.text_input("Жанр")
+        year = st.number_input("Година", min_value=0, max_value=3000, value=2024, step=1)
+        is_read = st.checkbox("Прочетена", value=False)
+        submit = st.form_submit_button("Запази")
+
+    if submit:
+        if not title.strip() or not author.strip():
+            st.error("Заглавието и авторът са задължителни.")    
+        else:
+            add_book(title, author, genre, int(year), is_read)
+            st.success(f"Книгата '{title.strip()}' беше добавена.")
+            st.rerun()
+
+c1, c2 = st.columns([2, 1])
+with c1:
+    search = st.text_input("Търсене по заглавие или автор")
+with c2:
+    unread_only = st.toggle("Само непрочетени", value=False)
+
+books = load_books(search, unread_only)
+st.subheader("Книги в базата")
+st.dataframe(books, use_container_width=True, hide_index=True)
+
+total, read, progress = get_totals()
+m1, m2, m3 = st.columns(3)
+m1.metric("Общо книги", total)
+m2.metric("Прочетени", read)
+m3.metric("Прогрес", f"{progress}%")
 
