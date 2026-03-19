import streamlit as st



books = [
{“title”: “Хари Потър”,        “author”: “Дж. К. Роулинг”, “price”: 15.99, “genre”: “Фентъзи”},
{“title”: “Властелинът на пръстените”, “author”: “Дж. Р. Р. Толкин”, “price”: 22.50, “genre”: “Фентъзи”},
{“title”: “1984”,              “author”: “Джордж Оруел”,   “price”: 12.00, “genre”: “Антиутопия”},
{“title”: “Малкият принц”,     “author”: “Антоан дьо Сент-Екзюпери”, “price”: 8.99, “genre”: “Класика”},
{“title”: “Дон Кихот”,         “author”: “Мигел де Сервантес”, “price”: 18.00, “genre”: “Класика”},
{“title”: “Мартин Идън”,       “author”: “Джак Лондон”,    “price”: 10.50, “genre”: “Роман”},
{“title”: “Алхимикът”,         “author”: “Паулу Коелю”,    “price”: 13.99, “genre”: “Философия”},
{“title”: “Престъпление и наказание”, “author”: “Достоевски”, “price”: 16.00, “genre”: “Класика”},
]



st.title(“📚 Каталог с книги”)
st.markdown(“Намери книга по **заглавие** или **цена**”)
st.divider()



col1, col2 = st.columns(2)

with col1:
search_title = st.text_input(“🔍 Търси по заглавие”, placeholder=“напр. Хари…”)

with col2:
max_price = st.slider(“💰 Максимална цена (лв.)”,
min_value=0.0,
max_value=50.0,
value=50.0,
step=0.5)

st.divider()



results = [
book for book in books
if search_title.lower() in book[“title”].lower()   # търси в заглавието
and book[“price”] <= max_price                      # проверява цената
]



st.subheader(f”📖 Намерени книги: {len(results)}”)

if results:
for book in results:
with st.container(border=True):
col_a, col_b = st.columns([3, 1])
with col_a:
st.markdown(f”### {book[‘title’]}”)
st.write(f”✍️ **Автор:** {book[‘author’]}”)
st.write(f”🏷️ **Жанр:** {book[‘genre’]}”)
with col_b:
st.metric(“Цена”, f”{book[‘price’]:.2f} лв.”)
else:
st.warning(“Няма намерени книги. Опитай с друго заглавие или по-висока цена.”)