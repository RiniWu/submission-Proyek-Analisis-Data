import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium

from pathlib import Path
from streamlit_folium import st_folium


# ============================================================
# 1. KONFIGURASI DASHBOARD
# ============================================================

st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

# Lokasi folder dashboard/
DASHBOARD_DIR = Path(__file__).resolve().parent

# Lokasi folder utama project
PROJECT_DIR = DASHBOARD_DIR.parent

# main_data.csv berada di dashboard/
MAIN_DATA_PATH = DASHBOARD_DIR / "main_data.csv"

# state_geo.csv berada di data/
STATE_GEO_PATH = PROJECT_DIR / "data" / "state_geo.csv"

BLUE = "#3B6F89"
RED = "#B44B40"
GRAY = "#C2C6CA"
ORANGE = "#E67E22"


# ============================================================
# 2. MEMUAT DATA HASIL CLEANING COLAB
# ============================================================

@st.cache_data
def load_data():
    main_df = pd.read_csv(MAIN_DATA_PATH)
    state_geo = pd.read_csv(STATE_GEO_PATH)

    # Menangani variasi nama kolom kategori
    if "product_category" not in main_df.columns:
        if "product_category_name_english" in main_df.columns:
            main_df = main_df.rename(
                columns={
                    "product_category_name_english": "product_category"
                }
            )
        elif "product_category_name" in main_df.columns:
            main_df = main_df.rename(
                columns={
                    "product_category_name": "product_category"
                }
            )

    # Konversi tipe data tanggal
    date_cols = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for col in date_cols:
        if col in main_df.columns:
            main_df[col] = pd.to_datetime(
                main_df[col],
                errors="coerce"
            )

    # Konversi tipe data numerik
    numeric_cols = [
        "price",
        "delivery_days",
        "review_score"
    ]

    for col in numeric_cols:
        if col in main_df.columns:
            main_df[col] = pd.to_numeric(
                main_df[col],
                errors="coerce"
            )

    # Konversi status keterlambatan
    if "is_late" in main_df.columns:
        main_df["is_late"] = (
            main_df["is_late"]
            .astype("string")
            .str.strip()
            .str.lower()
            .map({
                "true": True,
                "false": False,
                "1": True,
                "0": False
            })
        )

    # Konversi koordinat geospasial
    for col in ["lat", "lng"]:
        if col in state_geo.columns:
            state_geo[col] = pd.to_numeric(
                state_geo[col],
                errors="coerce"
            )

    return main_df, state_geo


try:
    # Periksa keberadaan file sebelum membaca dataset
    missing_files = [
        str(path)
        for path in [MAIN_DATA_PATH, STATE_GEO_PATH]
        if not path.is_file()
    ]

    if missing_files:
        raise FileNotFoundError(
            "File tidak ditemukan: " + ", ".join(missing_files)
        )

    main_df, state_geo = load_data()

except (FileNotFoundError, pd.errors.EmptyDataError) as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.info(
        "Pastikan main_data.csv berada di folder dashboard "
        "dan state_geo.csv berada di folder data."
    )
    st.stop()


# ============================================================
# 3. VALIDASI DATA
# ============================================================

required_cols = [
    "order_id",
    "customer_unique_id",
    "order_purchase_timestamp",
    "price",
    "product_category",
    "customer_state",
    "delivery_days",
    "review_score",
    "is_late"
]

missing_cols = [
    col for col in required_cols
    if col not in main_df.columns
]

if missing_cols:
    st.error(
        "Kolom berikut belum ditemukan pada main_data.csv: "
        + ", ".join(missing_cols)
    )
    st.stop()


# Periode analisis sesuai notebook
main_df = main_df[
    main_df["order_purchase_timestamp"].between(
        pd.Timestamp("2017-01-01"),
        pd.Timestamp("2018-09-01"),
        inclusive="left"
    )
].copy()

if main_df.empty:
    st.error(
        "Tidak ada data pada periode Januari 2017–Agustus 2018."
    )
    st.stop()


# ============================================================
# 3B. FILTER INTERAKTIF (SIDEBAR)
# ============================================================

st.sidebar.header("Filter Data")

min_date = main_df["order_purchase_timestamp"].min().date()
max_date = main_df["order_purchase_timestamp"].max().date()

