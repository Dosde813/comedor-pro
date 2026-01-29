import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid

# Configuración inicial
st.set_page_config(page_title="Comedor Pro", layout="centered")

# Truco JS para el scroll al inicio
st.components.v1.html("<script>window.parent.scrollTo(0,0);</script>", height=0)

# --- ESTÉTICA CYBERPUNK SOFT (ALTO CONTRASTE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0d0221 !important; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Botones de Selección */
    div.stButton > button { 
        width: 100%; height: 50px; border-radius: 8px; 
        font-weight: bold; border: 2px solid #5b21b6 !important;
        background-color: #1a1a2e !important; color: #ffffff !important;
    }
    .stButton button[kind="primary"] { 
        background-color: #5b21b6 !important; 
        box-shadow: 0 0 10px #5b21b6;
        border: 2px solid #ffffff !important;
    }
    
    /* Botón GUARDAR */
    .btn-save button {
        background-color: #059669 !important; color: #ffffff !important; 
        font-size: 18px !important; border: 2px solid #ffffff !important;
        box-shadow: 0 4px 0px #047857 !important;
    }
    
    /* Cuadros de Totales */
    .stat-card {
        padding: 10px; border-radius: 12px; border: 1px solid #06b6d4;
        text-align: center; background: rgba(6, 182, 212, 0.1);
        margin-bottom: 10px;
    }
    .stat-rep { border-color: #7c3aed; background: rgba(124, 58, 237, 0.1); }

    /* Botón BORRAR (Rojo Sólido) */
    .btn-del button {
        background-color: #b91c1c !important; color: white !important;
        border: 1px solid white !important; height: 38px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MANEJO DE DATOS ---
archivo = "registro_comedor.csv"
cols_fijas = ["ID", "Año", "Seccion", "Mencion", "Repitiente", "Hora"]

def cargar_datos():
    if os.path.exists(archivo):
        try:
            df = pd.read_csv(archivo)
            if "Repitiente" not in df.columns: raise ValueError()
            return df
        except:
            df = pd.DataFrame(columns=cols_fijas)
            df.to_csv(archivo, index=False)
            return df
    else:
        df = pd.DataFrame(columns=cols_fijas)
        df.to_csv(archivo, index=False)
        return df

# --- LIMPIAR SESIÓN AL INICIAR ---
if 'init' not in st.session_state:
    st.session_state.pagina = "registro"
    st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
    st.session_state.init = True

# --- NAVEGACIÓN ---
def ir_a(p, d=None):
    st.session_state.pagina = p
    st.session_state.sec_activa = d
    st.rerun()

# --- VISTA 1: REGISTRO ---
if st.session_state.pagina == "registro":
    st.title("🍴 REGISTRO COMEDOR")
    
    c1, c2 = st.columns(2)
    with c1: fijar = st.toggle("📌 Fijar Selección")
    with c2: rep = st.checkbox("🔄 ES REPITIENTE")

    st.divider()

    def fila_btns(titulo, opciones, clave, pref):
        st.write(f"**{titulo}**")
        cols = st.columns(len(opciones)) if len(opciones) <= 3 else st.columns(2)
        for i, opt in enumerate(opciones):
            es_sel = st.session_state.get(clave) == opt
            # Llave única combinando prefijo y opción para evitar el DuplicateKeyError
            if cols[i % len(cols)].button(opt, key=f"{pref}_{opt}", type="primary" if es_sel else "secondary"):
                st.session_state[clave] = None if es_sel else opt
                st.rerun()

    fila_btns("AÑO", ["1ERO", "2DO", "3ERO"], 's_a', 'btn_a')
    fila_btns("SECCIÓN", ["A", "B", "C"], 's_s', 'btn_s')
    fila_btns("MENCIÓN", ["Química", "Electricidad", "Turismo", "Administración"], 's_m', 'btn_m')

    st.divider()

    # Guardar Registro
    if all([st.session_state.get('s_a'), st.session_state.get('s_s'), st.session_state.get('s_m')]):
        st.markdown('<div class="btn-save">', unsafe_allow_html=True)
        if st.button("✅ GUARDAR REGISTRO", use_container_width=True):
            nuevo = {
                "ID": str(uuid.uuid4())[:8], "Año": st.session_state.s_a, 
                "Seccion": st.session_state.s_s, "Mencion": st.session_state.s_m, 
                "Repitiente": rep, "Hora": datetime.now().strftime("%H:%M")
            }
            df = cargar_datos()
            pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True).to_csv(archivo, index=False)
            if not fijar:
                st.session_state.s_a = st.session_state.s_s = st.session_state.s_m = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Mostrar Totales
    df_hoy = cargar_datos()
    if not df_hoy.empty:
        st.divider()
        ca, cb = st.columns(2)
        t_est = len(df_hoy[df_hoy['Repitiente'] == False])
        ca.markdown(f'<div class="stat-card"><b>ESTUDIANTES</b><br><span style="font-size:22px;">{t_est}</span></div>', unsafe_allow_html=True)
        t_rep = len(df_hoy[df_hoy['Repitiente'] == True])
        cb.markdown(f'<div class="stat-card stat-rep"><b>REPITIENTES</b><br><span style="font-size:22px;">{t_rep}</span></div>', unsafe_allow_html=True)

        st.write("### 📂 Secciones")
        # Agrupamos por todo para que la llave sea única
        res = df_hoy.groupby(["Año", "Seccion", "Mencion"]).size().reset_index(name='n')
        for idx, r in res.iterrows():
            # LLAVE ÚNICA: combina año, seccion y mencion para que no se repita nunca
            unique_key = f"list_{r['Año']}_{r['Seccion']}_{r['Mencion']}"
            if st.button(f"{r['Año']} {r['Seccion']} {r['Mencion']} ({r['n']})", key=unique_key):
                ir_a("detalle", r.to_dict())

        st.divider()
        if st.button("🗑️ LIMPIAR TODO EL DÍA", type="secondary", key="reset_all"):
            pd.DataFrame(columns=cols_fijas).to_csv(archivo, index=False)
            st.rerun()

# --- VISTA 2: DETALLE (BORRAR INDIVIDUAL) ---
elif st.session_state.pagina == "detalle":
    if st.button("⬅️ VOLVER", key="back_btn"): ir_a("registro")
    
    sel = st.session_state.sec_activa
    st.subheader(f"Lista: {sel['Año']} {sel['Seccion']} {sel['Mencion']}")
    
    df = cargar_datos()
    lista = df[(df['Año'] == sel['Año']) & (df['Seccion'] == sel['Seccion']) & (df['Mencion'] == sel['Mencion'])]

    for i, r in lista.iterrows():
        c1, c2 = st.columns([3, 1])
        lbl = "⚠️ REP" if r['Repitiente'] else "👤 OK"
        c1.write(f"**{r['Hora']}** | {lbl}")
        with c2:
            st.markdown('<div class="btn-del">', unsafe_allow_html=True)
            if st.button("Borrar", key=f"del_{r['ID']}"):
                df.drop(i).to_csv(archivo, index=False)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)