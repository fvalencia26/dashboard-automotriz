
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel("Ventas.xlsx")

df["Fecha Venta"] = pd.to_datetime(df["Fecha Venta"])

df["Año"] = df["Fecha Venta"].dt.year

df["Mes"] = df["Fecha Venta"].dt.month

df["Periodo"] = df["Fecha Venta"].dt.strftime("%Y-%m")

# =========================================================
# CONFIGURACION PAGINA
# =========================================================

st.set_page_config(
    page_title="Dashboard Comercial y Pricing",
    layout="wide"
)

# =========================================================
# ESTILO VISUAL
# =========================================================

st.markdown("""
<style>

.stApp{
    background:
    linear-gradient(
        180deg,
        #020617 0%,
        #0f172a 55%,
        #111827 100%
    );

    color:white;
}
            
h1{
    color:white !important;
    font-size:48px !important;
    font-weight:800 !important;
}

h2,h3,h4,h5,h6{
    color:white !important;
    font-weight:700 !important;
}

label{
    color:white !important;
    font-weight:bold;
}

[data-testid="metric-container"]{

    background:
    linear-gradient(
        145deg,
        rgba(17,24,39,0.98),
        rgba(30,41,59,0.95)
    );

    border-radius:24px;

    padding:28px;

    border:1px solid rgba(148,163,184,0.12);

    box-shadow:
    0 10px 30px rgba(0,0,0,0.35);

    transition:0.3s;
}

[data-testid="metric-container"]:hover{

    transform:translateY(-5px);

    border:1px solid rgba(96,165,250,0.45);

    box-shadow:
    0 18px 35px rgba(37,99,235,0.22);
}

[data-testid="metric-container"] label{
    color:#cbd5e1 !important;
}

[data-testid="metric-container"] div{
    color:white !important;
}

.stTabs [data-baseweb="tab"]{

    background-color:#111827;

    border-radius:14px;

    padding:12px 24px;

    font-size:18px;

    font-weight:700;

    color:white;
}
.stTabs [aria-selected="true"]{

    background:linear-gradient(
        135deg,
        #dc2626,
        #991b1b
    ) !important;

    color:white !important;

    box-shadow:0 6px 20px rgba(220,38,38,0.35);
}
            
</style>
""", unsafe_allow_html=True)

# =========================================================
# TITULO
# =========================================================

col_logo, col_titulo = st.columns([1,4])

with col_logo:
    st.image("logo_callegari.png", width=220)

with col_titulo:
    st.title("🚗 Dashboard Comercial y Pricing")
    st.caption("Inteligencia Comercial · Pricing · Ventas · Stock")

st.markdown("---")

# =========================================================
# LEER ARCHIVOS
# =========================================================

df_ventas = pd.read_excel(
    "Ventas.xlsx",
    sheet_name="Hoja1"
)

df_stock = pd.read_excel(
    "stock.xlsx.xlsx",
    sheet_name="BBDD2"
)



# =========================================================
# TOMAS Y RETOMAS
# =========================================================

archivo_tomas = "tomas.xlsx"

df_tasaciones = pd.read_excel(
    archivo_tomas,
    sheet_name="Tasaciones"
)

df_peritajes = pd.read_excel(
    archivo_tomas,
    sheet_name="Peritajes"
)

df_tomas = pd.read_excel(
    archivo_tomas,
    sheet_name="Toma"
)

# =========================================================
# LIMPIAR COLUMNAS
# =========================================================

df_ventas.columns = df_ventas.columns.str.strip()
df_stock.columns = df_stock.columns.str.strip()

df_tasaciones.columns = df_tasaciones.columns.str.strip()
df_peritajes.columns = df_peritajes.columns.str.strip()
df_tomas.columns = df_tomas.columns.str.strip()
# =========================================================
# FORMATO COLUMNAS
# =========================================================

df_stock["Marca"] = df_stock["Marca"].astype(str)
df_stock["Modelo"] = df_stock["Modelo"].astype(str)
df_stock["Versión"] = df_stock["Versión"].astype(str)
df_stock["Placa Patente"] = df_stock["Placa Patente"].astype(str)

# =========================================================
# FECHAS
# =========================================================

