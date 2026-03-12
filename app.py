import sqlite3
import streamlit as st

conn = sqlite3.connect("books.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    year INTEGER
)
""")

st.title("📚 Моята библиотека")

st.header("Добави книга")

title = st.text_input("Заглавие")
author = st.text_input("Автор")
year = st.number_input("Година", 0, 3000, 2024)

if st.button("Добави"):
    c.execute(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        (title, author, year),
    )
    conn.commit()
    st.success("Книгата е добавена")

st.header("Всички книги")

books = c.execute("SELECT * FROM books").fetchall()

for book in books:
    st.write(f"{book[1]} - {book[2]} ({book[3]})")
