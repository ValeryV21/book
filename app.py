import sqlite3
import streamlit as st

# --- База данни ---
conn = sqlite3.connect("books.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        year INTEGER,
        is_read INTEGER DEFAULT 0
    )
""")
conn.commit()

st.title("📚 Моята библиотека")

# --- Добавяне ---
st.subheader("➕ Добави книга")
title  = st.text_input("Заглавие")
author = st.text_input("Автор")
genre  = st.text_input("Жанр")
year   = st.number_input("Година", min_value=0, max_value=2100, value=2024, step=1)

if st.button("Добави"):
    if not title or not author:
        st.warning("Попълни заглавие и автор.")
        st.stop()
    c.execute("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)",
              (title, author, genre, year))
    conn.commit()
    st.success("Добавена!")

st.divider()

# --- Търсене ---
search = st.text_input("🔎 Търси по заглавие или автор")
if search:
    books = c.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        (f"%{search}%", f"%{search}%")
    ).fetchall()
else:
    books = c.execute("SELECT * FROM books ORDER BY year DESC").fetchall()

# --- Показване ---
st.subheader(f"Книги ({len(books)})")
for b in books:
    col1, col2, col3 = st.columns([5, 1, 1])
    status = "✅" if b[5] else "📖"
    col1.write(f"{status} **{b[1]}** — {b[2]}  |  {b[3]}  |  {b[4]}")
    if col2.button("Прочетена", key=f"r{b[0]}"):
        c.execute("UPDATE books SET is_read = 1 WHERE id = ?", (b[0],))
        conn.commit()
        st.rerun()
    if col3.button("🗑️", key=f"d{b[0]}"):
        c.execute("DELETE FROM books WHERE id = ?", (b[0],))
        conn.commit()
        st.rerun()
