import streamlit as st
from db import supabase

st.set_page_config(page_title="Taxi Hotel", page_icon="🚕", layout="centered")

# Estilos
st.markdown("""
    <style>
    .main { background-color: #FFF9DB; }
    h1 { color: #1a1a1a; }
    .stButton>button {
        background-color: #FACC15;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1em;
        border: none;
    }
    .stButton>button:hover { background-color: #EAB308; }
    </style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.title("🚕 Taxi Hotel")
    st.subheader("Iniciar sesión")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        r = supabase.table("usuarios").select("*").eq("usuario", usuario).eq("password", password).execute()
        if r.data:
            st.session_state.usuario = r.data[0]
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")
else:
    u = st.session_state.usuario
    st.success(f"👋 Bienvenido, {u['nombre']} ({u['rol']})")

    if u["rol"] == "admin":
        st.info("➡️ Ve al panel **Admin** en el menú lateral")
    elif u["rol"] == "recepcion":
        st.info("➡️ Ve al panel **Recepción** en el menú lateral")
    elif u["rol"] == "taxista":
        st.info("➡️ Ve al panel **Taxista** en el menú lateral")

    if st.button("Cerrar sesión"):
        del st.session_state.usuario
        st.rerun()