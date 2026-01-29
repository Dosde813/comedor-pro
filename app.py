import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import time

# 1. CONFIGURACIÓN Y CSS "ESTILO FOTO"
st.set_page_config(page_title="Comedor Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0221 !important; }
    
    /* Eliminar espacios vacíos arriba y a los lados */
    .block-container { padding: 0.5rem !important; max-width: 100% !important; }
    
    /* Forzar que las filas no se rompan */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
    }
    
    div[data-testid="column"] { flex: 1 !important; min-width: 0 !important; }

    /* Botones de Selección (Estilo Neón) */
    div.stButton > button { 
        width: 100% !important; height: 50px !important; border-radius: 12px; 
        background-color: #1a1a2e !important; color: white !important;
        border: 2px solid #5b21b6 !important; font-size: 14px !important;
        font-weight: bold !important;
    }
    
    /* Botón Seleccionado (Alumbra) */
    .stButton button[kind="primary"] { 
        background-color: #7c3aed !important; 
        box-shadow: 0 0 15px #7c3aed; border: 2px solid white !important;
    }

    /* BOTÓN REGISTRAR (Verde Neón, grande y llamativo como la foto) */
    .btn-save button {
        background-color: #00c9b7 !important; color: white !important;
        height: 70px !important; font-size: 18px !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 20px rgba(0, 201, 183, 0.5) !important;
        margin-top: 10px !important;
    }

    /* Estilo de Etiquetas */
    p, b { color: #00f2ff !important; font-size: 14px !important; margin-bottom: 2px !important; }
    
    /* Resúmenes (Cuadritos de abajo) */
    .res-card {
        background: rgba(0, 242, 255, 0.1);
        border: 1px solid #00f2ff;
        padding: 8px; border-radius: 8px; margin-top: 5px;
    }
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

# 3. VISTA: REGISTRO
if st.session_state.pagina == "registro":
    st.markdown("<h3 style='text-align:center; color:#00f2ff; margin-top:0;'>🍴 REGISTRO COMEDOR</h3>", unsafe_allow_html=True)
    
    # Switches compactos
    c_top = st.columns(2)
    with c_top[0]: fijar = st.toggle("📌 Fijar Datos")
    with c_top[1]: rep = st.checkbox("🔄 REPITIENTE")

    # GRADO
    st.write("**GRADO / AÑO**")
    ca = st.columns(3)
    for i, opt in enumerate(["1ERO", "2DO", "3ERO"]):
        if ca[i].button(opt, key=f"a_{opt}", type="primary" if st.session_state.s_a == opt else "secondary"):
            st.session_state.s_a = opt
            st.rerun()

    # SECCIÓN
    st.write("**SECCIÓN**")
    cs = st.columns(3)
    for i, opt in enumerate(["A", "B", "C"]):
        if cs[i].button(opt, key=f"s_{opt}", type="primary" if st.session_state.s_s == opt else "secondary"):
            st.session_state.s_s = opt
            st.rerun()

    # MENCIÓN (2x2 para ahorrar espacio vertical)
    st.write("**MENCIÓN**")
    cm1, cm2 = st.columns(2)
    menciones = ["Química", "Electr.", "Turismo", "Adm."]
    for i, opt in enumerate(menciones):
        col = cm1 if i < 2 else cm2
        if col.button(opt, key=f"m_{opt}", type="primary" if st.session_state.s_m == opt else "secondary"):
            st.session_state.s_m = opt
            st.rerun()

    # BOTÓN REGISTRAR (Justo debajo de las menciones)
    st.markdown('<div class="btn-save">', unsafe_allow_html=True)
    if st.button("✅ REGISTRAR ESTUDIANTE", use_container_width=True):
        if all([st.session_state.s_a, st.session_state.s_s, st.session_state.s_m]):
            nuevo = {"ID": str(uuid.uuid4())[:8], "Año": st.session_state.s_a, "Seccion": st.session_state.s_s, "Mencion": st.session_state.s_m, "Repitiente": rep, "Hora": datetime.now().strftime("%H:%M")}
            df = cargar_datos()
            pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True).to_csv(archivo, index=False)
            st.toast("¡Guardado!", icon='🔥')
            if not fijar:
                st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
            time.sleep(0.3); st.rerun()
        else:
            st.warning("Selecciona todo primero")
    st.markdown('</div>', unsafe_allow_html=True)

    # RESUMEN RÁPIDO ABAJO
    df_h = cargar_datos()
    if not df_h.empty:
        st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
        res = df_h.groupby(["Año", "Seccion", "Mencion"]).size().reset_index(name='n')
        for _, r in res.iterrows():
            if st.button(f"📊 {r['Año']} {r['Seccion']} {r['Mencion']} ({r['n']})", key=f"r_{uuid.uuid4()}", use_container_width=True):
                st.session_state.sec_activa = r.to_dict()
                st.session_state.pagina = "detalle"; st.rerun()