date_range = st.sidebar.date_input(
    "Rentang tanggal pembelian",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if not (isinstance(date_range, (tuple, list)) and len(date_range) == 2):
    st.info("Pilih tanggal awal dan tanggal akhir pada sidebar.")
    st.stop()

all_states = sorted(main_df["customer_state"].dropna().unique())
selected_states = st.sidebar.multiselect(
    "State pelanggan (kosong = semua)",
    options=all_states,
    default=[]
)

all_categories = sorted(main_df["product_category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Kategori produk (kosong = semua)",
    options=all_categories,
    default=[]
)

filter_mask = (
    (main_df["order_purchase_timestamp"].dt.date >= date_range[0])
    & (main_df["order_purchase_timestamp"].dt.date <= date_range[1])
)

if selected_states:
    filter_mask &= main_df["customer_state"].isin(selected_states)

if selected_categories:
    filter_mask &= main_df["product_category"].isin(selected_categories)

main_df = main_df[filter_mask].copy()

if main_df.empty:
    st.warning(
        "Tidak ada data untuk kombinasi filter yang dipilih. "
        "Ubah rentang tanggal, state, atau kategori pada sidebar."
    )
    st.stop()


# ============================================================
# 4. JUDUL DASHBOARD
# ============================================================

st.title("📊 Olist E-Commerce Analytics")

st.caption(
    "Analisis penjualan, performa pengiriman, segmentasi pelanggan, "
    "dan distribusi geografis Olist E-Commerce Brasil."
)

st.caption(
    f"Periode ditampilkan: {date_range[0]:%d %b %Y} – {date_range[1]:%d %b %Y} "
    f"(data tersedia: Januari 2017–Agustus 2018). "
    "Gunakan filter di sidebar untuk menyaring tanggal, state, dan kategori."
)


# ============================================================
# 5. KPI UTAMA
# ============================================================

st.header("Ringkasan Kinerja")

total_revenue = main_df["price"].sum()
total_orders = main_df["order_id"].nunique()
total_customers = main_df["customer_unique_id"].nunique()

order_level = main_df.drop_duplicates(
    subset=["order_id"]
).copy()

avg_review = order_level["review_score"].mean()
avg_delivery = order_level["delivery_days"].mean()
late_rate = order_level["is_late"].mean() * 100

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Revenue", f"R$ {total_revenue:,.0f}")
k2.metric("Total Pesanan", f"{total_orders:,}")
k3.metric("Pelanggan Unik", f"{total_customers:,}")
k4.metric(
    "Rata-rata Skor Review",
    f"{avg_review:.2f}/5" if pd.notna(avg_review) else "N/A"
)

st.divider()


# ============================================================
# 6. PERTANYAAN 1
# REVENUE KATEGORI PRODUK DAN PERTUMBUHAN
# ============================================================

st.header("1. Kategori Produk dan Pertumbuhan Revenue")

st.markdown(
    "Analisis kategori produk dengan revenue terbesar serta "
    "pertumbuhan revenue Januari–Agustus 2018 dibandingkan "
    "periode yang sama pada 2017."
)

revenue_category = (
    main_df.groupby("product_category")["price"]
    .sum()
    .sort_values(ascending=False)
)

top10 = revenue_category.head(10)

temp = main_df.copy()
temp["year"] = temp["order_purchase_timestamp"].dt.year
temp["month"] = temp["order_purchase_timestamp"].dt.month

ytd = temp[
    temp["year"].isin([2017, 2018])
    & temp["month"].between(1, 8)
].pivot_table(
    index="product_category",
    columns="year",
    values="price",
    aggfunc="sum",
    fill_value=0
)

for year in [2017, 2018]:
    if year not in ytd.columns:
        ytd[year] = 0

ytd["growth_pct"] = float("nan")
valid_growth = ytd[2017] > 0

ytd.loc[valid_growth, "growth_pct"] = (
    (
        ytd.loc[valid_growth, 2018]
        / ytd.loc[valid_growth, 2017]
    ) - 1
) * 100

growth_top10 = ytd.reindex(top10.index)
growth_top10 = growth_top10.sort_values(
    "growth_pct",
    ascending=False,
    na_position="last"
)


# 6A. TOP 10 REVENUE DAN PERTUMBUHAN

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Kategori berdasarkan Revenue")
    plot_revenue = top10.sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(9, 6))
    plot_revenue.plot(kind="barh", ax=ax, color=BLUE)

    ax.set_title("10 Kategori dengan Revenue Tertinggi", loc="left")
    ax.set_xlabel("Total Revenue (R$)")
    ax.set_ylabel("Kategori Produk")
    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)

    for i, value in enumerate(plot_revenue):
        ax.text(value, i, f"  {value / 1000:,.0f}K",
                va="center", fontsize=8)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("Pertumbuhan Revenue Top 10")

    plot_growth = (
        growth_top10["growth_pct"]
        .dropna()
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    if not plot_growth.empty:
        bar_colors = [
            RED if value < 0 else BLUE
            for value in plot_growth.values
        ]

        plot_growth.plot(kind="barh", ax=ax, color=bar_colors)
        ax.axvline(0, color="black", linewidth=0.8)

        for i, value in enumerate(plot_growth):
            ax.text(value, i, f"  {value:.0f}%",
                    va="center", fontsize=8)

    ax.set_title(
        "Pertumbuhan Jan–Agu 2018 vs Jan–Agu 2017",
        loc="left"
    )
    ax.set_xlabel("Pertumbuhan Revenue (%)")
    ax.set_ylabel("Kategori Produk")
    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# 6B. TREN REVENUE BULANAN

st.subheader("Tren Revenue Bulanan")

temp["order_month"] = (
    temp["order_purchase_timestamp"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

monthly_revenue = (
    temp.groupby("order_month")["price"]
    .sum()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o",
    linewidth=2,
    color=BLUE
)

ax.set_title("Tren Revenue Bulanan", loc="left")
ax.set_xlabel("Bulan")
ax.set_ylabel("Revenue (R$)")
ax.grid(alpha=0.25)
fig.autofmt_xdate()
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

with st.expander("Lihat detail revenue kategori"):
    revenue_table = pd.DataFrame({
        "Total Revenue (R$)": revenue_category
    })

    revenue_table["Kontribusi Revenue (%)"] = (
        revenue_table["Total Revenue (R$)"]
        / revenue_category.sum() * 100
    )

    revenue_table = revenue_table.sort_values(
        "Total Revenue (R$)", ascending=False
    )

    st.dataframe(
        revenue_table.style.format({
            "Total Revenue (R$)": "R$ {:,.2f}",
            "Kontribusi Revenue (%)": "{:.1f}%"
        }),
        use_container_width=True
    )

st.markdown(
    """
    **Insight Pertanyaan 1**

    Kategori dengan revenue terbesar menjadi prioritas untuk
    pengelolaan stok dan promosi. Pertumbuhan kategori perlu
    dibandingkan pada periode Januari–Agustus agar perbandingan
    antar-tahun menggunakan rentang bulan yang setara.
    """
)

st.caption(
    "Revenue dihitung dari price (harga barang), tanpa ongkos kirim. "
    "Kategori dengan revenue 2017 nol tidak memiliki persentase "
    "pertumbuhan yang dapat dihitung. Pertumbuhan hanya muncul jika "
    "filter tanggal mencakup Januari–Agustus 2017 dan 2018."
)

st.divider()


# ============================================================
# 7. PERTANYAAN 2
# WAKTU PENGIRIMAN DAN SKOR REVIEW
# ============================================================

st.header("2. Waktu Pengiriman dan Skor Review")

st.markdown(
    "Menganalisis perbedaan waktu pengiriman dan skor ulasan "
    "berdasarkan state pelanggan serta status keterlambatan."
)

state_stats = (
    order_level.groupby("customer_state")
    .agg(
        orders=("order_id", "nunique"),
        avg_delivery_days=("delivery_days", "mean"),
        avg_review=("review_score", "mean"),
        late_rate=("is_late", "mean")
    )
    .sort_values("avg_delivery_days", ascending=False)
)

state_stats["late_rate_pct"] = state_stats["late_rate"] * 100

c1, c2, c3 = st.columns(3)

c1.metric(
    "Rata-rata Pengiriman",
    f"{avg_delivery:.1f} hari" if pd.notna(avg_delivery) else "N/A"
)

c2.metric(
    "Pesanan Terlambat",
    f"{late_rate:.1f}%" if pd.notna(late_rate) else "N/A"
)

corr_data = state_stats[
    ["avg_delivery_days", "avg_review"]
].dropna()

corr_value = (
    corr_data["avg_delivery_days"].corr(corr_data["avg_review"])
    if len(corr_data) > 1 else float("nan")
)

c3.metric(
    "Korelasi Antar-State",
    f"{corr_value:.2f}" if pd.notna(corr_value) else "N/A"
)


# 7A. WAKTU PENGIRIMAN PER STATE

col1, col2 = st.columns(2)

with col1:
    st.subheader("Rata-rata Waktu Pengiriman per State")

    delivery_plot = (
        state_stats["avg_delivery_days"]
        .dropna()
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(9, 8))

    delivery_colors = [
        RED if value >= 22 else GRAY
        for value in delivery_plot.values
    ]

    delivery_plot.plot(kind="barh", ax=ax, color=delivery_colors)

    ax.axvline(
        avg_delivery,
        linestyle="--",
        color=BLUE,
        label=f"Rata-rata keseluruhan {avg_delivery:.1f} hari"
        if pd.notna(avg_delivery) else "Rata-rata keseluruhan"
    )

    ax.set_title("State dengan Pengiriman Terlama", loc="left")
    ax.set_xlabel("Rata-rata Waktu Pengiriman (hari)")
    ax.set_ylabel("State Pelanggan")
    ax.legend(fontsize=8)
    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("Waktu Pengiriman vs Skor Review")

    scatter_data = state_stats.dropna(
        subset=["avg_delivery_days", "avg_review", "orders"]
    ).copy()

    fig, ax = plt.subplots(figsize=(9, 8))

    if not scatter_data.empty:
        sizes = (
            scatter_data["orders"]
            / scatter_data["orders"].max()
            * 800
        )

        ax.scatter(
            scatter_data["avg_delivery_days"],
            scatter_data["avg_review"],
            s=sizes,
            alpha=0.6,
            color=BLUE,
            edgecolors="white"
        )

        for state, row in scatter_data.iterrows():
            if row["avg_delivery_days"] >= 22 or row["avg_review"] < 3.85:
                ax.annotate(
                    state,
                    (row["avg_delivery_days"], row["avg_review"]),
                    xytext=(4, 4),
                    textcoords="offset points",
                    fontsize=8
                )

    ax.set_title(
        "Waktu Pengiriman dan Skor Review per State",
        loc="left"
    )
    ax.set_xlabel("Rata-rata Waktu Pengiriman (hari)")
    ax.set_ylabel("Rata-rata Skor Review (1–5)")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# 7B. REVIEW TEPAT WAKTU VS TERLAMBAT

st.subheader("Perbandingan Review: Tepat Waktu vs Terlambat")

late_review = (
    order_level.dropna(subset=["is_late", "review_score"])
    .groupby("is_late")["review_score"]
    .agg(["mean", "count"])
)

late_review = late_review.reindex([False, True]).dropna(subset=["mean"])

late_review.index = [
    "Tepat waktu" if value is False else "Terlambat"
    for value in late_review.index
]

fig, ax = plt.subplots(figsize=(8, 4))

colors = [
    BLUE if label == "Tepat waktu" else RED
    for label in late_review.index
]

bars = ax.bar(late_review.index, late_review["mean"], color=colors)

for bar, value in zip(bars, late_review["mean"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.05,
        f"{value:.2f}",
        ha="center"
    )

ax.set_title("Rata-rata Skor Review berdasarkan Ketepatan Pengiriman")
ax.set_ylabel("Rata-rata Skor Review (1–5)")
ax.set_ylim(0, 5)
ax.grid(axis="y", alpha=0.25)
ax.set_axisbelow(True)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.dataframe(
    late_review.rename(columns={
        "mean": "Rata-rata Skor Review",
        "count": "Jumlah Pesanan"
    }).style.format({
        "Rata-rata Skor Review": "{:.2f}",
        "Jumlah Pesanan": "{:,.0f}"
    }),
    use_container_width=True
)


# 7C. BINNING LAMA PENGIRIMAN

st.subheader("Skor Review berdasarkan Kelompok Durasi Pengiriman")

bin_data = order_level.dropna(
    subset=["delivery_days", "review_score"]
).copy()

bins = [-float("inf"), 7, 14, 21, 30, float("inf")]
labels = ["<= 7 hari", "8–14 hari", "15–21 hari", "22–30 hari", "> 30 hari"]

bin_data["delivery_group"] = pd.cut(
    bin_data["delivery_days"],
    bins=bins,
    labels=labels
)

bin_stats = (
    bin_data.groupby("delivery_group", observed=False)
    .agg(
        avg_review=("review_score", "mean"),
        orders=("order_id", "nunique")
    )
    .reindex(labels)
)

fig, ax = plt.subplots(figsize=(10, 4))

bin_colors = [
    RED if label in ["> 30 hari", "22–30 hari"] else GRAY
    for label in bin_stats.index
]

bars = ax.bar(
    bin_stats.index.astype(str),
    bin_stats["avg_review"],
    color=bin_colors
)

for bar, value in zip(bars, bin_stats["avg_review"]):
    if pd.notna(value):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.05,
            f"{value:.2f}",
            ha="center"
        )

ax.set_title(
    "Skor Review Menurut Kelompok Lama Pengiriman",
    loc="left"
)
ax.set_xlabel("Kelompok Lama Pengiriman")
ax.set_ylabel("Rata-rata Skor Review (1–5)")
ax.set_ylim(0, 5)
ax.grid(axis="y", alpha=0.25)
ax.set_axisbelow(True)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.markdown(
    """
    **Insight Pertanyaan 2**

    Bandingkan skor ulasan pesanan tepat waktu dan terlambat.
    Penurunan skor pada kelompok pengiriman yang lebih lama
    menunjukkan pentingnya evaluasi kinerja logistik. Hubungan
    ini merupakan asosiasi, bukan bukti bahwa durasi pengiriman
    menjadi satu-satunya penyebab skor ulasan.
    """
)

with st.expander("Lihat statistik seluruh state"):
    st.dataframe(
        state_stats.style.format({
            "avg_delivery_days": "{:.2f}",
            "avg_review": "{:.2f}",
            "late_rate": "{:.3f}",
            "late_rate_pct": "{:.1f}%"
        }),
        use_container_width=True
    )

st.divider()


# ============================================================
# 8. PERTANYAAN 3
# RFM ANALYSIS
# ============================================================

st.header("3. Segmentasi Pelanggan (RFM)")

st.markdown(
    """
    RFM mengelompokkan pelanggan berdasarkan Recency, Frequency,
    dan Monetary. Karena mayoritas pelanggan hanya bertransaksi
    sekali, segmentasi menggunakan aturan bisnis dari notebook.
    """
)

ref_date = (
    main_df["order_purchase_timestamp"].max()
    + pd.Timedelta(days=1)
)

rfm = (
    main_df.groupby("customer_unique_id")
    .agg(
        last_order=("order_purchase_timestamp", "max"),
        Frequency=("order_id", "nunique"),
        Monetary=("price", "sum")
    )
    .reset_index()
)

rfm["Recency"] = (ref_date - rfm["last_order"]).dt.days
m_q75 = rfm["Monetary"].quantile(0.75)


def segment_customer(row):
    if row["Frequency"] >= 2:
        return "Repeat Buyers"

    if row["Recency"] <= 180:
        if row["Monetary"] >= m_q75:
            return "Recent High Spenders"
        return "Recent Customers"

    if row["Monetary"] >= m_q75:
        return "At-Risk High Spenders"

    return "Dormant Customers"


rfm["segment"] = rfm.apply(segment_customer, axis=1)

seg_stats = (
    rfm.groupby("segment")
    .agg(
        customers=("customer_unique_id", "count"),
        revenue=("Monetary", "sum"),
        avg_recency=("Recency", "mean"),
        avg_monetary=("Monetary", "mean")
    )
)

seg_stats["pct_customers"] = (
    seg_stats["customers"] / seg_stats["customers"].sum() * 100
)

seg_stats["pct_revenue"] = (
    seg_stats["revenue"] / seg_stats["revenue"].sum() * 100
)

seg_stats = seg_stats.sort_values(
    "pct_revenue", ascending=False
).round(1)

st.caption(
    f"Batas high spender (kuartil ke-3 Monetary): R$ {m_q75:,.2f}"
)

st.metric(
    "Pelanggan dengan Pembelian Berulang",
    f"{(rfm['Frequency'] > 1).mean() * 100:.1f}%"
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Persentase Pelanggan per Segmen")
    plot_customers = seg_stats["pct_customers"].sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(9, 5))

    bar_colors = [
        RED if label == "At-Risk High Spenders" else
        BLUE if label == "Recent High Spenders" else GRAY
        for label in plot_customers.index
    ]

    bars = ax.barh(
        plot_customers.index,
        plot_customers.values,
        color=bar_colors
    )

    for bar, value in zip(bars, plot_customers.values):
        ax.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f"  {value:.1f}%",
            va="center"
        )

    ax.set_title("Distribusi Pelanggan per Segmen", loc="left")
    ax.set_xlabel("Persentase Pelanggan (%)")
    ax.set_ylabel("")
    ax.set_xlim(0, max(55, plot_customers.max() + 8))
    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("Kontribusi Revenue per Segmen")
    plot_revenue_segment = seg_stats["pct_revenue"].sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(9, 5))

    segment_colors = [
        RED if label == "At-Risk High Spenders" else
        BLUE if label == "Recent High Spenders" else GRAY
        for label in plot_revenue_segment.index
    ]

    bars = ax.barh(
        plot_revenue_segment.index,
        plot_revenue_segment.values,
        color=segment_colors
    )

    for bar, value in zip(bars, plot_revenue_segment.values):
        ax.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f"  {value:.1f}%",
            va="center"
        )

    ax.set_title("Kontribusi Revenue per Segmen", loc="left")
    ax.set_xlabel("Persentase Revenue (%)")
    ax.set_ylabel("")
    ax.set_xlim(0, max(42, plot_revenue_segment.max() + 8))
    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with st.expander("Lihat detail RFM per segmen"):
    rfm_table = seg_stats.rename(columns={
        "customers": "Jumlah Pelanggan",
        "revenue": "Revenue (R$)",
        "avg_recency": "Rata-rata Recency (hari)",
        "avg_monetary": "Rata-rata Monetary (R$)",
        "pct_customers": "Pelanggan (%)",
        "pct_revenue": "Revenue (%)"
    })

    st.dataframe(
        rfm_table.style.format({
            "Revenue (R$)": "R$ {:,.2f}",
            "Rata-rata Recency (hari)": "{:.1f}",
            "Rata-rata Monetary (R$)": "R$ {:,.2f}",
            "Pelanggan (%)": "{:.1f}%",
            "Revenue (%)": "{:.1f}%"
        }),
        use_container_width=True
    )

