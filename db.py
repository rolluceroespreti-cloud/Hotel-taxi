import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

# Cargar .env solo si existe (en local). En Cloud no hay .env, no pasa nada.
load_dotenv()


def get_secret(key: str):
    """
    Prioridad:
      1) st.secrets  (Streamlit Cloud y también funciona en local si hay .streamlit/secrets.toml)
      2) variables de entorno (.env local)
    Devuelve el valor limpio (sin espacios ni saltos de línea) o None.
    """
    valor = None

    # 1) st.secrets primero
    try:
        valor = st.secrets[key]
    except Exception:
        valor = None

    # 2) fallback a .env
    if not valor:
        valor = os.getenv(key)

    if not valor:
        return None

    # Limpieza defensiva: quitar espacios, saltos de línea y comillas accidentales
    valor = str(valor).strip().strip('"').strip("'")

    return valor


SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")

# Validación temprana: si falta algo, error claro
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Faltan SUPABASE_URL o SUPABASE_KEY. "
        "En local revisá tu .env; en Streamlit Cloud revisá los Secrets."
    )

# Normalizar URL (sin barra final)
SUPABASE_URL = SUPABASE_URL.rstrip("/")

# Diagnóstico suave (no muestra la key completa)
print(f"[db.py] Conectando a Supabase: {SUPABASE_URL}")
print(f"[db.py] Key length: {len(SUPABASE_KEY)} | primeros 10: {SUPABASE_KEY[:10]}...")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)