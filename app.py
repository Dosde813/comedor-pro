import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import time

# 1. CONFIGURACIÓN Y CSS (EL LOOK EXACTO QUE PEDISTE)
st.set_page_config(page_title="Comedor Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0221 !important; }
    .block-container { padding: 0.5rem !important; max-width: 100% !important; }

    /* FUERZA LAS FILAS HORIZONTALES */
    .fuerza-fila {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 8px !important;
        margin-bottom: 15px !important;
    }

    .fuerza-fila-mencion {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 8px !important;
        margin-bottom: 15px !important;
    }

    /* ESTILO DE BOTONES */
    div.stButton > button {
        width: 100% !important;
        height: 55px !important;
        border-radius: 10px;
        background-color: #1a1a2e !important;
        color: white !important;
        border: 2px solid #5b21b6 !important;
        font-size: 15px !important;
        font-weight: bold !important;
    }

    /* BOTÓN SELECCIONADO (NEÓN) */
    div.stButton > button[kind="primary"] {
        background-color: #7c3aed !important;
        box-shadow: 0 0 15px #7c3aed;
        border: 2px solid white !important;
    }

    /* BOTÓN REGISTRAR */
    .btn-registrar button {
        background-color: #00c9b7 !important;
        height: 70px !important;
        font-size: 18px !important;
        box-shadow: 0 0 20px rgba(0, 201, 183, 0.6) !important;
        color: black !important;
    }

    p, b { color: #00f2ff !important; margin-bottom: 2px !important; font-size: 14px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS (Mantiene tu sistema de archivos)
archivo = "registro_comedor.csv"

if 's_a' not in st.session_state:
    st.session_state.update({'s_a': None, 's_s': None, 's_m': None, 'pagina': 'registro'})

def cargar_datos():
    if os.path.exists(archivo):
        try:
            return pd.read_csv(archivo)
        except:
            return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])
    return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])

# 3. INTERFAZ DE REGISTRO
if st.session_state.pagina == "registro":
    st.markdown("<h3 style='text-align:center; color:#00f2ff;'>🍴 REGISTRO RÁPIDO</h3>", unsafe_allow_html=True)
    
    col_t = st.columns(2)
    with col_t[0]:
        fijar = st.toggle("📌 Fijar Datos")
    with col_t[1]:
        rep = st.checkbox("🔄 REPITIENTE")

    # SECCIÓN: AÑO
    st.write("**AÑO**")
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

    # SECCIÓN: SECCIÓN
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

    # SECCIÓN: MENCIÓN
    st.write("**MENCIÓN**")
    m1, m2 = st.columns(2)
    with m1:
        if st.button("Química", key="mQ", type="primary" if st.session_state.s_m == "Química" else "secondary"):
            st.session_state.s_m = "Química"; st.rerun()
        if st.button("Turismo", key="mT", type="primary" if st.session_state.s_m == "Turismo" else "secondary"):
            st.session_state.s_m = "Turismo"; st.rerun()
    with m2:
        if st.button("Electr.", key="mE", type="primary" if st.session_state.s_m == "Electr." else "secondary"):
            st.session_state.s_m = "Electr."; st.rerun()
        if st.button("Adm.", key="mAD", type="primary" if st.session_state.s_m == "Adm." else "secondary"):
            st.session_state.s_m = "Adm."; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # BOTÓN REGISTRAR FINAL
    st.markdown('<div class="btn-registrar">', unsafe_allow_html=True)
    if st.button("✅ REGISTRAR ESTUDIANTE", use_container_width=True):
        if all([st.session_state.s_a, st.session_state.s_s, st.session_state.s_m]):
            nuevo = {
                "ID": str(uuid.uuid4())[:8], 
                "Año": st.session_state.s_a, 
                "Seccion": st.session_state.s_s, 
                "Mencion": st.session_state.s_m, 
                "Repitiente": rep, 
                "Hora": datetime.now().strftime("%H:%M")
            }
            df = cargar_datos()
            pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True).to_csv(archivo, index=False)
            st.toast("🚀 ¡Registro Guardado!", icon="✅")
            
            if not fijar:
                st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
            
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Faltan datos por seleccionar")
    st.markdown('</div>', unsafe_allow_html=True)

    # Vista previa rápida de registros de hoy
    if st.checkbox("Ver registros de hoy"):
        st.write(cargar_datos().tail(5))
