import os
from html import escape
from urllib.parse import quote_plus

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine


ACCENT_COLOR = "#0f766e"
INK_COLOR = "#18181b"
MUTED_COLOR = "#71717a"
PANEL_COLOR = "#ffffff"
BACKGROUND_COLOR = "#f9fafb"
BORDER_COLOR = "#e4e4e7"


st.set_page_config(
    page_title="Brewline Sales Analytics",
    layout="wide",
)


def inject_styles() -> None:
    st.markdown(
        f"""
        <style>
            :root {{
                --accent: {ACCENT_COLOR};
                --ink: {INK_COLOR};
                --muted: {MUTED_COLOR};
                --panel: {PANEL_COLOR};
                --background: {BACKGROUND_COLOR};
                --border: {BORDER_COLOR};
            }}

            .stApp {{
                background:
                    linear-gradient(135deg, rgba(15, 118, 110, 0.08), transparent 34rem),
                    var(--background);
                color: var(--ink);
                font-family: "Satoshi", "Geist", "Helvetica Neue", Arial, sans-serif;
            }}

            [data-testid="stHeader"] {{
                background: transparent;
            }}

            [data-testid="stSidebar"] {{
                background: rgba(255, 255, 255, 0.72);
                border-right: 1px solid rgba(228, 228, 231, 0.9);
            }}

            .block-container {{
                max-width: 1400px;
                padding-top: 2.2rem;
                padding-bottom: 4rem;
            }}

            .eyebrow {{
                color: var(--accent);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                margin-bottom: 0.8rem;
            }}

            .hero-title {{
                color: var(--ink);
                font-size: clamp(2.1rem, 4.7vw, 4.85rem);
                font-weight: 760;
                letter-spacing: -0.055em;
                line-height: 0.95;
                max-width: 10.5ch;
                margin: 0;
            }}

            .hero-copy {{
                color: #52525b;
                font-size: 1.03rem;
                line-height: 1.65;
                max-width: 58ch;
                margin-top: 1.25rem;
            }}

            .status-strip {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.65rem;
                margin-top: 1.35rem;
            }}

            .status-pill {{
                align-items: center;
                background: rgba(255, 255, 255, 0.74);
                border: 1px solid rgba(228, 228, 231, 0.96);
                border-radius: 999px;
                color: #3f3f46;
                display: inline-flex;
                font-size: 0.82rem;
                font-weight: 650;
                gap: 0.5rem;
                padding: 0.55rem 0.85rem;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.72);
            }}

            .pulse-dot {{
                width: 0.48rem;
                height: 0.48rem;
                border-radius: 999px;
                background: var(--accent);
                animation: breathe 2.4s cubic-bezier(0.16, 1, 0.3, 1) infinite;
            }}

            .metric-panel {{
                background: rgba(255, 255, 255, 0.82);
                border: 1px solid rgba(228, 228, 231, 0.95);
                border-radius: 1.5rem;
                box-shadow: 0 24px 60px -36px rgba(24, 24, 27, 0.32);
                padding: 1.2rem;
            }}

            .metric-grid {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.85rem;
            }}

            .metric-card {{
                background: var(--panel);
                border: 1px solid rgba(228, 228, 231, 0.86);
                border-radius: 1rem;
                padding: 1rem;
                transition: transform 260ms cubic-bezier(0.16, 1, 0.3, 1), border-color 260ms cubic-bezier(0.16, 1, 0.3, 1);
            }}

            .metric-card:hover {{
                border-color: rgba(15, 118, 110, 0.28);
                transform: translateY(-2px);
            }}

            .metric-label {{
                color: var(--muted);
                font-size: 0.74rem;
                font-weight: 680;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }}

            .metric-value {{
                color: var(--ink);
                font-family: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
                font-size: clamp(1.35rem, 2vw, 2rem);
                font-weight: 760;
                letter-spacing: -0.05em;
                margin-top: 0.55rem;
            }}

            .section-title {{
                color: var(--ink);
                font-size: 1.15rem;
                font-weight: 760;
                letter-spacing: -0.03em;
                margin: 0 0 0.15rem 0;
            }}

            .section-copy {{
                color: var(--muted);
                font-size: 0.92rem;
                line-height: 1.55;
                margin: 0 0 1rem 0;
            }}

            .panel {{
                background: rgba(255, 255, 255, 0.86);
                border: 1px solid rgba(228, 228, 231, 0.9);
                border-radius: 1.25rem;
                box-shadow: 0 18px 50px -34px rgba(24, 24, 27, 0.38);
                padding: 1rem 1rem 0.45rem;
            }}

            .state-box {{
                background: rgba(255, 255, 255, 0.86);
                border: 1px solid rgba(228, 228, 231, 0.95);
                border-radius: 1.25rem;
                padding: 1.4rem;
                box-shadow: 0 18px 50px -34px rgba(24, 24, 27, 0.36);
            }}

            .state-title {{
                color: var(--ink);
                font-size: 1.25rem;
                font-weight: 760;
                letter-spacing: -0.03em;
                margin-bottom: 0.4rem;
            }}

            .state-copy {{
                color: #52525b;
                line-height: 1.6;
                margin: 0;
            }}

            .skeleton {{
                background: linear-gradient(90deg, #f4f4f5, #ffffff, #f4f4f5);
                background-size: 220% 100%;
                border: 1px solid rgba(228, 228, 231, 0.9);
                border-radius: 1rem;
                height: 7.5rem;
                animation: shimmer 1.35s cubic-bezier(0.16, 1, 0.3, 1) infinite;
            }}

            .stButton > button {{
                border-radius: 999px;
                border: 1px solid rgba(15, 118, 110, 0.22);
                color: var(--ink);
                transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1), border-color 180ms cubic-bezier(0.16, 1, 0.3, 1);
            }}

            .stButton > button:active {{
                transform: scale(0.98) translateY(1px);
            }}

            @keyframes shimmer {{
                0% {{ background-position: 120% 0; }}
                100% {{ background-position: -120% 0; }}
            }}

            @keyframes breathe {{
                0%, 100% {{ opacity: 0.52; transform: scale(0.82); }}
                50% {{ opacity: 1; transform: scale(1.08); }}
            }}

            @media (max-width: 768px) {{
                .block-container {{
                    padding-left: 1rem;
                    padding-right: 1rem;
                    padding-top: 1.25rem;
                }}

                .hero-title {{
                    max-width: 12ch;
                }}

                .metric-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_secret_config() -> dict[str, str]:
    try:
        if "postgres" in st.secrets:
            return dict(st.secrets["postgres"])
    except Exception:
        return {}

    return {}


def build_database_url() -> str:
    db_config = get_secret_config()

    user = db_config.get("user") or os.getenv("POSTGRES_USER", "coffee_user")
    password = db_config.get("password") or os.getenv("POSTGRES_PASSWORD", "coffee_password")
    host = db_config.get("host") or os.getenv("POSTGRES_HOST", "localhost")
    port = db_config.get("port") or os.getenv("POSTGRES_PORT", "5433")
    database = db_config.get("database") or os.getenv("POSTGRES_DB", "coffee_sales_db")
    sslmode = db_config.get("sslmode") or os.getenv("POSTGRES_SSLMODE", "prefer")

    return (
        f"postgresql+psycopg2://{quote_plus(str(user))}:"
        f"{quote_plus(str(password))}@{host}:"
        f"{port}/{quote_plus(str(database))}?sslmode={quote_plus(str(sslmode))}"
    )


@st.cache_resource(show_spinner=False)
def get_engine():
    return create_engine(build_database_url())


@st.cache_data(show_spinner=False)
def load_sales_data() -> pd.DataFrame:
    query = """
        SELECT
            transaction_id,
            transaction_date,
            transaction_time,
            transaction_qty,
            store_id,
            store_location,
            product_id,
            unit_price,
            product_category,
            product_type,
            product_detail,
            total_amount,
            year,
            month,
            day,
            day_name,
            loaded_at
        FROM sales;
    """

    engine = get_engine()
    df = pd.read_sql_query(query, engine)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["total_amount"] = pd.to_numeric(df["total_amount"])
    df["transaction_qty"] = pd.to_numeric(df["transaction_qty"])
    return df


def show_loading_state() -> None:
    cols = st.columns([1.15, 0.85])
    with cols[0]:
        st.markdown('<div class="skeleton"></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<div class="skeleton"></div>', unsafe_allow_html=True)


def show_error_state(error: Exception) -> None:
    error_message = escape(str(error))
    st.markdown(
        f"""
        <div class="state-box">
            <div class="state-title">Database connection needs attention</div>
            <p class="state-copy">
                The dashboard could not read the sales table. Check your Streamlit secrets,
                Neon host, SSL mode, and whether the Airflow load step has created the
                <code>sales</code> table. Details: <code>{error_message}</code>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_empty_state() -> None:
    st.markdown(
        """
        <div class="state-box">
            <div class="state-title">No sales rows found</div>
            <p class="state-copy">
                Run the Airflow DAG first so the cleaned Excel records are loaded into PostgreSQL.
                After the table is populated, refresh this dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_money(value: float) -> str:
    return f"${value:,.2f}"


def format_number(value: float) -> str:
    return f"{value:,.0f}"


def metric_card(label: str, value: str) -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """


def render_header(df: pd.DataFrame) -> None:
    total_sales = df["total_amount"].sum()
    total_transactions = df["transaction_id"].nunique()
    items_sold = df["transaction_qty"].sum()
    avg_order = total_sales / total_transactions if total_transactions else 0
    latest_load = pd.to_datetime(df["loaded_at"]).max()

    left, right = st.columns([1.24, 0.76], gap="large")
    with left:
        st.markdown(
            """
            <div class="eyebrow">Airflow to PostgreSQL to Streamlit</div>
            <h1 class="hero-title">Retail sales intelligence.</h1>
            <p class="hero-copy">
                A compact operating dashboard for tracking revenue, product demand,
                store performance, and daily transaction rhythm from the ETL pipeline.
            </p>
            <div class="status-strip">
                <div class="status-pill"><span class="pulse-dot"></span> PostgreSQL connected</div>
                <div class="status-pill">Cloud deployment ready</div>
                <div class="status-pill">Filtered views below</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="metric-panel">
                <div class="metric-grid">
                    {metric_card("Total sales", format_money(total_sales))}
                    {metric_card("Transactions", format_number(total_transactions))}
                    {metric_card("Items sold", format_number(items_sold))}
                    {metric_card("Avg order", format_money(avg_order))}
                </div>
                <p class="section-copy" style="margin: 1rem 0 0 0;">
                    Last loaded: {latest_load.strftime("%Y-%m-%d %H:%M") if pd.notna(latest_load) else "Not available"}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def filter_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown("### Filters")

    min_date = df["transaction_date"].min().date()
    max_date = df["transaction_date"].max().date()
    selected_dates = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    stores = sorted(df["store_location"].dropna().unique())
    categories = sorted(df["product_category"].dropna().unique())

    selected_stores = st.sidebar.multiselect("Store locations", stores, default=stores)
    selected_categories = st.sidebar.multiselect("Product categories", categories, default=categories)

    filtered_df = df.copy()
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered_df = filtered_df[
            (filtered_df["transaction_date"].dt.date >= start_date)
            & (filtered_df["transaction_date"].dt.date <= end_date)
        ]

    if selected_stores:
        filtered_df = filtered_df[filtered_df["store_location"].isin(selected_stores)]

    if selected_categories:
        filtered_df = filtered_df[filtered_df["product_category"].isin(selected_categories)]

    return filtered_df


def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Satoshi, Geist, Helvetica Neue, Arial, sans-serif", "color": INK_COLOR},
        margin={"l": 8, "r": 8, "t": 18, "b": 8},
        hoverlabel={"bgcolor": "#ffffff", "bordercolor": BORDER_COLOR, "font_size": 13},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "left", "x": 0},
    )
    fig.update_xaxes(showgrid=False, zeroline=False, color=MUTED_COLOR)
    fig.update_yaxes(gridcolor="rgba(228, 228, 231, 0.74)", zeroline=False, color=MUTED_COLOR)
    return fig


def render_charts(df: pd.DataFrame) -> None:
    daily_sales = (
        df.groupby("transaction_date", as_index=False)
        .agg(total_sales=("total_amount", "sum"), transactions=("transaction_id", "count"))
        .sort_values("transaction_date")
    )
    category_sales = (
        df.groupby("product_category", as_index=False)
        .agg(total_sales=("total_amount", "sum"), items_sold=("transaction_qty", "sum"))
        .sort_values("total_sales", ascending=False)
    )
    store_sales = (
        df.groupby("store_location", as_index=False)
        .agg(total_sales=("total_amount", "sum"), transactions=("transaction_id", "count"))
        .sort_values("total_sales", ascending=True)
    )
    top_products = (
        df.groupby(["product_detail", "product_category"], as_index=False)
        .agg(total_sales=("total_amount", "sum"), items_sold=("transaction_qty", "sum"))
        .sort_values("total_sales", ascending=False)
        .head(12)
    )

    st.markdown("<br>", unsafe_allow_html=True)
    trend_col, category_col = st.columns([1.35, 0.65], gap="large")

    with trend_col:
        st.markdown(
            '<div class="panel"><p class="section-title">Daily revenue rhythm</p>'
            '<p class="section-copy">Revenue and transaction movement across the selected window.</p>',
            unsafe_allow_html=True,
        )
        fig = px.line(
            daily_sales,
            x="transaction_date",
            y="total_sales",
            markers=True,
            color_discrete_sequence=[ACCENT_COLOR],
        )
        fig.update_traces(line={"width": 3}, marker={"size": 5})
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with category_col:
        st.markdown(
            '<div class="panel"><p class="section-title">Category mix</p>'
            '<p class="section-copy">Share of revenue by product family.</p>',
            unsafe_allow_html=True,
        )
        fig = px.bar(
            category_sales,
            x="total_sales",
            y="product_category",
            orientation="h",
            color="total_sales",
            color_continuous_scale=["#ccfbf1", ACCENT_COLOR],
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    store_col, product_col = st.columns([0.74, 1.26], gap="large")

    with store_col:
        st.markdown(
            '<div class="panel"><p class="section-title">Store performance</p>'
            '<p class="section-copy">Location revenue across the selected filters.</p>',
            unsafe_allow_html=True,
        )
        fig = px.bar(
            store_sales,
            x="total_sales",
            y="store_location",
            orientation="h",
            color_discrete_sequence=[ACCENT_COLOR],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with product_col:
        st.markdown(
            '<div class="panel"><p class="section-title">Top products</p>'
            '<p class="section-copy">Highest-grossing menu items with category context.</p>',
            unsafe_allow_html=True,
        )
        fig = px.bar(
            top_products.sort_values("total_sales"),
            x="total_sales",
            y="product_detail",
            color="product_category",
            orientation="h",
            color_discrete_sequence=["#0f766e", "#334155", "#64748b", "#14b8a6", "#475569"],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_data_table(df: pd.DataFrame) -> None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="panel"><p class="section-title">Transaction sample</p>'
        '<p class="section-copy">Recent rows from the filtered dataset for quick inspection.</p>',
        unsafe_allow_html=True,
    )
    columns = [
        "transaction_id",
        "transaction_date",
        "store_location",
        "product_category",
        "product_detail",
        "transaction_qty",
        "unit_price",
        "total_amount",
    ]
    st.dataframe(
        df.sort_values("transaction_date", ascending=False)[columns].head(200),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    inject_styles()

    loading_placeholder = st.empty()
    with loading_placeholder.container():
        show_loading_state()

    try:
        df = load_sales_data()
    except Exception as error:
        loading_placeholder.empty()
        show_error_state(error)
        return

    loading_placeholder.empty()

    if df.empty:
        show_empty_state()
        return

    filtered_df = filter_sales_data(df)

    if filtered_df.empty:
        render_header(df)
        show_empty_state()
        return

    render_header(filtered_df)
    render_charts(filtered_df)
    render_data_table(filtered_df)


if __name__ == "__main__":
    main()
