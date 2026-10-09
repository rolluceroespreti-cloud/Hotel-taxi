import streamlit as st
from db import supabase

st.set_page_config(page_title="Taxista", page_icon="🚖")

if "usuario" not in st.session_state or st.session_state.usuario["rol"] != "taxista":
    st.error("⛔ Acceso restringido a taxistas.")
    st.stop()

u = st.session_state.usuario
st.title(f"🚖 Panel de {u['nombre']}")

viajes = supabase.table("viajes").select("*").eq("taxista_username", u["nombre"]).order("id", desc=True).execute().data

if not viajes:
    st.info("No tenés viajes asignados todavía")
else:
    for v in viajes:
        st.markdown(f"### Viaje #{v['id']} — {v['pasajero']}")
        st.write(f"**Destino:** {v['destino']} · **Precio:** ${v['precio']}")
        st.write(f"**Hotel:** {v['hotel']} · **Hab:** {v['habitacion']}")
        st.write(f"**Estado actual:** `{v['estado']}`")

        col1, col2, col3 = st.columns(3)
        with col1:
            if v["estado"] == "asignado" and st.button("▶️ Aceptar / Iniciar", key=f"ini_{v['id']}"):
                supabase.table("viajes").update({"estado": "en_viaje"}).eq("id", v["id"]).execute()
                st.rerun()
        with col2:
            if v["estado"] == "en_viaje" and st.button("✅ Finalizar", key=f"fin_{v['id']}"):
                supabase.table("viajes").update({"estado": "finalizado"}).eq("id", v["id"]).execute()
                st.rerun()
        with col3:
            if v["estado"] not in ("finalizado", "cancelado") and st.button("❌ Cancelar", key=f"can_{v['id']}"):
                supabase.table("viajes").update({"estado": "cancelado"}).eq("id", v["id"]).execute()
                st.rerun()

        st.divider()