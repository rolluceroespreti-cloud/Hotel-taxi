import streamlit as st
import pandas as pd
from db import supabase

st.set_page_config(page_title="Historial", page_icon="📊")

if "usuario" not in st.session_state:
    st.error("⛔ Iniciá sesión primero")
    st.stop()

st.title("📊 Historial de viajes")

viajes = supabase.table("viajes").select("*").order("id", desc=True).execute().data

if not viajes:
    st.info("No hay viajes registrados")
    st.stop()

df = pd.DataFrame(viajes)

# Filtros
col1, col2, col3 = st.columns(3)
with col1:
    filtro_estado = st.selectbox("Estado", ["(todos)"] + sorted(df["estado"].dropna().unique().tolist()))
with col2:
    filtro_taxista = st.selectbox("Taxista", ["(todos)"] + sorted(df["taxista_username"].dropna().unique().tolist()))
with col3:
    filtro_cobrado = st.selectbox("Cobrado", ["(todos)", "Sí", "No"])

if filtro_estado != "(todos)":
    df = df[df["estado"] == filtro_estado]
if filtro_taxista != "(todos)":
    df = df[df["taxista_username"] == filtro_taxista]
if filtro_cobrado == "Sí":
    df = df[df["cobrado"] == True]
elif filtro_cobrado == "No":
    df = df[df["cobrado"] == False]

st.dataframe(df, use_container_width=True)
st.write(f"Total: **{len(df)}** viajes · Facturado: **${df['precio'].fillna(0).sum():,.0f}**")

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Descargar CSV", csv, "historial_viajes.csv", "text/csv")