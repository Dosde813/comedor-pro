import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import time

# 1. CONFIGURACIÓN Y CSS ULTRA-COMPACTO
st.set_page_config(page_title="Comedor Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0221 !important; }
    
    /* Eliminar espacios vacíos extremos */
    .block-container { padding: 0.2rem 0.5rem !important; max-width: 100% !important; }
    header {visibility: hidden;}
    
    /* FORZAR COLUMNAS PEQUEÑAS EN UNA SOLA FILA */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
        margin-bottom: -15px !important; /* Pegar las filas entre sí */
    }
    
    [data-testid="column"] { flex: 1 !important; min-width: 0 !important; }

    /* Botones de Selección Mini */
    div.stButton > button { 
        width: 100% !important; 
        height: 40px !important; /* Más bajos para que quepan */
        border-radius: 8px; 
        background-color: #1a1a2e !important; 
        color: white !important;
        border: 1px solid #5b21b6 !important;
        font-size: 12px !important;
        padding: 0 !important;
    }
    
    /* Alumbrar selección */
    .stButton button[kind="primary"] { 
        background-color: #7c3aed !important; 
        box-shadow: 0 0 10px #7c3aed; border: 1px solid white !important;
    }

    /* BOTÓN REGISTRAR (Compacto pero llamativo) */
    .btn-save button {
        background-color: #00c9b7 !important; 
        height: 55px !important; 
        font-size: 16px !important;
        font-weight: bold !important;
        margin-top: 10px !important;
    }

    /* Textos muy pequeños */
    p, b, label { color: #00f2ff !important; font-size: 11px !important; margin: 0 !important; }
    h3 { font-size: 18px !important; margin-bottom: 5px !important; color: #00f2ff !important; text-align: center; }
    
    /* Ajuste de toggle y checkbox */
    .stCheckbox label, .stToggle label { font-size: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
archivo = "registro_comedor.csv"
if 'pagina' not in st.session_state:
    st.session_state.update({'s_a': None, 's_s': None, 's_m': None, 'pagina': 'registro'})

def cargar_datos():
    if os.path.exists(archivo):
        try: return pd.read_csv(archivo)
        except: return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])
    return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])

# 3. VISTA: REGISTRO (TODO EN UNA PANTALLA)
if st.session_state.pagina == "registro":
    st.markdown("<h3>🍴 COMEDOR</h3>", unsafe_allow_html=True)
    
    # Fila superior de opciones (muy juntas)
    c_top = st.columns(2)
    with c_top[0]: fijar = st.toggle("📌 Fijar", value=False)
    with c_top[1]: rep = st.checkbox("🔄 REP")

    # GRADO (En una sola fila horizontal)
    st.write("**AÑO**")
    ca = st.columns(3)
    for i, opt in enumerate(["1ERO", "2DO", "3ERO"]):
        if ca[i].button(opt, key=f"a_{opt}", type="primary" if st.session_state.s_a == opt else "secondary"):
            st.session_state.s_a = opt; st.rerun()

    # SECCIÓN (En una sola fila horizontal)
    st.write("**SECCIÓN**")
    cs = st.columns(3)
    for i, opt in enumerate(["A", "B", "C"]):
        if cs[i].button(opt, key=f"s_{opt}", type="primary" if st.session_state.s_s == opt else "secondary"):
            st.session_state.s_s = opt; st.rerun()

    # MENCIÓN (En una sola fila horizontal - Texto corto)
    st.write("**MENCIÓN**")
    cm = st.columns(4)
    menciones = ["QUIM", "ELEC", "TUR", "ADM"]
    for i, opt in enumerate(menciones):
        if cm[i].button(opt, key=f"m_{opt}", type="primary" if st.session_state.s_m == opt else "secondary"):
            st.session_state.s_m = opt; st.rerun()

    # BOTÓN REGISTRAR (Siempre visible al final)
    st.markdown('<div class="btn-save">', unsafe_allow_html=True)
    if st.button("✅ REGISTRAR AHORA", use_container_width=True):
        if all([st.session_state.s_a, st.session_state.s_s, st.session_state.s_m]):
            nuevo = {"ID": str(uuid.uuid4())[:8], "Año": st.session_state.s_a, "Seccion": st.session_state.s_s, "Mencion": st.session_state.s_m, "Repitiente": rep, "Hora": datetime.now().strftime("%H:%M")}
            df = cargar_datos()
            pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True).to_csv(archivo, index=False)
            st.toast("Guardado")
            if not fijar: st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
            time.sleep(0.2); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Mini historial
    df_h = cargar_datos()
    if not df_h.empty:
        st.markdown(f"<p style='text-align:center;'>Total hoy: {len(df_h)}</p>", unsafe_allow_html=True)
        if st.button("📂 VER LISTADO", use_container_width=True):
            st.session_state.pagina = "detalle"; st.rerun()
