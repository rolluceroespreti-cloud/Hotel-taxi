import streamlit as st
import os

st.title("🔧 Diagnóstico")

try:
    url = st.secrets["SUPABASE_URL"]
    st.success(f"✅ SUPABASE_URL: {url}")
except Exception as e:
    st.error(f"❌ SUPABASE_URL NO encontrada: {e}")

try:
    key = st.secrets["SUPABASE_KEY"]
    st.success(f"✅ SUPABASE_KEY: empieza con '{key[:20]}...' (longitud total: {len(key)})")
except Exception as e:
    st.error(f"❌ SUPABASE_KEY NO encontrada: {e}")

st.write("---")
st.write("**Variables de entorno (os.getenv):**")
st.write(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
st.write(f"SUPABASE_KEY: {os.getenv('SUPABASE_KEY')}")
