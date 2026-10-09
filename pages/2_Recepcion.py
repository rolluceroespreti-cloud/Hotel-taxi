import streamlit as st
from db import supabase

st.set_page_config(page_title="Recepción", page_icon="🏨")

if "usuario" not in st.session_state or st.session_state.usuario["rol"] not in ("recepcion", "admin"):
    st.error("⛔ Acceso restringido.")
    st.stop()

st.title("🏨 Panel de Recepción")

# Cargar taxis y tarifas
taxis = supabase.table("taxis").select("*").eq("activo", True).execute().data
tarifas = supabase.table("tarifas").select("*").order("destino").execute().data

if not taxis:
    st.warning("⚠️ No hay taxis activos. Pedile al admin que agregue uno.")
if not tarifas:
    st.warning("⚠️ No hay tarifas. Pedile al admin que agregue una.")

with st.form("form_viaje"):
    st.subheader("Nuevo viaje")
    hotel = st.text_input("Hotel", value="Bros Lucero")
    habitacion = st.text_input("Habitación")
    pasajero = st.text_input("Pasajero")

    destinos = [t["destino"] for t in tarifas]
    destino = st.selectbox("Destino", destinos) if destinos else None

    if destino:
        precio_sugerido = next((t["precio"] for t in tarifas if t["destino"] == destino), 0.0)
    else:
        precio_sugerido = 0.0

    precio = st.number_input("Precio", value=float(precio_sugerido), step=100.0)

    opciones_taxi = {f"{t['nombre']} ({t.get('patente', 'sin patente')})": t["id"] for t in taxis}
    taxi_label = st.selectbox("Asignar taxista", list(opciones_taxi.keys())) if opciones_taxi else None

    if st.form_submit_button("Crear viaje"):
        if not pasajero or not destino or not taxi_label:
            st.warning("Completá pasajero, destino y taxista")
        else:
            taxi_id = opciones_taxi[taxi_label]
            taxi_data = next(t for t in taxis if t["id"] == taxi_id)
            supabase.table("viajes").insert({
                "hotel": hotel,
                "habitacion": habitacion,
                "pasajero": pasajero,
                "destino": destino,
                "precio": precio,
                "taxi_id": taxi_id,
                "taxista_username": taxi_data["nombre"],
                "estado": "asignado",
                "cobrado": False,
                "creado_por": st.session_state.usuario["usuario"],
            }).execute()
            st.success("✅ Viaje creado y asignado")
            st.rerun()

st.divider()
st.subheader("Viajes de hoy sin cobrar")
viajes = supabase.table("viajes").select("*").eq("cobrado", False).order("id", desc=True).execute().data

if viajes:
    for v in viajes:
        with st.expander(f"#{v['id']} · {v['pasajero']} → {v['destino']} · {v['estado']}"):
            st.write(f"**Hotel:** {v['hotel']} · **Hab:** {v['habitacion']}")
            st.write(f"**Taxista:** {v.get('taxista_username', '-')}")
            st.write(f"**Precio:** ${v['precio']}")
            if st.button(f"💵 Marcar como cobrado", key=f"cobrar_{v['id']}"):
                supabase.table("viajes").update({"cobrado": True}).eq("id", v["id"]).execute()
                st.success("Marcado como cobrado")
                st.rerun()
else:
    st.info("No hay viajes pendientes de cobro")