st.markdown(
    """
    **Insight Pertanyaan 3**

    Basis pelanggan didominasi pembeli satu kali. Segmen
    At-Risk High Spenders memiliki nilai strategis karena
    pelanggan dalam segmen ini telah lebih dari 180 hari
    tidak kembali berbelanja, tetapi menyumbang kontribusi
    revenue yang besar.

    Strategi yang dapat dipertimbangkan adalah kampanye reaktivasi
    pelanggan bernilai tinggi dan program loyalitas untuk
    mendorong pembelian berulang.
    """
)

st.divider()


# ============================================================
# 9. GEOSPATIAL ANALYSIS
# ============================================================

st.header("4. Geospatial Analysis")

st.markdown(
    """
    Peta menunjukkan persebaran revenue dan rata-rata waktu
    pengiriman per state pelanggan di Brasil. Ukuran lingkaran
    menunjukkan revenue, sedangkan warna menunjukkan waktu
    pengiriman rata-rata.
    """
)

geo_state = (
    main_df.groupby("customer_state")
    .agg(
        revenue=("price", "sum"),
        orders=("order_id", "nunique"),
        avg_delivery=("delivery_days", "mean")
    )
    .reset_index()
    .merge(
        state_geo,
        on="customer_state",
        how="inner"
    )
)

