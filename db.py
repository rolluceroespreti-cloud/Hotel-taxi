import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def get_secret(key):
    """Busca primero en variables de entorno (.env local) y luego en st.secrets (nube)."""
    valor = os.getenv(key)
    if valor:
        return valor
    try:
        return st.secrets[key]
    except Exception:
        return None

supabase = create_client(
    get_secret("SUPABASE_URL"),
    get_secret("SUPABASE_KEY")
)