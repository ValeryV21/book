import sqlite3
import streamlit as st

# връзка с базата
conn = sqlite3.connect("books.db", check_same_thread=False)
c = conn.cursor()

# създаване на таблица
c.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT
)
""")

st.title("📚 Моята библиотека")

# добавяне на книга
st.header("Добави книга")

title = st.text_input("Заглавие")
author = st.text_input("Автор")

if st.button("Добави"):
    if title and author:
        c.execute("INSERT INTO books(title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        st.success("Книгата е добавена")

# търсене
st.header("Търсене")

search = st.text_input("Търси по заглавие или автор")

if search:
    books = c.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        ('%' + search + '%', '%' + search + '%')
    ).fetchall()
else:
    books = c.execute("SELECT * FROM books").fetchall()

# показване на книгите
st.header("Книги")

for book in books:
    st.write(book[1], "-", book[2])
