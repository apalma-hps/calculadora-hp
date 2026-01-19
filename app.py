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
                "labelColor": "#64748B",
                "titleColor": "#0F172A",
                "gridColor": "#E5E7EB",
            },
            "legend": {
                "labelColor": "#0F172A",
                "titleColor": "#0F172A",
            },
            "line": {"strokeWidth": 3},
            "range": {
                "category": [
                    "#0F172A",
                    "#06B6D4",
                    "#A855F7",
                    "#22C55E",
                    "#F97316",
                    "#EC4899",
                ]
            },
        }
    }

alt.themes.register("hp_theme", hp_altair_theme)
alt.themes.enable("hp_theme")

LOGO_URL = (
    "https://raw.githubusercontent.com/apalma-hps/Dashboard-Ventas-HP/"
    "49cbb064b6dcf8eecaa4fb39292d9fe94f357d49/logo_hp.png"
)

st.set_page_config(
    page_title="Calculadora de Insumos – BOM",
    page_icon=LOGO_URL,
    layout="wide"
)

# --------------------------------------------------
# THEME VISUAL
# --------------------------------------------------
st.markdown(
    """
<style>
    body { background: #E5F3FF !important; }
    .stApp {
        background: linear-gradient(135deg, #E0F2FE 0%, #ECFDF5 50%, #FDF2F8 100%) !important;
        color: #0F172A !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    header[data-testid="stHeader"] > div { background: transparent !important; }
    main.block-container { padding-top: 1rem !important; }
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
    }
    section[data-testid="stSidebar"] * { color: #0F172A !important; }
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    h4, h5 { color: #111827 !important; font-weight: 600 !important; }
    label, span, p, li, .stMarkdown, [data-testid="stMarkdownContainer"] * { color: #0F172A !important; }
    a { color: #06B6D4 !important; text-decoration: none !important; }
    a:hover { color: #0E7490 !important; text-decoration: underline !important; }
    button[kind="primary"], button[kind="secondary"], button[data-testid^="baseButton"] {
        background: linear-gradient(135deg, #06B6D4, #22C55E) !important;
        color: #FFFFFF !important;
        border-radius: 999px !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(8, 145, 178, 0.25) !important;
        font-weight: 600 !important;
    }
    button[kind="primary"]:hover, button[kind="secondary"]:hover, button[data-testid^="baseButton"]:hover {
        background: linear-gradient(135deg, #0891B2, #16A34A) !important;
    }
    input, .stTextInput > div > input, .stNumberInput input, textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 0.75rem !important;
        padding: 0.45rem 0.75rem !important;
    }
    input:focus, .stTextInput > div > input:focus, .stNumberInput input:focus, textarea:focus {
        outline: 2px solid #06B6D4 !important;
        border-color: #06B6D4 !important;
    }
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border-radius: 1.5rem !important;
        padding: 1.2rem 1.5rem !important;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08) !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
    }
    .stSuccess { background-color: #ECFDF5 !important; color: #16A34A !important; border-left: 4px solid #16A34A !important; }
    .stError { background-color: #FEF2F2 !important; color: #DC2626 !important; border-left: 4px solid #DC2626 !important; }
    .stWarning { background-color: #FFFBEB !important; color: #92400E !important; border-left: 4px solid #F59E0B !important; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="
        display:flex; align-items:center; gap:20px;
        margin-top:10px; margin-bottom:25px;
        padding:18px 22px;
        background-color: rgba(255,255,255,0.9);
        border-radius: 24px;
        box-shadow: 0 18px 45px rgba(15,23,42,0.08);
    ">
        <img src="{LOGO_URL}" style="
            width:80px; height:80px; object-fit:contain;
            border-radius:50%; background:white;
            box-shadow: 0 4px 12px rgba(15,23,42,0.18);
        "/>
        <div>
            <h1 style="font-size: 1.9rem; font-weight:700; margin:0; padding:0; color:#0F172A;">
                Calculadora de Insumos por Receta (BOM)
            </h1>
            <p style="margin:4px 0 0 0; color:#64748B; font-size:0.95rem;">
                Elige productos, cantidades y obtén consumo teórico, objetivo con merma y KPI vs consumo real.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# HELPERS
# =========================
DATA_PATH = Path("data") / "bom_recetas.xlsx"


def parse_merma(raw: str) -> float:
    """
    Acepta: '0.1', '.30', '0.30', '30%', '0,3'
    Devuelve proporción float >= 0
    """
    if raw is None:
        return 0.0
    s = str(raw).strip()
    if s == "":
        return 0.0
    s = s.replace(",", ".")
    is_pct = False
    if s.endswith("%"):
        is_pct = True
        s = s[:-1].strip()
    if s.startswith("."):
        s = "0" + s
    try:
        v = float(s)
    except Exception:
        raise ValueError("Merma inválida. Usa por ejemplo: 0.10, .30, 0.30, 30%")
    if is_pct:
        v = v / 100.0
    if v < 0:
        raise ValueError("La merma no puede ser negativa.")
    return v


def convert_to_base_units(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte la cantidad final:
    - gr -> kg (divide entre 1000)
    - ml -> lt (divide entre 1000)
    Mantiene otras unidades igual.
    Espera columnas:
      - Unidad_comp
      - Cant_total_comp_teorico
      - Cant_total_comp_objetivo
    Agrega:
      - Unidad_final
      - Cant_total_teorico_final
      - Cant_total_objetivo_final
    """
    out = df.copy()

    unit = out["Unidad_comp"].astype(str).str.strip().str.lower()

    # factores
    factor = np.where(unit.eq("gr"), 1/1000,
             np.where(unit.eq("ml"), 1/1000, 1.0))

    unidad_final = np.where(unit.eq("gr"), "kg",
                   np.where(unit.eq("ml"), "lt", out["Unidad_comp"]))

    out["Unidad_final"] = unidad_final
    out["Cant_total_teorico_final"] = out["Cant_total_comp_teorico"] * factor
    out["Cant_total_objetivo_final"] = out["Cant_total_comp_objetivo"] * factor

    return out


@st.cache_data
def load_bom(path: Path) -> pd.DataFrame:
    """
    Carga el BOM con columnas estándar.
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

    # Fill-down de cabecera para filas de componentes
    for col in ["Producto", "Nombre_prod", "Cantidad_prod", "Unidad_prod", "Referencia", "Tipo_BOM", "Costo_receta", "PU"]:
        df[col] = df[col].ffill()

    # Señal de cabecera
    mask_header = df["Tipo_BOM"].notna()

    # FIX de desfase (solo si tu excel está corrido así)
    df["Componente"] = df["Componente"].where(mask_header, df["PU"])
    df["Nombre_comp"] = df["Nombre_comp"].where(mask_header, df["Componente"])
    df["Cantidad_comp"] = df["Cantidad_comp"].where(mask_header, df["Nombre_comp"])
    df["Unidad_comp"] = df["Unidad_comp"].where(mask_header, df["Cantidad_comp"])

    # Numéricos
    for col in ["Cantidad_prod", "Costo_receta", "PU", "Cantidad_comp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Textos
    for col in ["Producto", "Nombre_prod", "Componente", "Nombre_comp", "Unidad_comp"]:
        df[col] = df[col].astype(str).str.strip()

    # Quitar ruido sin componente
    df = df[df["Componente"] != ""].copy()

    return df


# =========================
# LOAD BOM
# =========================
try:
    bom_df = load_bom(DATA_PATH)
except Exception as e:
    st.error("❌ No pude cargar el archivo de BOM.\n\n" f"Detalles del error: {e}")
    st.stop()

productos_df = (
    bom_df[bom_df["Tipo_BOM"].notna()][["Producto", "Nombre_prod", "Costo_receta", "PU"]]
    .drop_duplicates(subset=["Producto", "Nombre_prod"])
    .sort_values("Producto")
    .reset_index(drop=True)
)

producto_labels = {row["Producto"]: f'{row["Producto"]} – {row["Nombre_prod"]}' for _, row in productos_df.iterrows()}
def format_producto(prod_id: str) -> str:
    return producto_labels.get(prod_id, str(prod_id))


# =========================
# SIDEBAR CONTROLS
# =========================
with st.sidebar:
    st.header("⚙️ Opciones de cálculo")
    st.markdown(
        """
        1) Elige productos del pedido  
        2) Captura cantidades por producto  
        3) Calcula insumos teóricos  
        4) Aplica merma objetivo  
        5) Pega/sube consumo real → KPI
        """
    )

    merma_raw = st.text_input("Merma objetivo (proporción). Ej: 0.10, .30, 30%", value="0.00")
    try:
        merma_obj = parse_merma(merma_raw)
    except Exception as e:
        st.error(f"❌ {e}")
        st.stop()

    if merma_obj >= 1:
        st.warning("⚠️ Merma ≥ 1.0 significa 100% o más. Si querías 30%, usa 0.30 o 30%.")

    factor_merma = 1.0 + merma_obj
    st.caption(f"Factor objetivo aplicado a insumos: **{factor_merma:.3f}**")

    mostrar_costos = st.checkbox("Mostrar sección de costos", value=True)
    aplicar_merma_a_costos = st.checkbox(
        "Aplicar merma objetivo al costo teórico",
        value=True,
        help="Si activas esto, el costo objetivo se multiplica por (1 + merma).",
    )

# =========================
# 1) SELECCIÓN PRODUCTOS
# =========================
st.subheader("1️⃣ Selecciona productos del pedido")
productos_sel = st.multiselect(
    "Productos a preparar:",
    options=productos_df["Producto"].tolist(),
    format_func=format_producto,
)

if not productos_sel:
    st.info("Selecciona al menos un producto para comenzar.")
    st.stop()

# =========================
# 2) CAPTURA CANTIDADES
# =========================
st.subheader("2️⃣ Ingresa las cantidades a preparar")

pedido_rows = []
cols = st.columns(min(len(productos_sel), 4))
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
st.dataframe(pedido_df.merge(productos_df, on="Producto", how="left"), use_container_width=True)

# =========================
# 3) INSUMOS TEÓRICOS + OBJETIVO
# =========================
st.subheader("3️⃣ Consumo total de insumos (Teórico vs Objetivo con merma)")

detalle = pedido_df.merge(
    bom_df[["Producto", "Componente", "Nombre_comp", "Cantidad_comp", "Unidad_comp"]],
    on="Producto",
    how="left",
)

detalle["Cant_total_comp_teorico"] = detalle["Cantidad_pedida"] * detalle["Cantidad_comp"]
detalle["Cant_total_comp_objetivo"] = detalle["Cant_total_comp_teorico"] * factor_merma

resumen = (
    detalle.groupby(["Componente", "Nombre_comp", "Unidad_comp"], as_index=False)[
        ["Cant_total_comp_teorico", "Cant_total_comp_objetivo"]
    ]
    .sum()
    .sort_values("Nombre_comp")
    .reset_index(drop=True)
)

# ✅ NUEVO: convertir a kg/lt cuando aplique
resumen = convert_to_base_units(resumen)

st.markdown("#### 📋 Requerimiento total por componente (convertido a kg/lt si aplica)")
st.dataframe(
    resumen[
        [
            "Componente",
            "Nombre_comp",
            "Unidad_comp",
            "Cant_total_comp_teorico",
            "Cant_total_comp_objetivo",
            "Unidad_final",
            "Cant_total_teorico_final",
            "Cant_total_objetivo_final",
        ]
    ],
    use_container_width=True,
)

# =========================
# 4) COSTO TEÓRICO + OBJETIVO (opcional)
# =========================
if mostrar_costos:
    st.subheader("4️⃣ Costo (Teórico vs Objetivo con merma)")

    costo_df = pedido_df.merge(
        productos_df[["Producto", "Nombre_prod", "Costo_receta", "PU"]],
        on="Producto",
        how="left",
    )

    costo_df["Costo_total_teorico"] = costo_df["Cantidad_pedida"] * costo_df["Costo_receta"]
    costo_df["PU_teorico"] = costo_df["Costo_receta"] / costo_df["PU"].replace(0, np.nan)

    if aplicar_merma_a_costos:
        costo_df["Costo_total_objetivo"] = costo_df["Costo_total_teorico"] * factor_merma
        total_costo_teo = float(costo_df["Costo_total_teorico"].sum())
        total_costo_obj = float(costo_df["Costo_total_objetivo"].sum())
    else:
        costo_df["Costo_total_objetivo"] = np.nan
        total_costo_teo = float(costo_df["Costo_total_teorico"].sum())
        total_costo_obj = np.nan

    st.dataframe(
        costo_df[
            [
                "Producto",
                "Nombre_prod",
                "Cantidad_pedida",
                "Costo_receta",
                "Costo_total_teorico",
                "Costo_total_objetivo",
            ]
        ],
        use_container_width=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Costo total teórico", f"${total_costo_teo:,.2f} MXN")
    with c2:
        if aplicar_merma_a_costos:
            st.metric("Costo objetivo (con merma)", f"${total_costo_obj:,.2f} MXN")
        else:
            st.metric("Costo objetivo (con merma)", "—")

# =========================
# 5) KPI MERMA REAL (requiere consumo real)
# =========================
st.subheader("5️⃣ KPI de merma real (requiere consumo real)")

st.markdown(
    """