geo_state = geo_state.dropna(
    subset=["lat", "lng", "revenue", "avg_delivery"]
)

if not geo_state.empty:
    geo_state = geo_state.sort_values("revenue", ascending=False)
    max_revenue = geo_state["revenue"].max()

    geo_map = folium.Map(
        location=[-15.0, -52.0],
        zoom_start=4,
        tiles="OpenStreetMap"
    )

    for _, row in geo_state.iterrows():
        radius = (
            4 + (row["revenue"] / max_revenue) * 28
            if max_revenue > 0 else 4
        )

        if row["avg_delivery"] >= 20:
            color = RED
        elif row["avg_delivery"] >= 14:
            color = ORANGE
        else:
            color = "#2A6F97"

        folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            tooltip=(
                f"State: {row['customer_state']} | "
                f"Revenue: R$ {row['revenue']:,.0f} | "
                f"Pesanan: {row['orders']:,} | "
                f"Pengiriman: {row['avg_delivery']:.1f} hari"
            )
        ).add_to(geo_map)

    st_folium(
        geo_map,
        use_container_width=True,
        height=550
    )

    geo_total_revenue = geo_state["revenue"].sum()

    top3_geo = geo_state.sort_values(
        "revenue", ascending=False
    ).head(3)

    st.subheader("Tiga State dengan Revenue Terbesar")
    metric_cols = st.columns(3)

    for col, (_, row) in zip(metric_cols, top3_geo.iterrows()):
        share = (
            row["revenue"] / geo_total_revenue * 100
            if geo_total_revenue > 0 else 0
        )

        col.metric(
            row["customer_state"],
            f"R$ {row['revenue']:,.0f}",
            f"{share:.1f}% dari revenue pada peta"
        )

    with st.expander("Lihat seluruh data geospasial"):
        geo_table = geo_state.copy()

        geo_table["pct_revenue"] = (
            geo_table["revenue"] / geo_total_revenue * 100
        )

        geo_table = geo_table.sort_values("revenue", ascending=False)

        st.dataframe(
            geo_table[[
                "customer_state",
                "revenue",
                "pct_revenue",
                "orders",
                "avg_delivery"
            ]].rename(columns={
                "customer_state": "State",
                "revenue": "Revenue (R$)",
                "pct_revenue": "Kontribusi Revenue (%)",
                "orders": "Jumlah Pesanan",
                "avg_delivery": "Rata-rata Pengiriman (hari)"
            }).style.format({
                "Revenue (R$)": "R$ {:,.2f}",
                "Kontribusi Revenue (%)": "{:.1f}%",
                "Jumlah Pesanan": "{:,.0f}",
                "Rata-rata Pengiriman (hari)": "{:.1f}"
            }),
            use_container_width=True
        )

    st.markdown(
        """
        **Insight Geospatial**

        Distribusi revenue yang terkonsentrasi pada sejumlah
        state dapat menjadi dasar untuk menentukan prioritas
        stok dan distribusi. State dengan waktu pengiriman
        tinggi perlu dievaluasi lebih lanjut dari sisi jangkauan
        logistik dan layanan kurir.
        """
    )