df_ventas["Fecha Venta"] = pd.to_datetime(
    df_ventas["Fecha Venta"],
    errors="coerce"
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
<h2 style="
color:white;
font-size:28px;
font-weight:800;
">
🔎 Filtros
</h2>
""", unsafe_allow_html=True)

# -----------------------------
# FILTROS
# -----------------------------

st.sidebar.header("Filtros")

años = sorted(df["Año"].unique())

años_sel = st.sidebar.multiselect(
    "Año",
    años,
    default=años
)

meses = list(range(1, 13))

meses_sel = st.sidebar.multiselect(
    "Mes",
    meses,
    default=meses
)

df = df[
    (df["Año"].isin(años_sel)) &
    (df["Mes"].isin(meses_sel))
]

marca = st.sidebar.multiselect(
    "Marca",
    sorted(df_ventas["Marca"].dropna().unique())
)

if marca:

    modelos_disponibles = sorted(
        df[
            df["Marca"].isin(marca)
        ]["Modelo"]
        .dropna()
        .astype(str)
        .unique()
    )

else:

    modelos_disponibles = sorted(
        df["Modelo"]
        .dropna()
        .astype(str)
        .unique()
    )

modelo = st.sidebar.multiselect(
    "Modelo",
    modelos_disponibles
)

df_version = df.copy()

if marca:

    df_version = df_version[
        df_version["Marca"].isin(marca)
    ]

if modelo:

    df_version = df_version[
        df_version["Modelo"]
        .astype(str)
        .isin(modelo)
    ]

version = st.sidebar.multiselect(
    "Versión",
    sorted(
        df_version["Versión"]
        .dropna()
        .astype(str)
        .unique()
    )
)

vendedor = st.sidebar.multiselect(
    "Vendedor",
    sorted(df_ventas["Vendedor"].dropna().unique())
)

sucursal = st.sidebar.multiselect(
    "Sucursal",
    sorted(df_ventas["Sucursal"].dropna().unique())
)

# =========================================================
# FILTROS
# =========================================================

df_filtrado = df_ventas.copy()

df_filtrado = df[
    (df["Año"].isin(años_sel)) &
    (df["Mes"].isin(meses_sel))
]

if marca:

    df_filtrado = df_filtrado[
        df_filtrado["Marca"].isin(marca)
    ]

if modelo:

    df_filtrado = df_filtrado[
        df_filtrado["Modelo"]
        .astype(str)
        .str.strip()
        .isin([m.strip() for m in modelo])
    ]

if version:

    df_filtrado = df_filtrado[
        df_filtrado["Versión"]
        .astype(str)
        .str.strip()
        .isin([v.strip() for v in version])
    ]

if vendedor:

    df_filtrado = df_filtrado[
        df_filtrado["Vendedor"].isin(vendedor)
    ]

if sucursal:

    df_filtrado = df_filtrado[
        df_filtrado["Sucursal"].isin(sucursal)
    ]

# =========================================================
# FILTROS TOMAS
# =========================================================

df_tomas["Fecha carta de toma"] = pd.to_datetime(
    df_tomas["Fecha carta de toma"],
    errors="coerce"
)

df_tomas["Año Filtro"] = df_tomas["Fecha carta de toma"].dt.year
df_tomas["Mes Filtro"] = df_tomas["Fecha carta de toma"].dt.month

df_toma_filtrado = df_tomas[
    (df_tomas["Año Filtro"].isin(años_sel))
    &
    (df_tomas["Mes Filtro"].isin(meses_sel))
]

df_tasaciones["Última Actualización"] = pd.to_datetime(
    df_tasaciones["Última Actualización"],
    errors="coerce"
)

df_tasaciones["Año Filtro"] = df_tasaciones["Última Actualización"].dt.year
df_tasaciones["Mes Filtro"] = df_tasaciones["Última Actualización"].dt.month


df_peritajes["Fecha de firma"] = pd.to_datetime(
    df_peritajes["Fecha de firma"],
    errors="coerce"
)

df_peritajes["Año Filtro"] = df_peritajes["Fecha de firma"].dt.year
df_peritajes["Mes Filtro"] = df_peritajes["Fecha de firma"].dt.month


# =========================================================
# DATAFRAMES FILTRADOS
# =========================================================

df_tas_filtrado = df_tasaciones[
    (df_tasaciones["Año Filtro"].isin(años_sel))
    &
    (df_tasaciones["Mes Filtro"].isin(meses_sel))
]

df_per_filtrado = df_peritajes[
    (df_peritajes["Año Filtro"].isin(años_sel))
    &
    (df_peritajes["Mes Filtro"].isin(meses_sel))
]
# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs([
    "📈 Ventas",
    "🚗 Stock y Pricing",
    "🔄 Tomas y Retomas"
])

# =========================================================
# TAB 1 - VENTAS
# =========================================================

with tab1:

    # =====================================================
    # KPIS
    # =====================================================

    ventas_totales = df_filtrado["Total Venta"].sum()
    margen_total = df_filtrado["Margen de Venta"].sum()
    cantidad_ventas = len(df_filtrado)
    ticket_promedio = ventas_totales / cantidad_ventas if cantidad_ventas > 0 else 0

    st.markdown("""
    <div style="
    background: linear-gradient(90deg,#0f172a,#1e293b);
    padding:30px;
    border-radius:24px;
    margin-bottom:25px;
    border:1px solid #334155;
    box-shadow:0 8px 30px rgba(0,0,0,0.35);
    ">

    <h1 style="
    color:white;
    margin:0;
    font-size:20px;
    font-weight:200;
    ">
    📈 Análisis de ventas, vendedores, sucursales y rendimiento comercial
    </h1> 
                
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric(
        "💰 Ventas Totales",
        f"${ventas_totales:,.0f}".replace(",", ".")
    )

    col2.metric(
        "📈 Margen Total",
        f"${margen_total:,.0f}".replace(",", ".")
    )

    col3.metric(
        "🚘 Cantidad",
        f"{cantidad_ventas:,.0f}".replace(",", ".")
    )

    col4.metric(
        "🏷️ Ticket Promedio",
        f"${ticket_promedio:,.0f}".replace(",", ".")
    )

    st.markdown("---")

    # =====================================================
    # GRAFICO DINAMICO
    # =====================================================

    st.markdown("""
    <h3 style="
    margin-top:10px;
    margin-bottom:20px;
    font-size:28px;
    font-weight:700;
    ">
    📈 Evolución Comercial
    </h3>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # SELECTOR
    # ---------------------------------------------------

    tipo_grafico = st.selectbox(
        "Selecciona indicador",
        [
            "Total Venta",
            "N° Vehículos",
            "Margen de Venta"
        ]
    )

    # =====================================================
    # TOTAL VENTA
    # =====================================================

    if tipo_grafico == "Total Venta":

        evolucion = (
        df_filtrado.groupby(["Mes", "Año"])["Total Venta"]
        .sum()
        .reset_index()
    )

        fig = px.line(
        evolucion,
        x="Mes",
        y="Total Venta",
        color="Año",
        markers=True
    )

    # =====================================================
    # VEHICULOS
    # =====================================================

    elif tipo_grafico == "N° Vehículos":

        vehiculos = (
            df_filtrado.groupby(["Mes", "Año"])["Placa Patente"]
            .nunique()
            .reset_index(name="Cantidad")
        )

        fig = px.line(
            vehiculos,
            x="Mes",
            y="Cantidad",
            color="Año",
            markers=True
        )

    # =====================================================
    # MARGEN
    # =====================================================

    else:

        margen = (
            df_filtrado.groupby(["Mes", "Año"])["Margen de Venta"]
            .mean()
            .reset_index()
        )

        fig = px.line(
            margen,
            x="Mes",
            y="Margen de Venta",
            color="Año",
            markers=True
        )

    # =====================================================
    # ESTILO GRAFICO
    # =====================================================

    fig.update_layout(

        height=550,

        plot_bgcolor="rgba(17,24,39,0.85)",
        paper_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white",
            size=14
        ),

        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont=dict(color="white")
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont=dict(color="white")
        )
    )

    fig.update_traces(
        line=dict(width=4),
        marker=dict(size=8)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # =====================================================
    # RENDIMIENTO VENDEDOR
    # =====================================================

    st.markdown("---")

    st.subheader("🧑 Rendimiento por Vendedor")

    lista_vendedores = sorted(
        df_filtrado["Vendedor"]
        .dropna()
        .unique()
    )

    lista_vendedores.insert(0, "TODOS")

    vendedor_select = st.selectbox(
        "Selecciona Vendedor",
        lista_vendedores
    )

    if vendedor_select == "TODOS":

        df_vendedor = df_filtrado.copy()

    else:

        df_vendedor = df_filtrado[
            df_filtrado["Vendedor"]
            == vendedor_select
        ]

    ventas_vendedor = df_vendedor["Total Venta"].sum()

    margen_vendedor = df_vendedor["Margen de Venta"].sum()

    cantidad_vendedor = len(df_vendedor)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Ventas",
        f"${ventas_vendedor:,.0f}".replace(",", ".")
    )

    col2.metric(
        "📈 Margen",
        f"${margen_vendedor:,.0f}".replace(",", ".")
    )

    col3.metric(
        "🚘 Cantidad",
        f"{cantidad_vendedor:,.0f}".replace(",", ".")
    )

    ventas_marca = (
        df_vendedor.groupby("Marca")["Total Venta"]
        .sum()
        .reset_index()
        .sort_values(
            by="Total Venta",
            ascending=False
        )
        .head(10)
    )

    fig_vendedor = px.bar(
        ventas_marca,
        x="Marca",
        y="Total Venta",
        color="Total Venta",
        text_auto=".2s"
    )

    fig_vendedor.update_layout(

        height=500,

        plot_bgcolor="#111827",
        paper_bgcolor="#111827",

        font=dict(
            color="white",
            size=14
        ),

        xaxis=dict(
            showgrid=False,
            tickfont=dict(
                color="white",
                size=12
            )
        ),

        yaxis=dict(
            showgrid=False,
            tickfont=dict(
                color="white",
                size=12
            )
        )
    )

    st.plotly_chart(
        fig_vendedor,
        use_container_width=True
    )
    cantidad_marca = (
    df_vendedor.groupby("Marca")
    .size()
    .reset_index(name="Cantidad")
    .sort_values(by="Cantidad", ascending=False)
    .head(10)
)

    fig_cantidad = px.bar(
    cantidad_marca,
    x="Marca",
    y="Cantidad",
    color="Cantidad",
    text_auto=True
)

    st.subheader("🚘 Cantidad de Autos por Marca")

    st.plotly_chart(
    fig_cantidad,
    use_container_width=True
)
    st.subheader("📋 Detalle de Ventas")

    tabla_detalle = df_vendedor[[
    "Vendedor",
    "Marca",
    "Modelo",
    "Placa Patente",
    "Año Auto",
    "Total Venta",
    "Margen de Venta"
]]

    st.dataframe(
    tabla_detalle.sort_values(by="Total Venta", ascending=False),
    use_container_width=True
)   

    # =====================================================
    # TOP VENDEDORES + SUCURSALES
    # =====================================================

    top_vendedores = (
        df_filtrado.groupby("Vendedor")["Total Venta"]
        .sum()
        .reset_index()
        .sort_values(by="Total Venta", ascending=False)
        .head(10)
    )

    fig_top = px.bar(
        top_vendedores,
        x="Total Venta",
        y="Vendedor",
        orientation="h",
        color="Total Venta",
        text_auto=".2s",
        template="plotly_dark"
    )

    fig_top.update_traces(
        textfont_size=13,
        marker_line_width=0
    )

    fig_top.update_layout(
        height=450,
        plot_bgcolor="rgba(17,24,39,0.85)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="white",
            size=13
        ),
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        coloraxis_showscale=False,
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color="white")
        )
    )

    ventas_sucursal = (
        df_filtrado.groupby("Sucursal")
        .size()
        .reset_index(name="Cantidad Ventas")
    )

    fig_sucursal = px.bar(
        ventas_sucursal,
        x="Sucursal",
        y="Cantidad Ventas",
        color="Cantidad Ventas",
        text_auto=True,
        template="plotly_dark"
    )

    fig_sucursal.update_traces(
        marker_line_width=0
    )

    fig_sucursal.update_layout(
        height=450,
        plot_bgcolor="rgba(17,24,39,0.85)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="white",
            size=13
        ),
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        coloraxis_showscale=False,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            tickfont=dict(color="white")
        )
    )

    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:

        st.markdown(
            """
            <h3 style="
            margin-bottom:15px;
            font-size:24px;
            font-weight:700;
            ">
            👨‍💼 Top Vendedores
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig_top,
            use_container_width=True
        )

    with col_graf2:

        st.markdown(
            """
            <h3 style="
            margin-bottom:15px;
            font-size:24px;
            font-weight:700;
            ">
            🏢 Ventas por Sucursal
            </h3>
            """,
            unsafe_allow_html=True
        )
    
        st.plotly_chart(
            fig_sucursal,
            use_container_width=True
        )
    
    

# =========================================================
# TAB 2 - STOCK Y PRICING
# =========================================================

with tab2:

    # ==========================================
# KPIs STOCK
# ==========================================

    stock_total = len(df_stock)

    stock_disponible = len(
    df_stock[
        df_stock["Estado Dealer"]
        .astype(str)
        .str.upper()
        .str.contains("DISPONIBLE", na=False)
    ]
    )

    stock_taller = len(
    df_stock[
        df_stock["Estado Dealer"]
        .astype(str)
        .str.upper()
        .str.contains("TALLER", na=False)
    ]
    )

    stock_no_disponible = len(
        df_stock[
        df_stock["Estado Dealer"]
        .astype(str)
        .str.upper()
        .str.contains("NO DISPONIBLE", na=False)
        ]
    )

    st.subheader("🚗 Estado del Stock")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
    "🚗 Stock Total",
    f"{stock_total:,.0f}".replace(",", ".")
    )

    col2.metric(
    "🟢 Disponible",
    f"{stock_disponible:,.0f}".replace(",", ".")
    )

    col3.metric(
    "🟠 En Taller",
    f"{stock_taller:,.0f}".replace(",", ".")
    )

    col4.metric(
    "🔴 No Disponible",
    f"{stock_no_disponible:,.0f}".replace(",", ".")
    )

    st.markdown("---")

    st.subheader("💡 Pricing Automático")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        marca_pricing = st.selectbox(
            "Marca",
            sorted(df_stock["Marca"].dropna().unique())
        )

    with col2:

        modelo_pricing = st.selectbox(
            "Modelo",
            sorted(
                df_stock[
                    df_stock["Marca"]
                    == marca_pricing
                ]["Modelo"]
                .dropna()
                .astype(str)
                .unique()
            )
        )

    with col3:

        año_pricing = st.selectbox(
            "Año",
            sorted(
                df_stock[
                    (
                        df_stock["Marca"]
                        == marca_pricing
                    )
                    &
                    (
                        df_stock["Modelo"]
                        .astype(str)
                        == str(modelo_pricing)
                    )
                ]["Año"]
                .dropna()
                .unique()
            )
        )

    with col4:

        version_pricing = st.selectbox(
            "Versión",
            sorted(
                df_stock[
                    (
                        df_stock["Marca"]
                        == marca_pricing
                    )
                    &
                    (
                        df_stock["Modelo"]
                        .astype(str)
                        == str(modelo_pricing)
                    )
                    &
                    (
                        df_stock["Año"]
                        == año_pricing
                    )
                ]["Versión"]
                .dropna()
                .astype(str)
                .unique()
            )
        )

    resultado = df_stock[
        (
            df_stock["Marca"]
            == marca_pricing
        )
        &
        (
            df_stock["Modelo"]
            .astype(str)
            == str(modelo_pricing)
        )
        &
        (
            df_stock["Año"]
            == año_pricing
        )
        &
        (
            df_stock["Versión"]
            .astype(str)
            == str(version_pricing)
        )
    ]

    if not resultado.empty:

        fila = resultado.iloc[0]

        lista = fila["Precio Lista informe stock"]
        mercado = fila["Precio Mercado"]
        toma = fila["Precio toma historico autored"]
        dias = fila["Suma de Días Stock"]

        if dias <= 30:

            venta_sugerida = mercado * 1.02
            toma_sugerida = toma * 1.02

        elif dias <= 90:

            venta_sugerida = mercado * 0.98
            toma_sugerida = toma * 1.00

        else:

            venta_sugerida = mercado * 0.95
            toma_sugerida = toma * 1.05

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "🏷️ Precio Lista",
            f"${lista:,.0f}".replace(",", ".")
        )

        col2.metric(
            "🌎 Precio Mercado",
            f"${mercado:,.0f}".replace(",", ".")
        )

        col3.metric(
            "📉 Precio Toma",
            f"${toma:,.0f}".replace(",", ".")
        )

        st.markdown("")

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "🔵 Toma Sugerida",
            f"${toma_sugerida:,.0f}".replace(",", ".")
        )

        col5.metric(
            "⏳ Días Stock",
            f"{dias:,.0f}".replace(",", ".")
        )

        col6.metric(
            "🔥 Venta Sugerida",
            f"${venta_sugerida:,.0f}".replace(",", ".")
        )

    st.markdown("---")

    # =====================================================
    # ALERTAS STOCK
    # =====================================================

    st.subheader("🚨 Riesgo y Obsolescencia")

    def alerta_stock(dias):

        if pd.isna(dias):
            return "⚪ Sin Datos"

        elif dias >= 120:
            return "🔴 Crítico"

        elif dias >= 60:
            return "🟠 Riesgo"

        else:
            return "🟢 Saludable"

    df_stock["Alerta"] = (
        df_stock["Suma de Días Stock"]
        .apply(alerta_stock)
    )

    riesgo_stock = df_stock[
        df_stock["Suma de Días Stock"].notna()
    ]

    buscar_patente = st.text_input(
        "🔎 Buscar Patente"
    )

    if buscar_patente:

        riesgo_stock = riesgo_stock[
            riesgo_stock["Placa Patente"]
            .astype(str)
            .str.contains(
                buscar_patente,
                case=False,
                na=False
            )
        ]

    patentes_excluir = st.multiselect(

        "🚫 Excluir Patentes",

        sorted(
            riesgo_stock["Placa Patente"]
            .dropna()
            .astype(str)
            .unique()
        )
    )

    if patentes_excluir:

        riesgo_stock = riesgo_stock[
            ~riesgo_stock["Placa Patente"]
            .astype(str)
            .isin(patentes_excluir)
        ]

    riesgo_stock["Suma de Días Stock"] = (
        riesgo_stock["Suma de Días Stock"]
        .fillna(0)
        .astype(int)
    )

    tabla_final = riesgo_stock[
        [
            "Marca",
            "Modelo",
            "Versión",
            "Placa Patente",
            "Suma de Días Stock",
            "Precio Lista informe stock",
            "Precio Mercado",
            "Precio toma historico autored",
            "Alerta"
        ]
    ].sort_values(
        by="Suma de Días Stock",
        ascending=False
    )

    st.dataframe(
        tabla_final,
        use_container_width=True
    )

