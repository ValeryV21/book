import sqlite3
import streamlit as st

conn = sqlite3.connect("books.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT
)
""")

st.title("📚 Библиотека")

title = st.text_input("Заглавие")
author = st.text_input("Автор")

if st.button("Добави книга"):
    c.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author)
    )
    conn.commit()
    st.success("Добавена!")

search = st.text_input("Търси книга или автор")

if search:
    books = c.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        ('%' + search + '%', '%' + search + '%')
    ).fetchall()
else:
    books = c.execute("SELECT * FROM books").fetchall()

st.subheader("Книги:")

for book in books:
    st.write(book[1], "-", book[2])
