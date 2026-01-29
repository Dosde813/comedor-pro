import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import time

# 1. AJUSTE DE PANTALLA Y RESOLUCIÓN
st.set_page_config(page_title="Comedor Pro", layout="centered")

st.markdown("""
    <style>
    /* Fondo y Reset de Espacios */
    .stApp { background-color: #0d0221 !important; }
    .block-container { 
        padding: 1rem !important; 
        max-width: 100% !important; 
    }
    
    /* FUERZA EL AJUSTE AL ANCHO DEL TELÉFONO (Sin scroll horizontal) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 5px !important; /* Espacio mínimo entre botones */
    }
    
    /* Cada columna ocupa el espacio justo (1/3 para Grados, 1/3 para Secciones) */
    [data-testid="column"] {
        flex: 1 !important;
        min-width: 0 !important;
    }

    /* Estilo de Botones (Grandes y Táctiles) */
    div.stButton > button { 
        width: 100% !important; 
        height: 60px !important; 
        border-radius: 8px; 
        background-color: #1a1a2e !important; 
        color: white !important;
        border: 2px solid #5b21b6 !important;
        font-size: 15px !important;
        padding: 0px !important;
    }
    
    /* Alumbrar botón seleccionado */
    .stButton button[kind="primary"] { 
        background-color: #7c3aed !important; 
        box-shadow: 0 0 15px #7c3aed; 
        border: 2px solid white !important;
    }

    /* Botón Guardar (Ocupa todo el ancho) */
    .btn-save button {
        background-color: #059669 !important; 
        height: 80px !important;
        font-size: 20px !important;
        margin-top: 10px !important;
    }
    
    p, b { color: white !important; margin: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
archivo = "registro_comedor.csv"
if 's_a' not in st.session_state:
    st.session_state.update({'s_a': None, 's_s': None, 's_m': None, 'pagina': 'registro', 'sec_activa': None})

def cargar_datos():
    if os.path.exists(archivo):
        try: return pd.read_csv(archivo)
        except: return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])
    return pd.DataFrame(columns=["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"])

# 3. VISTA: REGISTRO (Optimizado para 1080px de ancho)
if st.session_state.pagina == "registro":
    st.markdown("<h2 style='text-align:center; color:#00f2ff;'>🍴 REGISTRO</h2>", unsafe_allow_html=True)
    
    # Fila de Toggle y Checkbox
    c_op = st.columns(2)
    with c_op[0]: fijar = st.toggle("📌 Fijar")
    with c_op[1]: rep = st.checkbox("🔄 REP")

    # GRADOS (Repartidos en el ancho de la pantalla)
    st.write("**AÑO**")
    ca = st.columns(3)
    for i, opt in enumerate(["1ERO", "2DO", "3ERO"]):
        if ca[i].button(opt, key=f"a_{opt}", type="primary" if st.session_state.s_a == opt else "secondary"):
            st.session_state.s_a = None if st.session_state.s_a == opt else opt
            st.rerun()

    # SECCIONES (Repartidas en el ancho de la pantalla)
    st.write("**SECCIÓN**")
    cs = st.columns(3)
    for i, opt in enumerate(["A", "B", "C"]):
        if cs[i].button(opt, key=f"s_{opt}", type="primary" if st.session_state.s_s == opt else "secondary"):
            st.session_state.s_s = None if st.session_state.s_s == opt else opt
            st.rerun()

    # MENCIONES (2 y 2 para aprovechar el espacio)
    st.write("**MENCIÓN**")
    cm = st.columns(2)
    menciones = ["Química", "Elect.", "Turismo", "Adm."]
    for i, opt in enumerate(menciones):
        if cm[i%2].button(opt, key=f"m_{opt}", type="primary" if st.session_state.s_m == opt else "secondary"):
            st.session_state.s_m = None if st.session_state.s_m == opt else opt
            st.rerun()

    # GUARDAR
    if all([st.session_state.s_a, st.session_state.s_s, st.session_state.s_m]):
        st.markdown('<div class="btn-save">', unsafe_allow_html=True)
        if st.button("✅ GUARDAR REGISTRO", use_container_width=True):
            nuevo = {"ID": str(uuid.uuid4())[:8], "Año": st.session_state.s_a, "Seccion": st.session_state.s_s, "Mencion": st.session_state.s_m, "Repitiente": rep, "Hora": datetime.now().strftime("%H:%M")}
            df = cargar_datos()
            pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True).to_csv(archivo, index=False)
            st.toast("¡Guardado!", icon='✅')
            if not fijar: st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
            time.sleep(0.3); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # RESÚMENES (Los cuadros de secciones que pediste)
    df_hoy = cargar_datos()
    if not df_hoy.empty:
        st.divider()
        st.write("### 📂 SECCIONES HOY")
        res = df_hoy.groupby(["Año", "Seccion", "Mencion"]).size().reset_index(name='n')
        res = res.sort_values(["Año", "Seccion"])

        for _, r in res.iterrows():
            txt = f"{r['Año']} {r['Seccion']} {r['Mencion']} -> {r['n']} Est."
            if st.button(txt, key=f"res_{uuid.uuid4()}", use_container_width=True):
                st.session_state.sec_activa = r.to_dict()
                st.session_state.pagina = "detalle"
                st.rerun()

# 4. VISTA: DETALLE
elif st.session_state.pagina == "detalle":
    if st.button("⬅️ VOLVER"):
        st.session_state.pagina = "registro"
        st.rerun()
    
    sel = st.session_state.sec_activa
    st.subheader(f"Lista: {sel['Año']} {sel['Seccion']}")
    df = cargar_datos()
    lista = df[(df['Año'] == sel['Año']) & (df['Seccion'] == sel['Seccion']) & (df['Mencion'] == sel['Mencion'])]

    for i, r in lista.iterrows():
        c1, c2 = st.columns([4, 1])
        c1.write(f"**{r['Hora']}** | {'⚠️ REP' if r['Repitiente'] else '👤 OK'}")
        if c2.button("🗑️", key=f"del_{r['ID']}"):
            df.drop(i).to_csv(archivo, index=False)
            st.rerun()