**Qué medimos aquí:**

- **Merma real (%)** por componente = (Real − Teórico) / Teórico  
- **Gap vs objetivo** = Real − Objetivo  
- Si *Real* < *Teórico*, el KPI sale negativo (sobrante, subregistro o error de captura).
"""
)

with st.expander("📥 Cargar consumo real (CSV) o pegar tabla", expanded=True):
    st.caption("Estructura mínima: columnas **Componente** y **Cant_real** (numérica).")
    up = st.file_uploader("Sube CSV de consumo real", type=["csv"])

    if "real_editor_df" not in st.session_state:
        st.session_state.real_editor_df = pd.DataFrame(
            {"Componente": ["", ""], "Cant_real": [0.0, 0.0]}
        )

    real_editor = st.data_editor(
        st.session_state.real_editor_df,
        use_container_width=True,
        num_rows="dynamic",
        key="real_editor",
    )

    real_df = None
    if up is not None:
        try:
            real_df = pd.read_csv(up)
        except Exception as e:
            st.error(f"No pude leer el CSV: {e}")
            real_df = None
    else:
        real_df = real_editor.copy()

if real_df is None or real_df.empty:
    st.info("Carga o pega consumo real para calcular el KPI.")
else:
    # Normalizar columnas
    real_df = real_df.rename(columns={c: c.strip() for c in real_df.columns})
    rename_map = {}
    for c in real_df.columns:
        cl = c.strip().lower()
        if cl in ["cant_real", "cantidad_real", "consumo_real", "real"]:
            rename_map[c] = "Cant_real"
        if cl in ["componente", "component", "sku", "insumo"]:
            rename_map[c] = "Componente"
    real_df = real_df.rename(columns=rename_map)

    if "Componente" not in real_df.columns or "Cant_real" not in real_df.columns:
        st.error("El consumo real debe tener columnas: **Componente** y **Cant_real**.")
        st.stop()

    real_df["Componente"] = real_df["Componente"].astype(str).str.strip()
    real_df["Cant_real"] = pd.to_numeric(real_df["Cant_real"], errors="coerce").fillna(0.0)
    real_df = real_df.groupby("Componente", as_index=False)["Cant_real"].sum()

    # Merge KPI con resumen
    kpi_df = resumen.merge(real_df, on="Componente", how="left")
    kpi_df["Cant_real"] = kpi_df["Cant_real"].fillna(0.0)

    # ⚠️ NOTA: aquí NO convierto Cant_real automáticamente porque no sabemos si tu real viene en gr/ml o kg/lt.
    # Si tu real SIEMPRE viene en la misma unidad que Unidad_comp (gr/ml), activa esta conversión:
    convertir_real_mismo_origen = st.checkbox(
        "Mi consumo real está en la misma unidad original (gr/ml) y quiero convertirlo a kg/lt también",
        value=False
    )
    if convertir_real_mismo_origen:
        unit = kpi_df["Unidad_comp"].astype(str).str.strip().str.lower()
        factor = np.where(unit.eq("gr"), 1/1000, np.where(unit.eq("ml"), 1/1000, 1.0))
        kpi_df["Cant_real_final"] = kpi_df["Cant_real"] * factor
    else:
        kpi_df["Cant_real_final"] = kpi_df["Cant_real"]

    # KPI (si convertiste, compáralo en la misma base final)
    denom = kpi_df["Cant_total_teorico_final"].replace(0, np.nan)
    kpi_df["Merma_real_pct"] = (kpi_df["Cant_real_final"] - kpi_df["Cant_total_teorico_final"]) / denom
    kpi_df["Gap_vs_teorico"] = kpi_df["Cant_real_final"] - kpi_df["Cant_total_teorico_final"]
    kpi_df["Gap_vs_objetivo"] = kpi_df["Cant_real_final"] - kpi_df["Cant_total_objetivo_final"]

    total_teo = float(kpi_df["Cant_total_teorico_final"].sum())
    total_real = float(kpi_df["Cant_real_final"].sum())
    total_obj = float(kpi_df["Cant_total_objetivo_final"].sum())

    merma_global = (total_real - total_teo) / (total_teo if total_teo != 0 else np.nan)
    gap_global_obj = total_real - total_obj

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Merma real global (vs teórico)", f"{(merma_global*100):.2f}%" if pd.notna(merma_global) else "—")
    with m2:
        st.metric("Gap global vs objetivo", f"{gap_global_obj:,.3f}")
    with m3:
        st.metric("Merma objetivo", f"{(merma_obj*100):.2f}%")

    st.markdown("#### 📌 KPI por componente (en kg/lt si aplica)")
    show_cols = [
        "Componente",
        "Nombre_comp",
        "Unidad_final",
        "Cant_total_teorico_final",
        "Cant_total_objetivo_final",
        "Cant_real_final",
        "Merma_real_pct",
        "Gap_vs_teorico",
        "Gap_vs_objetivo",
    ]
    st.dataframe(kpi_df[show_cols].sort_values("Merma_real_pct", ascending=False), use_container_width=True)

    st.download_button(
        "Descargar KPI (CSV)",
        data=kpi_df[show_cols].to_csv(index=False).encode("utf-8-sig"),
        file_name="kpi_merma_real.csv",
        mime="text/csv",
    )

# =========================
# 6) DESCARGAS ORIGINALES
# =========================
st.subheader("6️⃣ Descargar resultados")

tab1, tab2 = st.tabs(["Insumos (Teórico/Objetivo)", "Detalle BOM × pedido"])

with tab1:
    st.download_button(
        label="⬇️ Descargar insumos (CSV)",
        data=resumen.to_csv(index=False).encode("utf-8-sig"),
        file_name="insumos_pedido.csv",
        mime="text/csv",
    )

with tab2:
    detalle_export = detalle.merge(productos_df[["Producto", "Nombre_prod"]], on="Producto", how="left")
    st.download_button(
        label="⬇️ Descargar detalle BOM × pedido (CSV)",
        data=detalle_export.to_csv(index=False).encode("utf-8-sig"),
        file_name="detalle_bom_pedido.csv",
        mime="text/csv",
    )

st.success("Listo. Totales convertidos a kg/lt cuando Unidad_comp es gr/ml.")
