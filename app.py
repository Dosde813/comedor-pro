import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import time

# 1. CONFIGURACIÓN Y CSS PARA ENCUADRE PERFECTO
st.set_page_config(page_title="Comedor Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0221 !important; }
    
    /* Eliminar márgenes laterales para ganar espacio */
    .block-container { 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important; 
        max-width: 100% !important; 
    }

    /* CONTENEDOR DE BOTONES: Los obliga a repartirse el 100% del ancho */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* No se salen, se ajustan */
        width: 100% !important;
        gap: 8px !important;
    }
    
    /* Asegura que cada columna mida lo mismo y no se desplace */
    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0 !important;
    }

    /* Botones: Altura ergonómica (65px) y letra clara */
    div.stButton > button { 
        width: 100% !important; 
        height: 65px !important; 
        border-radius: 12px; 
        background-color: #1a1a2e !important; 
        color: white !important;
        border: 2px solid #5b21b6 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 0 !important;
    }
    
    /* Brillo Neón al seleccionar */
    .stButton button[kind="primary"] { 
        background-color: #7c3aed !important; 
        box-shadow: 0 0 20px #7c3aed; 
        border: 2px solid white !important;
    }

    /* Botón GUARDAR (Fácil de tocar al final) */
    .btn-save button {
        background-color: #059669 !important; 
        height: 85px !important;
        font-size: 22px !important;
        margin-top: 20px !important;
    }
    
    /* Cuadros de Secciones (Resumen abajo) */
    .resumen-btn button {
        height: auto !important;
        padding: 15px !important;
        text-align: left !important;
        border: 1px solid #06b6d4 !important;
        background: rgba(6, 182, 212, 0.1) !important;
    }

    p, b { color: white !important; font-size: 16px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
archivo = "registro_comedor.csv"
def cargar_datos():
    if os.path.exists(archivo):
        try: return pd.read_csv(archivo)
        except: return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])
    return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])

if 'pagina' not in st.session_state:
    st.session_state.update({'s_a': None, 's_s': None, 's_m': None, 'pagina': 'registro', 'sec_activa': None})

# 3. VISTA: REGISTRO
if st.session_state.pagina == "registro":
    st.markdown("<h2 style='text-align:center; color:#00f2ff;'>🍴 REGISTRO</h2>", unsafe_allow_html=True)
    
    # Opciones rápidas
    c_op = st.columns(2)
    with c_op[0]: fijar = st.toggle("📌 Fijar Datos")
    with c_op[1]: rep = st.checkbox("🔄 REPITIENTE")

    # FILA 1: GRADOS (1ERO | 2DO | 3ERO)
    st.write("**GRADO / AÑO**")
    ca = st.columns(3)
    for i, opt in enumerate(["1ERO", "2DO", "3ERO"]):
        if ca[i].button(opt, key=f"a_{opt}", type="primary" if st.session_state.s_a == opt else "secondary"):
            st.session_state.s_a = None if st.session_state.s_a == opt else opt
            st.rerun()

    # FILA 2: SECCIONES (A | B | C)
    st.write("**SECCIÓN**")
    cs = st.columns(3)
    for i, opt in enumerate(["A", "B", "C"]):
        if cs[i].button(opt, key=f"s_{opt}", type="primary" if st.session_state.s_s == opt else "secondary"):
            st.session_state.s_s = None if st.session_state.s_s == opt else opt
            st.rerun()

    # FILA 3: MENCIONES (2x2 para botones grandes)
    st.write("**MENCIÓN**")
    cm1, cm2 = st.columns(2)
    menciones = ["Química", "Elect.", "Turismo", "Adm."]
    for i, opt in enumerate(menciones):
        col = cm1 if i < 2 else cm2
        if col.button(opt, key=f"m_{opt}", type="primary" if st.session_state.s_m == opt else "secondary"):
            st.session_state.s_m = None if st.session_state.s_m == opt else opt
            st.rerun()

    # BOTÓN GUARDAR (Solo si está todo listo)
    if all([st.session_state.s_a, st.session_state.s_s, st.session_state.s_m]):
        st.markdown('<div class="btn-save">', unsafe_allow_html=True)
        if st.button("✅ REGISTRAR ESTUDIANTE", use_container_width=True):
            nuevo = {"ID": str(uuid.uuid4())[:8], "Año": st.session_state.s_a, "Seccion": st.session_state.s_s, "Mencion": st.session_state.s_m, "Repitiente": rep, "Hora": datetime.now().strftime("%H:%M")}
            df = cargar_datos()
            pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True).to_csv(archivo, index=False)
            st.toast("¡REGISTRADO!", icon='🔥')
            if not fijar: st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
            time.sleep(0.4); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 📊 CUADROS DE RESUMEN (Secciones acumuladas)
    df_h = cargar_datos()
    if not df_h.empty:
        st.markdown("<hr style='border: 1px solid #333;'>", unsafe_allow_html=True)
        st.write("### 📂 RESUMEN POR SECCIÓN")
        res = df_h.groupby(["Año", "Seccion", "Mencion"]).size().reset_index(name='n')
        res = res.sort_values(["Año", "Seccion"])

        for _, r in res.iterrows():
            if st.button(f"📍 {r['Año']} {r['Seccion']} {r['Mencion']} ({r['n']} Est.)", key=f"btn_{uuid.uuid4()}", use_container_width=True):
                st.session_state.sec_activa = r.to_dict()
                st.session_state.pagina = "detalle"
                st.rerun()

# 4. VISTA: DETALLE (Lo que hay dentro del cuadro)
elif st.session_state.pagina == "detalle":
    if st.button("⬅️ VOLVER AL PANEL"):
        st.session_state.pagina = "registro"
        st.rerun()
    
    sel = st.session_state.sec_activa
    st.subheader(f"Lista: {sel['Año']} {sel['Seccion']}")
    
    df = cargar_datos()
    lista = df[(df['Año'] == sel['Año']) & (df['Seccion'] == sel['Seccion']) & (df['Mencion'] == sel['Mencion'])]

    for i, r in lista.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"**{r['Hora']}** | {'⚠️ REPITIENTE' if r['Repitiente'] else '👤 REGULAR'}")
        if c2.button("🗑️", key=f"del_{r['ID']}"):
            df.drop(i).to_csv(archivo, index=False)
            st.rerun()
