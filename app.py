import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
from pathlib import Path
import altair as alt

# =========================
# TEMA ALTÁIR HP
# =========================
def hp_altair_theme():
    return {
        "config": {
            "background": "rgba(0,0,0,0)",
            "view": {"stroke": "transparent"},
            "axis": {
                "labelColor": "#64748B",   # slate-500
                "titleColor": "#0F172A",   # slate-900
                "gridColor": "#E5E7EB",
            },
            "legend": {
                "labelColor": "#0F172A",
                "titleColor": "#0F172A",
            },
            "line": {
                "strokeWidth": 3,
            },
            "range": {
                "category": [
                    "#0F172A",  # negro para Masaryk
                    "#06B6D4",  # cyan
                    "#A855F7",  # violeta
                    "#22C55E",  # verde
                    "#F97316",  # naranja
                    "#EC4899",  # rosa
                ]
            },
        }
    }


alt.themes.register("hp_theme", hp_altair_theme)
alt.themes.enable("hp_theme")

# Logo HP
LOGO_URL = (
    "https://raw.githubusercontent.com/apalma-hps/Dashboard-Ventas-HP/"
    "49cbb064b6dcf8eecaa4fb39292d9fe94f357d49/logo_hp.png"
)

# --------------------------------------------------
# Configuración básica de la página
# --------------------------------------------------
st.set_page_config(
    page_title="Calculadora de Insumos – BOM",
    page_icon=LOGO_URL,
    layout="wide"
)

