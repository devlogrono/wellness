import streamlit as st
import time
from src.cookie_manager import cookie_set, cookie_get, cookie_delete

st.title("🔍 Test de Cookie Manager (Streamlit)")


cookie_name = "MY_COOKIE"


# SET
st.write("### 1. SET COOKIE")
cookie_set(cookie_name, "Jose123", days=1)
st.success("Cookie creada (MY_COOKIE=Jose123)")

time.sleep(0.2)

# GET
st.write("### 2. GET COOKIE")
value = cookie_get(cookie_name)
st.write("Valor leído:", value)

time.sleep(5)

# DELETE
st.write("### 3. DELETE COOKIE")
cookie_delete(cookie_name)
st.info("Cookie eliminada")

st.write("---")
st.write("Valor leído al cargar la página:")
st.write("GET inicial →", repr(cookie_get(cookie_name, key="initial_get")))