else:
    st.warning(
        "Data geospasial kosong atau koordinat tidak cocok. "
        "Pastikan state_geo.csv memiliki customer_state, lat, dan lng."
    )


# ============================================================
# 10. KESIMPULAN DAN REKOMENDASI
# ============================================================

st.divider()
st.header("5. Kesimpulan dan Rekomendasi")

st.subheader("Kesimpulan")

st.markdown(
    """
    1. **Penjualan:** kategori dengan revenue tertinggi dapat
       menjadi prioritas pengelolaan stok dan promosi.
    2. **Pengiriman:** perbedaan skor review antara pesanan
       tepat waktu dan terlambat perlu menjadi perhatian
       dalam evaluasi layanan logistik.
    3. **Pelanggan:** segmen At-Risk High Spenders merupakan
       peluang reaktivasi karena nilai revenue-nya relatif besar.
    4. **Geospasial:** distribusi revenue dan waktu pengiriman
       per state dapat membantu menentukan prioritas wilayah.
    """
)

st.subheader("Rekomendasi")

st.markdown(
    """
    - Prioritaskan stok dan promosi pada kategori produk
      dengan revenue tinggi.
    - Evaluasi proses pengiriman pada state dengan durasi
      pengiriman terlama.
    - Pertimbangkan kampanye reaktivasi untuk At-Risk High
      Spenders dan program loyalitas untuk pembelian berulang.
    - Gunakan informasi revenue per state untuk mendukung
      perencanaan distribusi dan evaluasi mitra logistik.
    """
)

st.caption(
    "Sumber: Olist E-Commerce Public Dataset. "
    "Hasil dashboard mengikuti periode dan definisi analisis "
    "yang diterapkan pada notebook."
)