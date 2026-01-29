import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import time

# 1. CONFIGURACIÓN Y CSS RADICAL
st.set_page_config(page_title="Comedor Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0221 !important; }
    .block-container { padding: 0.5rem !important; }
    
    /* CONTENEDOR MANUAL PARA BOTONES EN FILA */
    .button-row {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 8px !important;
        margin-bottom: 15px !important;
        width: 100% !important;
    }

    /* ESTILO DE CADA BOTÓN DENTRO DE LA FILA */
    div.stButton > button {
        flex: 1 !important; /* Todos miden lo mismo */
        height: 55px !important;
        border-radius: 12px !important;
        background-color: #1a1a2e !important;
        color: white !important;
        border: 2px solid #5b21b6 !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }

    /* BOTÓN SELECCIONADO (ALUMBRA) */
    div.stButton > button[kind="primary"] {
        background-color: #7c3aed !important;
        box-shadow: 0 0 15px #7c3aed !important;
        border: 2px solid white !important;
    }

    /* BOTÓN REGISTRAR (GIGANTE Y FIJO ABAJO) */
    .btn-save-container button {
        background-color: #00c9b7 !important;
        height: 75px !important;
        font-size: 20px !important;
        border: 2px solid white !important;
        box-shadow: 0 0 20px rgba(0, 201, 183, 0.5) !important;
    }

    p, b { color: #00f2ff !important; margin-bottom: 5px !important; display: block; }
    </style>
    """, unsafe_allow_html=True)

# 2. MANEJO DE DATOS
archivo = "registro_comedor.csv"
if 's_a' not in st.session_state:
    st.session_state.update({'s_a': None, 's_s': None, 's_m': None, 'pagina': 'registro'})

def cargar_datos():
    if os.path.exists(archivo):
        try: return pd.read_csv(archivo)
        except: return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])
    return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])

# 3. VISTA DE REGISTRO
if st.session_state.pagina == "registro":
    st.markdown("<h3 style='text-align:center; color:#00f2ff;'>🍴 PANEL DE REGISTRO</h3>", unsafe_allow_html=True)
    
    # Switches de arriba
    col_t = st.columns(2)
    with col_t[0]: fijar = st.toggle("📌 Fijar Datos")
    with col_t[1]: rep = st.checkbox("🔄 REPITIENTE")

    # GRADO / AÑO
    st.write("**GRADO / AÑO**")
    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    ca = st.columns(3)
    for i, opt in enumerate(["1ERO", "2DO", "3ERO"]):
        if ca[i].button(opt, key=f"a_{opt}", type="primary" if st.session_state.s_a == opt else "secondary"):
            st.session_state.s_a = opt; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # SECCIÓN
    st.write("**SECCIÓN**")
    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    cs = st.columns(3)
    for i, opt in enumerate(["A", "B", "C"]):
        if cs[i].button(opt, key=f"s_{opt}", type="primary" if st.session_state.s_s == opt else "secondary"):
            st.session_state.s_s = opt; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # MENCIÓN (Distribución 2 y 2)
    st.write("**MENCIÓN**")
    m1 = st.columns(2)
    opts_m = ["Química", "Electr."]
    for i, opt in enumerate(opts_m):
        if m1[i].button(opt, key=f"m_{opt}", type="primary" if st.session_state.s_m == opt else "secondary"):
            st.session_state.s_m = opt; st.rerun()
    
    m2 = st.columns(2)
    opts_m2 = ["Turismo", "Adm."]
    for i, opt in enumerate(opts_m2):
        if m2[i].button(opt, key=f"m2_{opt}", type="primary" if st.session_state.s_m == opt else "secondary"):
            st.session_state.s_m = opt; st.rerun()

    # BOTÓN REGISTRAR (El gran botón verde de la foto)
    st.markdown('<div class="btn-save-container">', unsafe_allow_html=True)
    if st.button("✅ REGISTRAR ESTUDIANTE", use_container_width=True):
        if all([st.session_state.s_a, st.session_state.s_s, st.session_state.s_m]):
            nuevo = {"ID": str(uuid.uuid4())[:8], "Año": st.session_state.s_a, "Seccion": st.session_state.s_s, "Mencion": st.session_state.s_m, "Repitiente": rep, "Hora": datetime.now().strftime("%H:%M")}
            df = cargar_datos()
            pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True).to_csv(archivo, index=False)
            st.toast("¡Guardado!", icon='🔥')
            if not fijar: st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
            time.sleep(0.3); st.rerun()
        else:
            st.warning("Selecciona Grado, Sección y Mención")
    st.markdown('</div>', unsafe_allow_html=True)

    # RESUMEN (CUADROS ABAJO)
    df_hoy = cargar_datos()
    if not df_hoy.empty:
        st.write("---")
        res = df_hoy.groupby(["Año", "Seccion", "Mencion"]).size().reset_index(name='n')
        for _, r in res.iterrows():
            if st.button(f"📊 {r['Año']} {r['Seccion']} {r['Mencion']} ({r['n']})", key=f"res_{uuid.uuid4()}", use_container_width=True):
                st.session_state.sec_activa = r.to_dict(); st.session_state.pagina = "detalle"; st.rerun()
