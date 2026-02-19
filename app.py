import pandas as pd
import streamlit as st

st.set_page_config(page_title="Book List", page_icon="📚", layout="wide")

st.title("📚 Book List")
st.caption("Track your favorite books and explore your reading list.")

if "books" not in st.session_state:
    st.session_state.books = [
        {"Title": "1984", "Author": "George Orwell", "Genre": "Dystopian", "Year": 1949, "Read": True},
        {"Title": "The Hobbit", "Author": "J.R.R. Tolkien", "Genre": "Fantasy", "Year": 1937, "Read": True},
        {"Title": "Sapiens", "Author": "Yuval Noah Harari", "Genre": "History", "Year": 2011, "Read": False},
    ]

with st.sidebar:
    st.header("Add a book")
    with st.form("add_book"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.text_input("Genre")
        year = st.number_input("Year", min_value=0, max_value=3000, value=2024, step=1)
        read = st.checkbox("Already read", value=False)
        submit = st.form_submit_button("Add")

    if submit:
        if not title.strip() or not author.strip():
            st.error("Title and author are required.")
        else:
            st.session_state.books.append(
                {
                    "Title": title.strip(),
                    "Author": author.strip(),
                    "Genre": genre.strip() or "Unknown",
                    "Year": int(year),
                    "Read": read,
                }
            )
            st.success(f"Added '{title.strip()}'")

books_df = pd.DataFrame(st.session_state.books)

col1, col2 = st.columns([2, 1])
with col1:
    query = st.text_input("Search by title or author")
with col2:
    show_unread_only = st.toggle("Show unread only", value=False)

filtered_df = books_df.copy()
if query:
    mask = filtered_df["Title"].str.contains(query, case=False, na=False) | filtered_df["Author"].str.contains(query, case=False, na=False)
    filtered_df = filtered_df[mask]

if show_unread_only:
    filtered_df = filtered_df[~filtered_df["Read"]]

st.subheader("Your books")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

read_count = int(books_df["Read"].sum())
book_count = len(books_df)
percent_read = (read_count / book_count * 100) if book_count else 0

c1, c2, c3 = st.columns(3)
c1.metric("Total books", book_count)
c2.metric("Books read", read_count)
c3.metric("Progress", f"{percent_read:.0f}%")
