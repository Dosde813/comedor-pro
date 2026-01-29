import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import time

# 1. CONFIGURACIÓN Y CSS RADICAL (FORZADO HORIZONTAL)
st.set_page_config(page_title="Comedor Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0221 !important; }
    
    /* ESTO FUERZA LAS COLUMNAS */
    [data-testid="column"] {
        display: flex !important;
        flex-direction: row !important;
        width: 33% !important;
        min-width: 33% !important;
    }
    
    /* Ajuste para que los botones llenen el espacio */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        border-radius: 12px;
        background-color: #1a1a2e !important;
        color: #00f2ff !important;
        border: 2px solid #5b21b6 !important;
        font-weight: bold !important;
        margin: 0 !important;
    }

    /* Botón seleccionado con Brillo Neón */
    div.stButton > button[kind="primary"] {
        background-color: #7c3aed !important;
        box-shadow: 0 0 20px #7c3aed;
        border: 2px solid white !important;
        color: white !important;
    }

    /* Botón Registrar Grande */
    .btn-registrar button {
        background-color: #00c9b7 !important;
        height: 75px !important;
        color: black !important;
        font-size: 20px !important;
        margin-top: 20px !important;
    }

    p, b { color: #00f2ff !important; font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
archivo = "registro_comedor.csv"
if 's_a' not in st.session_state:
    st.session_state.update({'s_a': None, 's_s': None, 's_m': None})

def cargar_datos():
    if os.path.exists(archivo):
        return pd.read_csv(archivo)
    return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])

# 3. INTERFAZ
st.markdown("<h2 style='text-align:center; color:#00f2ff;'>🍴 REGISTRO</h2>", unsafe_allow_html=True)

col_t = st.columns(2)
with col_t[0]: fijar = st.toggle("📌 Fijar")
with col_t[1]: rep = st.checkbox("🔄 REP")

# --- GRADO / AÑO (HORIZONTAL) ---
st.write("**GRADO / AÑO**")
c1, c2, c3 = st.columns(3)
with c1: 
    if st.button("1ERO", key="a1", type="primary" if st.session_state.s_a == "1ERO" else "secondary"):
        st.session_state.s_a = "1ERO"; st.rerun()
with c2: 
    if st.button("2DO", key="a2", type="primary" if st.session_state.s_a == "2DO" else "secondary"):
        st.session_state.s_a = "2DO"; st.rerun()
with c3: 
    if st.button("3ERO", key="a3", type="primary" if st.session_state.s_a == "3ERO" else "secondary"):
        st.session_state.s_a = "3ERO"; st.rerun()

# --- SECCIÓN (HORIZONTAL) ---
st.write("**SECCIÓN**")
s1, s2, s3 = st.columns(3)
with s1: 
    if st.button("A", key="sA", type="primary" if st.session_state.s_s == "A" else "secondary"):
        st.session_state.s_s = "A"; st.rerun()
with s2: 
    if st.button("B", key="sB", type="primary" if st.session_state.s_s == "B" else "secondary"):
        st.session_state.s_s = "B"; st.rerun()
with s3: 
    if st.button("C", key="sC", type="primary" if st.session_state.s_s == "C" else "secondary"):
        st.session_state.s_s = "C"; st.rerun()

# --- MENCIÓN (HORIZONTAL) ---
st.write("**MENCIÓN**")
m1, m2 = st.columns(2)
with m1:
    if st.button("QUÍMICA", key="mQ", type="primary" if st.session_state.s_m == "QUÍMICA" else "secondary"):
        st.session_state.s_m = "QUÍMICA"; st.rerun()
with m2:
    if st.button("ELECTR.", key="mE", type="primary" if st.session_state.s_m == "ELECTR." else "secondary"):
        st.session_state.s_m = "ELECTR."; st.rerun()

# BOTÓN FINAL
st.markdown('<div class="btn-registrar">', unsafe_allow_html=True)
if st.button("✅ REGISTRAR ESTUDIANTE", use_container_width=True):
    if all([st.session_state.s_a, st.session_state.s_s, st.session_state.s_m]):
        nuevo = {"ID": str(uuid.uuid4())[:8], "Año": st.session_state.s_a, "Seccion": st.session_state.s_s, "Mencion": st.session_state.s_m, "Repitiente": rep, "Hora": datetime.now().strftime("%H:%M")}
        df = cargar_datos()
        pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True).to_csv(archivo, index=False)
        st.toast("¡Guardado!")
        if not fijar: st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
        time.sleep(0.5); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
