import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
import time

# 1. CONFIGURACIÓN Y CSS DE FUERZA BRUTA PARA MÓVIL
st.set_page_config(page_title="Comedor Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0d0221 !important; }
    
    /* FORZAR COLUMNAS HORIZONTALES EN CELULAR */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0 !important;
    }

    /* Botones Neón */
    div.stButton > button { 
        width: 100% !important; height: 55px !important; border-radius: 10px; 
        background-color: #1a1a2e !important; color: white !important;
        border: 2px solid #5b21b6 !important; font-size: 13px !important;
    }
    .stButton button[kind="primary"] { 
        background-color: #7c3aed !important; 
        box-shadow: 0 0 15px #7c3aed; border: 2px solid white !important;
    }

    /* Cuadritos de Resumen (Secciones) */
    .section-card {
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid #06b6d4;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 5px;
        color: white;
    }
    
    .btn-save button {
        background-color: #059669 !important; height: 75px !important;
        font-size: 18px !important; border: 2px solid white !important;
    }
    
    p, b, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE DATOS
archivo = "registro_comedor.csv"
cols_fijas = ["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"]

def cargar_datos():
    if os.path.exists(archivo):
        try: return pd.read_csv(archivo)
        except: return pd.DataFrame(columns=cols_fijas)
    return pd.DataFrame(columns=cols_fijas)

if 's_a' not in st.session_state:
    st.session_state.update({'s_a': None, 's_s': None, 's_m': None, 'pagina': 'registro', 'sec_activa': None})

def ir_a(p, d=None):
    st.session_state.pagina = p
    st.session_state.sec_activa = d
    st.rerun()

# 3. VISTA: REGISTRO
if st.session_state.pagina == "registro":
    st.markdown("<h3 style='text-align:center; color:#00f2ff;'>🍴 REGISTRO</h3>", unsafe_allow_html=True)
    
    col_top = st.columns(2)
    with col_top[0]: fijar = st.toggle("📌 Fijar", value=False)
    with col_top[1]: rep = st.checkbox("🔄 REP", value=False)

    # BOTONES HORIZONTALES (AÑO)
    st.write("**AÑO**")
    ca = st.columns(3)
    for i, opt in enumerate(["1ERO", "2DO", "3ERO"]):
        if ca[i].button(opt, key=f"a_{opt}", type="primary" if st.session_state.s_a == opt else "secondary"):
            st.session_state.s_a = None if st.session_state.s_a == opt else opt
            st.rerun()

    # BOTONES HORIZONTALES (SECCIÓN)
    st.write("**SECCIÓN**")
    cs = st.columns(3)
    for i, opt in enumerate(["A", "B", "C"]):
        if cs[i].button(opt, key=f"s_{opt}", type="primary" if st.session_state.s_s == opt else "secondary"):
            st.session_state.s_s = None if st.session_state.s_s == opt else opt
            st.rerun()

    # BOTONES (MENCIÓN - 2 y 2)
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

    # 📊 RESÚMENES POR SECCIÓN (Los cuadritos que pediste)
    df_hoy = cargar_datos()
    if not df_hoy.empty:
        st.divider()
        st.write("### 📂 SECCIONES HOY")
        
        # Agrupamos y ordenamos
        res = df_hoy.groupby(["Año", "Seccion", "Mencion"]).size().reset_index(name='n')
        res = res.sort_values(["Año", "Seccion"])

        for _, r in res.iterrows():
            # Botón que parece un cuadro de resumen
            label = f"{r['Año']} {r['Seccion']} {r['Mencion']} -> {r['n']} Est."
            if st.button(label, key=f"res_{r['Año']}{r['Seccion']}{r['Mencion']}", use_container_width=True):
                ir_a("detalle", r.to_dict())

        if st.button("🗑️ BORRAR TODO EL DÍA", type="secondary"):
            pd.DataFrame(columns=cols_fijas).to_csv(archivo, index=False)
            st.rerun()

# 4. VISTA: DETALLE (Ver personas exactas y si son repitientes)
elif st.session_state.pagina == "detalle":
    if st.button("⬅️ VOLVER"): ir_a("registro")
    
    sel = st.session_state.sec_activa
    st.subheader(f"Lista: {sel['Año']} {sel['Seccion']} {sel['Mencion']}")
    
    df = cargar_datos()
    # Filtramos la lista para ver solo esa sección
    lista = df[(df['Año'] == sel['Año']) & (df['Seccion'] == sel['Seccion']) & (df['Mencion'] == sel['Mencion'])]

    for i, r in lista.iterrows():
        c1, c2 = st.columns([4, 1])
        status = "⚠️ REP" if r['Repitiente'] else "👤 OK"
        c1.write(f"**{r['Hora']}** | {status}")
        if c2.button("🗑️", key=f"del_{r['ID']}"):
            df.drop(i).to_csv(archivo, index=False)
            st.rerun()
