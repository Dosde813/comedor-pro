import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import time

# 1. CONFIGURACIÓN Y FORZADO DE DISEÑO HORIZONTAL EN MÓVIL
st.set_page_config(page_title="Comedor Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0221 !important; }
    .block-container { padding-top: 1rem !important; }
    
    /* FORZAR COLUMNAS EN MÓVIL: Esto evita que los botones se pongan uno abajo de otro */
    [data-testid="column"] {
        width: calc(33% - 1rem) !important;
        flex: 1 1 calc(33% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }

    /* Botones de Selección */
    div.stButton > button { 
        width: 100%; height: 55px !important; border-radius: 10px; 
        background-color: #1a1a2e !important; color: white !important;
        border: 2px solid #5b21b6 !important; font-size: 14px !important;
    }
    
    /* Efecto Alumbrar (Morado Neón) */
    .stButton button[kind="primary"] { 
        background-color: #7c3aed !important; 
        box-shadow: 0 0 15px #7c3aed; border: 2px solid white !important;
    }

    /* Botón GUARDAR (Verde) */
    .btn-save button {
        background-color: #059669 !important; height: 75px !important;
        font-size: 18px !important; border: 2px solid white !important;
    }

    /* Botón BORRAR TODO (Rojo) */
    .btn-delete-all button {
        background-color: #b91c1c !important; color: white !important;
        border: 1px solid white !important; height: 45px !important;
    }

    p, b, label { color: white !important; font-size: 14px !important; margin: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
archivo = "registro_comedor.csv"
def cargar_datos():
    if os.path.exists(archivo):
        try: return pd.read_csv(archivo)
        except: return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])
    return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])

if 's_a' not in st.session_state:
    st.session_state.update({'s_a': None, 's_s': None, 's_m': None, 'pagina': 'registro'})

# 3. VISTA: REGISTRO
if st.session_state.pagina == "registro":
    st.markdown("<h3 style='text-align:center; color:#00f2ff; margin-bottom:10px;'>🍴 REGISTRO</h3>", unsafe_allow_html=True)
    
    c_top1, c_top2 = st.columns(2)
    with c_top1: fijar = st.toggle("📌 Fijar", value=False)
    with c_top2: rep = st.checkbox("🔄 REP", value=False)

    # GRADOS (1ero, 2do, 3ero en una sola línea)
    st.write("**AÑO**")
    ca1, ca2, ca3 = st.columns(3)
    for i, opt in enumerate(["1ERO", "2DO", "3ERO"]):
        if [ca1, ca2, ca3][i].button(opt, key=f"a_{opt}", type="primary" if st.session_state.s_a == opt else "secondary"):
            st.session_state.s_a = None if st.session_state.s_a == opt else opt
            st.rerun()

    # SECCIONES (A, B, C en una sola línea)
    st.write("**SECCIÓN**")
    cs1, cs2, cs3 = st.columns(3)
    for i, opt in enumerate(["A", "B", "C"]):
        if [cs1, cs2, cs3][i].button(opt, key=f"s_{opt}", type="primary" if st.session_state.s_s == opt else "secondary"):
            st.session_state.s_s = None if st.session_state.s_s == opt else opt
            st.rerun()

    # MENCIONES (2 y 2)
    st.write("**MENCIÓN**")
    cm1, cm2 = st.columns(2)
    menciones = ["Química", "Elect.", "Turismo", "Adm."]
    for i, opt in enumerate(menciones):
        if [cm1, cm2][i%2].button(opt, key=f"m_{opt}", type="primary" if st.session_state.s_m == opt else "secondary"):
            st.session_state.s_m = None if st.session_state.s_m == opt else opt
            st.rerun()

    # BOTÓN GUARDAR (Solo aparece si seleccionaste todo)
    if all([st.session_state.s_a, st.session_state.s_s, st.session_state.s_m]):
        st.markdown('<div class="btn-save" style="margin-top:15px;">', unsafe_allow_html=True)
        if st.button("✅ GUARDAR REGISTRO", use_container_width=True):
            nuevo = {"ID": str(uuid.uuid4())[:8], "Año": st.session_state.s_a, "Seccion": st.session_state.s_s, "Mencion": st.session_state.s_m, "Repitiente": rep, "Hora": datetime.now().strftime("%H:%M")}
            df = cargar_datos()
            pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True).to_csv(archivo, index=False)
            st.toast("¡Guardado!", icon='✅')
            if not fijar: st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
            time.sleep(0.3); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # TOTALES Y BOTONES DE ABAJO
    df_h = cargar_datos()
    st.markdown(f"<p style='text-align:center; margin-top:10px;'>Total: {len(df_h)}</p>", unsafe_allow_html=True)
    
    c_bot1, c_bot2 = st.columns(2)
    with c_bot1:
        if st.button("📂 VER LISTA"): st.session_state.pagina = "detalle"; st.rerun()
    with c_bot2:
        st.markdown('<div class="btn-delete-all">', unsafe_allow_html=True)
        if st.button("🗑️ BORRAR"):
            pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"]).to_csv(archivo, index=False)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "detalle":
    if st.button("⬅️ VOLVER"): st.session_state.pagina = "registro"; st.rerun()
    st.write("### Registros")
    st.dataframe(cargar_datos(), use_container_width=True)
