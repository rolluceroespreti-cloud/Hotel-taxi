import streamlit as st
from db import supabase

st.set_page_config(page_title="Taxi Hotel", page_icon="🚕", layout="centered")

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


def login():
    st.title("🚕 Taxi Hotel")
    st.subheader("Iniciar sesión")

    usuario = st.text_input("Usuario").strip()
    password = st.text_input("Contraseña", type="password").strip()

    if st.button("Ingresar"):
        if not usuario or not password:
            st.warning("Completá usuario y contraseña")
            return

        try:
            r = supabase.table("usuarios").select("*").eq("usuario", usuario).eq("password", password).execute()
        except Exception as e:
            st.error(f"Error consultando Supabase: {type(e).__name__}: {e}")
            return

        if r.data:
            st.session_state.usuario = r.data[0]
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")


def panel():
    u = st.session_state.usuario
    st.success(f"👋 Bienvenido, {u['nombre']} ({u['rol']})")

    if u["rol"] == "admin":
        st.info("➡️ Ve al panel **Admin** en el menú lateral")
    elif u["rol"] == "recepcion":
        st.info("➡️ Ve al panel **Recepción** en el menú lateral")
    elif u["rol"] == "taxista":
        st.info("➡️ Ve al panel **Taxista** en el menú lateral")

    st.divider()
    if st.button("🚪 Cerrar sesión"):
        del st.session_state.usuario
        st.rerun()


if "usuario" not in st.session_state:
    login()
else:
    panel()