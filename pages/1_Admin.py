import streamlit as st
from db import supabase

st.set_page_config(page_title="Admin", page_icon="⚙️")

# Protección: solo admin
if "usuario" not in st.session_state or st.session_state.usuario["rol"] != "admin":
    st.error("⛔ Acceso restringido. Iniciá sesión como admin.")
    st.stop()

st.title("⚙️ Panel de Administración")

tab1, tab2 = st.tabs(["🚕 Taxis", "💰 Tarifas"])

# ---------- TAXIS ----------
with tab1:
    st.subheader("Agregar taxi")
    with st.form("form_taxi"):
        nombre = st.text_input("Nombre del taxista")
        telefono = st.text_input("Teléfono")
        patente = st.text_input("Patente")
        if st.form_submit_button("Guardar taxi"):
            if nombre:
                supabase.table("taxis").insert({
                    "nombre": nombre,
                    "telefono": telefono,
                    "patente": patente,
                    "activo": True,
                }).execute()
                st.success(f"Taxi '{nombre}' agregado")
                st.rerun()
            else:
                st.warning("El nombre es obligatorio")

    st.divider()
    st.subheader("Taxis registrados")
    taxis = supabase.table("taxis").select("*").order("id").execute().data
    if taxis:
        st.dataframe(taxis, use_container_width=True)
    else:
        st.info("No hay taxis registrados todavía")

# ---------- TARIFAS ----------
with tab2:
    st.subheader("Agregar tarifa")
    with st.form("form_tarifa"):
        destino = st.text_input("Destino")
        precio = st.number_input("Precio", min_value=0.0, step=100.0)
        if st.form_submit_button("Guardar tarifa"):
            if destino:
                supabase.table("tarifas").insert({
                    "destino": destino,
                    "precio": precio,
                }).execute()
                st.success(f"Tarifa a '{destino}' agregada")
                st.rerun()
            else:
                st.warning("El destino es obligatorio")

    st.divider()
    st.subheader("Tarifas registradas")
    tarifas = supabase.table("tarifas").select("*").order("destino").execute().data
    if tarifas:
        st.dataframe(tarifas, use_container_width=True)
    else:
        st.info("No hay tarifas registradas todavía")