# --------------------------------------------------
# THEME VISUAL (MISMO QUE INVENTARIOS)
# --------------------------------------------------
st.markdown(
    """
<style>
    body {
        background: #E5F3FF !important;
    }

    .stApp {
        background: linear-gradient(135deg, #E0F2FE 0%, #ECFDF5 50%, #FDF2F8 100%) !important;
        color: #0F172A !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    header[data-testid="stHeader"] > div {
        background: transparent !important;
    }

    main.block-container {
        padding-top: 1rem !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
    }
    section[data-testid="stSidebar"] * {
        color: #0F172A !important;
    }

    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    h4, h5 {
        color: #111827 !important;
        font-weight: 600 !important;
    }

    label, span, p, li, .stMarkdown, [data-testid="stMarkdownContainer"] * {
        color: #0F172A !important;
    }

    a {
        color: #06B6D4 !important;
        text-decoration: none !important;
    }
    a:hover {
        color: #0E7490 !important;
        text-decoration: underline !important;
    }

    button[kind="primary"],
    button[kind="secondary"],
    button[data-testid^="baseButton"] {
        background: linear-gradient(135deg, #06B6D4, #22C55E) !important;
        color: #FFFFFF !important;
        border-radius: 999px !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(8, 145, 178, 0.25) !important;
        font-weight: 600 !important;
    }
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover,
    button[data-testid^="baseButton"]:hover {
        background: linear-gradient(135deg, #0891B2, #16A34A) !important;
    }

    [data-testid="stNumberInput"] button {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 0.75rem !important;
        box-shadow: none !important;
    }

    input,
    .stTextInput > div > input,
    .stNumberInput input,
    textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 0.75rem !important;
        padding: 0.45rem 0.75rem !important;
    }
    input:focus,
    .stTextInput > div > input:focus,
    .stNumberInput input:focus,
    textarea:focus {
        outline: 2px solid #06B6D4 !important;
        border-color: #06B6D4 !important;
    }

    [data-testid="stDateInput"] input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 0.75rem !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-radius: 0.75rem !important;
        border: 1px solid #D1D5DB !important;
    }
    div[data-baseweb="select"] svg {
        color: #64748B !important;
    }

    [data-baseweb="menu"],
    [data-baseweb="popover"] [data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-radius: 0.75rem !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 18px 45px rgba(15,23,42,0.18) !important;
    }

    [data-baseweb="menu"] [role="option"][aria-selected="true"],
    [data-baseweb="menu"] [role="option"]:hover {
        background-color: #DBEAFE !important;
        color: #0F172A !important;
    }

    .dataframe {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-radius: 1rem !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06) !important;
    }

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        background-color: #FFFFFF !important;
    }

    [data-testid="stDataFrame"] th,
    [data-testid="stTable"] th {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-weight: 600 !important;
    }

    [data-testid="stDataFrame"] tr:hover td,
    [data-testid="stTable"] tr:hover td {
        background-color: #F1F5F9 !important;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border-radius: 1.5rem !important;
        padding: 1.2rem 1.5rem !important;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
    }

    .stSuccess {
        background-color: #ECFDF5 !important;
        color: #16A34A !important;
        border-left: 4px solid #16A34A !important;
    }
    .stError {
        background-color: #FEF2F2 !important;
        color: #DC2626 !important;
        border-left: 4px solid #DC2626 !important;
    }
    .stWarning {
        background-color: #FFFBEB !important;
        color: #92400E !important;
        border-left: 4px solid #F59E0B !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Encabezado con logo
# --------------------------------------------------
st.markdown(
    f"""
    <div style="
        display:flex;
        align-items:center;
        gap:20px;
        margin-top:10px;
        margin-bottom:25px;
        padding:18px 22px;
        background-color: rgba(255,255,255,0.9);
        border-radius: 24px;
        box-shadow: 0 18px 45px rgba(15,23,42,0.08);
    ">
        <img src="{LOGO_URL}" 
             style="
                width:80px; 
                height:80px; 
                object-fit:contain; 
                border-radius:50%; 
                background:white;
                box-shadow: 0 4px 12px rgba(15,23,42,0.18);
             "/>
        <div>
            <h1 style="
                font-size: 1.9rem; 
                font-weight:700; 
                margin:0; 
                padding:0;
                color:#0F172A;
            ">
                Calculadora de Insumos por Receta (BOM)
            </h1>
            <p style="
                margin:4px 0 0 0;
                color:#64748B;
                font-size:0.95rem;
            ">
                Elige productos, cantidades y obtén el consumo total de insumos por receta estandarizada.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# LÓGICA DE LA CALCULADORA
# =========================

DATA_PATH = Path("data") / "bom_recetas.xlsx"


@st.cache_data
def load_bom(path: Path) -> pd.DataFrame:
    """
    Carga el BOM, corrige el desfase de columnas de componentes,
    y deja todo listo para multiplicar cantidades.
    """
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")
    df = pd.read_excel(path)

    expected_cols = [
        "Producto",
        "Nombre_prod",
        "Cantidad_prod",
        "Unidad_prod",
        "Referencia",
        "Tipo_BOM",
        "Costo_receta",
        "PU",
        "Componente",
        "Nombre_comp",
        "Cantidad_comp",
        "Unidad_comp",
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan estas columnas en el Excel: {missing}")

    # 1) Rellenar hacia abajo la info del producto para las filas de componentes
    for col in [
        "Producto",
        "Nombre_prod",
        "Cantidad_prod",
        "Unidad_prod",
        "Referencia",
        "Tipo_BOM",
        "Costo_receta",
        "PU",
    ]:
        df[col] = df[col].ffill()

    # 2) Corregir el desfase de columnas en filas de componentes "rotas"
    mask_header = df["Tipo_BOM"].notna()
    mask_comp_extra = df["Tipo_BOM"].isna()

    # Código componente
    df["Componente"] = df["Componente"].where(mask_header, df["PU"])
    # Nombre de componente
    df["Nombre_comp"] = df["Nombre_comp"].where(mask_header, df["Componente"])
    # Cantidad de componente
    df["Cantidad_comp"] = df["Cantidad_comp"].where(mask_header, df["Nombre_comp"])
    # Unidad de componente
    df["Unidad_comp"] = df["Unidad_comp"].where(mask_header, df["Cantidad_comp"])

    # 3) Forzar numéricos
    for col in ["Cantidad_prod", "Costo_receta", "PU", "Cantidad_comp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # 4) Limpieza de textos
    for col in ["Producto", "Nombre_prod", "Componente", "Nombre_comp", "Unidad_comp"]:
        df[col] = df[col].astype(str).str.strip()

    # Quitar filas sin componente (ruido)
    df = df[df["Componente"] != ""]

    return df


# Cargar BOM
try:
    bom_df = load_bom(DATA_PATH)
except Exception as e:
    st.error(
        "❌ No pude cargar el archivo de BOM.\n\n"
        f"Detalles del error: {e}"
    )
    st.stop()

# -------------------------
# TABLAS DERIVADAS
# -------------------------
# Solo filas cabecera (receta), donde Tipo_BOM no es nulo
productos_df = (
    bom_df[bom_df["Tipo_BOM"].notna()][
        ["Producto", "Nombre_prod", "Costo_receta", "PU"]
    ]
    .drop_duplicates(subset=["Producto", "Nombre_prod"])
    .sort_values("Producto")
    .reset_index(drop=True)
)

# Diccionario para mostrar bonito en los select
producto_labels = {
    row["Producto"]: f'{row["Producto"]} – {row["Nombre_prod"]}'
    for _, row in productos_df.iterrows()
}


def format_producto(prod_id: str) -> str:
    return producto_labels.get(prod_id, str(prod_id))


# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.header("⚙️ Opciones de cálculo")
    st.markdown(
        """
        1. Elige los productos del pedido  
        2. Captura cantidades por producto  
        3. Revisa insumos totales y costo teórico
        """
    )
    mostrar_costos = st.checkbox("Mostrar sección de costos", value=True)

# -------------------------
# 1) SELECCIÓN DE PRODUCTOS
# -------------------------
st.subheader("1️⃣ Selecciona productos del pedido")

productos_sel = st.multiselect(
    "Productos a preparar:",
    options=productos_df["Producto"].tolist(),
    format_func=format_producto,
)

if not productos_sel:
    st.info("Selecciona al menos un producto en el combo de arriba para comenzar.")
    st.stop()

# -------------------------
# 2) CAPTURA DE CANTIDADES
# -------------------------
st.subheader("2️⃣ Ingresa las cantidades a preparar")

pedido_rows = []
cols = st.columns(min(len(productos_sel), 4))  # hasta 4 columnas visuales

for idx, prod in enumerate(productos_sel):
    col = cols[idx % 4]
    with col:
        nombre = format_producto(prod)
        qty = st.number_input(
            f"Cantidad de\n**{nombre}**",
            min_value=0,
            step=1,
            value=0,
            key=f"qty_{prod}",
        )
        pedido_rows.append({"Producto": prod, "Cantidad_pedida": qty})

pedido_df = pd.DataFrame(pedido_rows)
pedido_df = pedido_df[pedido_df["Cantidad_pedida"] > 0]

if pedido_df.empty:
    st.warning("Ingresa cantidades mayores a 0 para al menos un producto.")
    st.stop()

st.markdown("### 🧾 Resumen de productos del pedido")
st.dataframe(
    pedido_df.merge(productos_df, on="Producto", how="left"),
    use_container_width=True,
)

# -------------------------
# 3) CÁLCULO DE INSUMOS TOTALES
# -------------------------
st.subheader("3️⃣ Consumo total de insumos")

detalle = pedido_df.merge(
    bom_df[
        [
            "Producto",
            "Componente",
            "Nombre_comp",
            "Cantidad_comp",
            "Unidad_comp",
        ]
    ],
    on="Producto",
    how="left",
)

detalle["Cant_total_comp"] = detalle["Cantidad_pedida"] * detalle["Cantidad_comp"]

resumen_insumos = (
    detalle.groupby(["Componente", "Nombre_comp", "Unidad_comp"], as_index=False)[
        "Cant_total_comp"
    ]
    .sum()
    .sort_values("Nombre_comp")
)

st.markdown("#### 📋 Requerimiento total por componente")
st.dataframe(
    resumen_insumos,
    use_container_width=True,
)

# -------------------------
# 4) COSTO TEÓRICO DEL PEDIDO (opcional)
# -------------------------
if mostrar_costos:
    st.subheader("4️⃣ Costo teórico del pedido")

    costo_df = pedido_df.merge(
        productos_df[["Producto", "Nombre_prod", "Costo_receta", "PU"]],
        on="Producto",
        how="left",
    )

    costo_df["Costo_total_producto"] = (
        costo_df["Cantidad_pedida"] * costo_df["Costo_receta"]
    )
    costo_df["PU_teorico"] = costo_df["Costo_receta"] / costo_df["PU"].replace(0, np.nan)

    total_costo = costo_df["Costo_total_producto"].sum()

    st.markdown("#### 🧮 Detalle por producto")
    st.dataframe(
        costo_df[
            [
                "Producto",
                "Nombre_prod",
                "Cantidad_pedida",
                "Costo_receta",
                "Costo_total_producto",
            ]
        ],
        use_container_width=True,
    )

    st.markdown(f"### 💰 Costo total teórico del pedido: **${total_costo:,.2f}** MXN")

# -------------------------
# 5) DESCARGA DE RESULTADOS
# -------------------------
st.subheader("5️⃣ Descargar resultados")

tab1, tab2 = st.tabs(["Insumos", "Detalle BOM × pedido"])

with tab1:
    st.download_button(
        label="⬇️ Descargar insumos (CSV)",
        data=resumen_insumos.to_csv(index=False).encode("utf-8-sig"),
        file_name="insumos_pedido.csv",
        mime="text/csv",
    )

with tab2:
    detalle_export = detalle.merge(
        productos_df[["Producto", "Nombre_prod"]], on="Producto", how="left"
    )
    st.download_button(
        label="⬇️ Descargar detalle BOM × pedido (CSV)",
        data=detalle_export.to_csv(index=False).encode("utf-8-sig"),
        file_name="detalle_bom_pedido.csv",
        mime="text/csv",
    )

st.success("Listo. Arriba tienes el consumo total de insumos y los botones para exportar.")
