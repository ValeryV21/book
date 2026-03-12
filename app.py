import streamlit as st
import requests

st.set_page_config(page_title="Търсене на книги", page_icon="📚")
st.title("📚 Търсене на книги")

# --- Избор на режим ---
режим = st.radio("Търси по:", ["Заглавие / ключова дума", "Автор"])

# --- Поле за търсене ---
заявка = st.text_input("Въведи заявка:")

# --- Функция за търсене на книги ---
def търси_книги(текст):
    url = "https://openlibrary.org/search.json"
    отговор = requests.get(url, params={"q": текст, "limit": 10})
    резултати = отговор.json().get("docs", [])
    return резултати

# --- Функция за търсене по автор ---
def търси_автор(ime):
    url = "https://openlibrary.org/search/authors.json"
    отговор = requests.get(url, params={"q": ime, "limit": 5})
    автори = отговор.json().get("docs", [])
    return автори

# --- Бутон и логика ---
if st.button("🔍 Търси") and заявка:

    if режим == "Заглавие / ключова дума":
        st.subheader("Намерени книги:")
        книги = търси_книги(заявка)

        if not книги:
            st.warning("Няма намерени книги.")
        else:
            for книга in книги:
                заглавие = книга.get("title", "Без заглавие")
                автор    = ", ".join(книга.get("author_name", ["Неизвестен"]))
                година   = книга.get("first_publish_year", "—")
                st.markdown(f"**{заглавие}**  \n✍️ {автор}  |  📅 {година}")
                st.divider()

    else:  # Търсене по автор
        st.subheader("Намерени автори:")
        автори = търси_автор(заявка)

        if not автори:
            st.warning("Няма намерени автори.")
        else:
            for автор in автори:
                ime       = автор.get("name", "—")
                години    = автор.get("birth_date", "—")
                творби    = автор.get("work_count", "—")
                st.markdown(f"**{ime}**  \n🎂 Роден: {години}  |  📖 Творби: {творби}")
                st.divider()