# =========================================================
# TAB 3 - TOMAS Y RETOMAS
# =========================================================

with tab3:

    st.markdown("""
    <div style="
    background: linear-gradient(90deg,#0f172a,#1e293b);
    padding:30px;
    border-radius:24px;
    margin-bottom:25px;
    border:1px solid #334155;
    ">
    <h1 style="
    color:white;
    margin:0;
    font-size:20px;
    font-weight:200;
    ">
    🔄 Tasaciones, Peritajes y Tomas
    </h1>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
# KPIs
# =====================================================

    total_tasaciones = len(df_tas_filtrado)
    total_peritajes = len(df_per_filtrado)
    total_tomas = len(df_toma_filtrado)

    valor_tomas = pd.to_numeric(
    df_toma_filtrado["Precio"],
    errors="coerce"
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📋 Tasaciones",
        f"{total_tasaciones:,.0f}".replace(",", ".")
    )

    col2.metric(
        "🔎 Peritajes",
        f"{total_peritajes:,.0f}".replace(",", ".")
    )

    col3.metric(
        "🚘 Tomas",
        f"{total_tomas:,.0f}".replace(",", ".")
    )

    col4.metric(
        "💰 Valor Tomado",
        f"${valor_tomas:,.0f}".replace(",", ".")
    )

# =====================================================
# FUNNEL
# =====================================================

    st.markdown("---")
    st.subheader("🔄 Funnel Comercial")

    import plotly.graph_objects as go

    funnel = go.Figure(go.Funnel(
        y=[
            "Tasaciones",
            "Peritajes",
            "Tomas"
        ],
        x=[
            total_tasaciones,
            total_peritajes,
            total_tomas
        ]
    ))

    funnel.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(
        funnel,
        use_container_width=True
    )

# =====================================================
# CONVERSIONES
# =====================================================

    st.markdown("---")
    st.subheader("🎯 Conversión por Etapa")

    conversion_peritaje = (
        total_peritajes / total_tasaciones * 100
        if total_tasaciones > 0 else 0  
    )

    conversion_toma = (
        total_tomas / total_peritajes * 100
        if total_peritajes > 0 else 0
    )

    conversion_total = (
        total_tomas / total_tasaciones * 100
        if total_tasaciones > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Tasación ➜ Peritaje",
        f"{conversion_peritaje:.1f}%"
    )

    col2.metric(
        "Peritaje ➜ Toma",
        f"{conversion_toma:.1f}%"
    )

    col3.metric(
        "Tasación ➜ Toma",
        f"{conversion_total:.1f}%"
    )

    # =====================================================
    # GESTIÓN POR SUCURSAL
    # =====================================================

    st.markdown("---")
    st.subheader("🏢 Gestión por Sucursal")

    tipo_sucursal = st.selectbox(
        "Indicador",
        [
            "Tasaciones",
            "Peritajes",
            "Tomas"
        ],
        key="sucursal_tab3"
    )

    if tipo_sucursal == "Tasaciones":

        datos_sucursal = (
            df_tas_filtrado.groupby("Sucursal")
            .size()
            .reset_index(name="Cantidad")
            .sort_values("Cantidad", ascending=False)
        )

    elif tipo_sucursal == "Peritajes":

        datos_sucursal = (
            df_per_filtrado.groupby("Sucursal")
            .size()
            .reset_index(name="Cantidad")
            .sort_values("Cantidad", ascending=False)
        )

    else:

        datos_sucursal = (
            df_toma_filtrado.groupby("Sucursal")
            .size()
            .reset_index(name="Cantidad")
            .sort_values("Cantidad", ascending=False)
        )

    fig_sucursal = px.bar(
        datos_sucursal,
        x="Sucursal",
        y="Cantidad",
        color="Cantidad",
        text_auto=True
    )

    fig_sucursal.update_layout(
        height=550,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.85)",
        font=dict(color="white")
    )

    st.plotly_chart(
        fig_sucursal,
        use_container_width=True
    )

    # =====================================================
    # TOP VENDEDORES
    # =====================================================

    st.markdown("---")
    st.subheader("👨‍💼 Top Vendedores")

    tipo_vendedor = st.selectbox(
        "Indicador vendedor",
        [
            "Tasaciones",
            "Peritajes",
            "Tomas"
        ],
        key="vendedores_tab3"
    )

    if tipo_vendedor == "Tasaciones":

        datos_vendedor = (
            df_tas_filtrado.groupby("Vendedor")
            .size()
            .reset_index(name="Cantidad")
            .sort_values("Cantidad", ascending=False)
            .head(15)
        )

    elif tipo_vendedor == "Peritajes":

        datos_vendedor = (
            df_per_filtrado.groupby("Vendedor")
            .size()
            .reset_index(name="Cantidad")
            .sort_values("Cantidad", ascending=False)
            .head(15)
        )

    else:

        datos_vendedor = (
            df_toma_filtrado.groupby("Vendedor")
            .size()
            .reset_index(name="Cantidad")
            .sort_values("Cantidad", ascending=False)
            .head(15)
        )

    fig_vendedor = px.bar(
        datos_vendedor,
        x="Cantidad",
        y="Vendedor",
        orientation="h",
        color="Cantidad",
        text_auto=True
    )

    fig_vendedor.update_layout(
        height=600,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.85)",
        font=dict(color="white")
    )

    st.plotly_chart(
        fig_vendedor,
        use_container_width=True
    )

    # =====================================================
    # TOP MARCAS
    # =====================================================

    st.markdown("---")
    st.subheader("🚗 Top Marcas")

    tipo_marca = st.selectbox(
        "Indicador marca",
        [
            "Tasaciones",
            "Tomas"
        ],
        key="marcas_tab3"
    )

    if tipo_marca == "Tasaciones":

        datos_marca = (
            df_tas_filtrado.groupby("Marca")
            .size()
            .reset_index(name="Cantidad")
            .sort_values("Cantidad", ascending=False)
            .head(10)
        )

    else:

        datos_marca = (
            df_toma_filtrado.groupby("Marca")
            .size()
            .reset_index(name="Cantidad")
            .sort_values("Cantidad", ascending=False)
            .head(10)
        )

    fig_marca = px.bar(
        datos_marca,
        x="Cantidad",
        y="Marca",
        orientation="h",
        color="Cantidad",
        text_auto=True
    )

    fig_marca.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.85)",
        font=dict(color="white")
    )

    st.plotly_chart(
        fig_marca,
        use_container_width=True
    )