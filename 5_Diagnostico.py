import streamlit as st
import os

st.title("🔧 Diagnóstico")

# Ver st.secrets
try:
    url = st.secrets["SUPABASE_URL"]
    st.success(f"URL: {url[:40]}...")
except Exception as e:
    st.error(f"SUPABASE_URL NO encontrada: {e}")

try:
    key = st.secrets["SUPABASE_KEY"]
    st.success(f"KEY empieza con: {key[:20]}... (longitud: {len(key)})")
except Exception as e:
    st.error(f"SUPABASE_KEY NO encontrada: {e}")

# Ver variables de entorno
st.write("**Variables de entorno:**")
st.write(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")

# Probar conexión
from db import supabase
try:
    r = supabase.table("usuarios").select("*").execute()
    st.success(f"✅ Conexión OK. Usuarios encontrados: {len(r.data)}")
except Exception as e:
    st.error(f"❌ Error de conexión: {e}")
