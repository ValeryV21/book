import sqlite3
import streamlit as st

conn = sqlite3.connect("books.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    )
""")

st.title("📚 Библиотека")

# --- Добавяне ---
title  = st.text_input("Заглавие")
author = st.text_input("Автор")
if st.button("Добави книга"):
    if not title or not author:
        st.warning("Попълни и двете полета.")
        st.stop()
    c.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    st.success("Добавена!")

# --- Търсене ---
search = st.text_input("Търси книга или автор")
if search:
    books = c.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        ('%' + search + '%', '%' + search + '%')
    ).fetchall()
else:
    books = c.execute("SELECT * FROM books").fetchall()

# --- Показване ---
st.subheader(f"Книги: ({len(books)})")
for book in books:
    col1, col2 = st.columns([6, 1])
    col1.write(f"{book[1]} — {book[2]}")
    if col2.button("🗑️", key=book[0]):
        c.execute("DELETE FROM books WHERE id = ?", (book[0],))
        conn.commit()
        st.rerun()
