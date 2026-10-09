import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def get_secret(key: str):
    """Prioridad: st.secrets (nube) > .env (local)."""
    valor = None
    try:
        valor = st.secrets[key]
    except Exception:
        valor = None
    if not valor:
        valor = os.getenv(key)
    if not valor:
        return None
    return str(valor).strip().strip('"').strip("'")


SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY.")

SUPABASE_URL = SUPABASE_URL.rstrip("/")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)