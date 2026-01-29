import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import time

# Configuración inicial para móvil
st.set_page_config(page_title="Comedor Pro", layout="centered")

# CSS Avanzado para feedback visual
st.markdown("""
    <style>
    .stApp { background-color: #0d0221 !important; }
    
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* Efecto de botones: Al tocar se encogen */
    div.stButton > button:active {
        transform: scale(0.95);
        transition: 0.1s;
    }

    div.stButton > button { 
        width: 100%; height: 60px !important; border-radius: 10px; 
        font-size: 16px !important; font-weight: bold;
        border: 2px solid #5b21b6 !important;
        background-color: #1a1a2e !important; color: #ffffff !important;
        transition: all 0.2s;
    }

    /* Botón seleccionado (Alumbra) */
    .stButton button[kind="primary"] { 
        background-color: #7c3aed !important; 
        box-shadow: 0 0 20px #7c3aed;
        border: 2px solid #ffffff !important;
    }
    
    /* Botón GUARDAR: Feedback de éxito */
    .btn-save button {
        background-color: #059669 !important; height: 80px !important;
        font-size: 22px !important; border: 2px solid #ffffff !important;
        box-shadow: 0 4px 15px rgba(5, 150, 105, 0.4);
    }
    
    .btn-save button:active {
        background-color: #10b981 !important;
        box-shadow: 0 0 30px #10b981;
    }

    p, b, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
archivo = "registro_comedor.csv"
def cargar_datos():
    if os.path.exists(archivo):
        try: return pd.read_csv(archivo)
        except: return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])
    return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])

if 's_a' not in st.session_state:
    st.session_state.update({'s_a': None, 's_s': None, 's_m': None, 'pagina': 'registro'})

# --- VISTA DE REGISTRO ---
if st.session_state.pagina == "registro":
    st.markdown("<h2 style='text-align:center; color:#00f2ff; margin:0;'>🍴 PANEL REGISTRO</h2>", unsafe_allow_html=True)
    
    c_f1, c_f2 = st.columns(2)
    with c_f1: fijar = st.toggle("📌 FIJAR", value=False)
    with c_f2: rep = st.checkbox("🔄 REPITIENTE", value=False)

    # AÑO
    st.write("---")
    ca1, ca2, ca3 = st.columns(3)
    for i, opt in enumerate(["1ERO", "2DO", "3ERO"]):
        if [ca1, ca2, ca3][i].button(opt, key=f"a_{opt}", type="primary" if st.session_state.s_a == opt else "secondary"):
            st.session_state.s_a = None if st.session_state.s_a == opt else opt
            st.rerun()

    # SECCIÓN
    cs1, cs2, cs3 = st.columns(3)
    for i, opt in enumerate(["A", "B", "C"]):
        if [cs1, cs2, cs3][i].button(opt, key=f"s_{opt}", type="primary" if st.session_state.s_s == opt else "secondary"):
            st.session_state.s_s = None if st.session_state.s_s == opt else opt
            st.rerun()

    # MENCIÓN
    cm1, cm2 = st.columns(2)
    menciones = ["Química", "Elect.", "Turismo", "Adm."]
    for i, opt in enumerate(menciones):
        if [cm1, cm2][i%2].button(opt, key=f"m_{opt}", type="primary" if st.session_state.s_m == opt else "secondary"):
            st.session_state.s_m = None if st.session_state.s_m == opt else opt
            st.rerun()

    # BOTÓN GUARDAR CON FEEDBACK
    st.write("")
    if all([st.session_state.s_a, st.session_state.s_s, st.session_state.s_m]):
        st.markdown('<div class="btn-save">', unsafe_allow_html=True)
        if st.button("✅ REGISTRAR AHORA", use_container_width=True):
            # Lógica de guardado
            nuevo = {
                "ID": str(uuid.uuid4())[:8], "Año": st.session_state.s_a, 
                "Seccion": st.session_state.s_s, "Mencion": st.session_state.s_m, 
                "Repitiente": rep, "Hora": datetime.now().strftime("%H:%M")
            }
            df = cargar_datos()
            pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True).to_csv(archivo, index=False)
            
            # Feedback Visual: Toast + Destello
            st.toast(f"✅ ¡{st.session_state.s_a} {st.session_state.s_s} Guardado!", icon='🔥')
            
            if not fijar:
                st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
            
            time.sleep(0.4) # Breve pausa para que veas el "click"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.button("⚠️ SELECCIONE TODO", disabled=True)

    # Footer compacto
    df_h = cargar_datos()
    st.markdown(f"<p style='text-align:center; opacity:0.7;'>Total hoy: {len(df_h)}</p>", unsafe_allow_html=True)
    if st.button("📂 VER LISTA COMPLETA"):
        st.session_state.pagina = "detalle"
        st.rerun()

elif st.session_state.pagina == "detalle":
    if st.button("⬅️ VOLVER AL REGISTRO"):
        st.session_state.pagina = "registro"
        st.rerun()
    st.write("### Historial de hoy")
    st.dataframe(cargar_datos(), use_container_width=True)
