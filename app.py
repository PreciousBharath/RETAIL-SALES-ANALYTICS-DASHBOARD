"""RetailPulse - Interactive retail sales analytics dashboard.
Run:  streamlit run app.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

from data import make_sales

st.set_page_config(page_title="RetailPulse Analytics", page_icon="🛒", layout="wide")
PAL = ["#FF416C", "#8E2DE2", "#00C9FF", "#F7B32B", "#39D98A"]


@st.cache_data
def load():
    return make_sales()


raw = load()
with st.sidebar:
    st.header("🔎 Filters")
    d0, d1 = st.date_input("Date range", (raw.date.min().date(), raw.date.max().date()))
    regions = st.multiselect("Region", sorted(raw.region.unique()), default=sorted(raw.region.unique()))
    cats = st.multiselect("Category", sorted(raw.category.unique()), default=sorted(raw.category.unique()))
    channels = st.multiselect("Channel", sorted(raw.channel.unique()), default=sorted(raw.channel.unique()))

df = raw[(raw.date.dt.date >= d0) & (raw.date.dt.date <= d1) & raw.region.isin(regions)
         & raw.category.isin(cats) & raw.channel.isin(channels)]

st.markdown("<h1 style='margin-bottom:0'>🛒 RetailPulse — Sales Analytics</h1>"
            "<p style='color:#888'>40,000 transactions · 9 cities · 5 categories · 2024–2025</p>", unsafe_allow_html=True)

fmt = lambda v: f"₹{v/1e7:.2f} Cr" if v >= 1e7 else f"₹{v/1e5:.1f} L"
cur, prev = df[df.date.dt.year == 2025], df[df.date.dt.year == 2024]
yoy = lambda a, b: f"{(a/b-1):+.1%} YoY" if b else None
k = st.columns(5)
k[0].metric("Revenue", fmt(df.revenue.sum()), yoy(cur.revenue.sum(), prev.revenue.sum()))
k[1].metric("Profit", fmt(df.profit.sum()), yoy(cur.profit.sum(), prev.profit.sum()))
k[2].metric("Orders", f"{len(df):,}", yoy(len(cur), len(prev)))
k[3].metric("Avg order value", f"₹{df.revenue.mean():,.0f}")
k[4].metric("Profit margin", f"{df.profit.sum()/df.revenue.sum():.1%}")

c1, c2 = st.columns([2, 1])
with c1:
    m = df.set_index("date").resample("MS")[["revenue", "profit"]].sum().reset_index()
    m["3-mo avg"] = m.revenue.rolling(3).mean()
    fig = px.area(m, x="date", y="revenue", title="Monthly revenue trend (festive peaks: Oct–Nov)",
                  color_discrete_sequence=["#8E2DE2"])
    fig.add_scatter(x=m.date, y=m["3-mo avg"], name="3-month avg", line=dict(color="#F7B32B", dash="dot"))
    fig.update_layout(height=340, margin=dict(t=40, b=10), legend=dict(orientation="h", x=0.01, y=0.98, bgcolor="rgba(0,0,0,0)"), showlegend=True)
    st.plotly_chart(fig, width="stretch")
with c2:
    fig = px.sunburst(df, path=["category", "product"], values="revenue", color="category",
                      color_discrete_sequence=PAL, title="Revenue mix")
    fig.update_layout(height=340, margin=dict(t=40, b=10))
    st.plotly_chart(fig, width="stretch")

c1, c2, c3 = st.columns(3)
with c1:
    city = df.groupby(["city", "region"], as_index=False).revenue.sum().sort_values("revenue")
    fig = px.bar(city, x="revenue", y="city", color="region", orientation="h", title="Revenue by city",
                 color_discrete_sequence=PAL)
    fig.update_layout(height=330, margin=dict(t=40, b=10))
    st.plotly_chart(fig, width="stretch")
with c2:
    heat = df.assign(day=df.date.dt.day_name().str[:3]).pivot_table(index="day", columns="hour", values="revenue", aggfunc="sum")
    heat = heat.reindex(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    fig = px.imshow(heat, color_continuous_scale="Magma", aspect="auto", title="Sales heatmap: day × hour")
    fig.update_layout(height=330, margin=dict(t=40, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig, width="stretch")
with c3:
    ch = df.groupby("channel", as_index=False).revenue.sum()
    fig = px.pie(ch, names="channel", values="revenue", hole=.55, title="Channel share", color_discrete_sequence=PAL)
    fig.update_layout(height=330, margin=dict(t=40, b=10))
    st.plotly_chart(fig, width="stretch")

c1, c2 = st.columns([3, 2])
with c1:
    top = df.groupby(["product", "category"], as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("qty", "size"))
    top["margin %"] = (100 * top.profit / top.revenue).round(1)
    st.subheader("🏆 Top products")
    st.dataframe(top.sort_values("revenue", ascending=False).head(8), hide_index=True, width="stretch",
                 column_config={"revenue": st.column_config.NumberColumn(format="₹%d"),
                                "profit": st.column_config.NumberColumn(format="₹%d"),
                                "margin %": st.column_config.ProgressColumn(min_value=0, max_value=45, format="%.1f%%")})
with c2:
    st.subheader("💡 Auto insights")
    best_cat = df.groupby("category").profit.sum().idxmax()
    best_city = df.groupby("city").revenue.sum().idxmax()
    peak = df.groupby(df.date.dt.month_name()).revenue.sum().idxmax()
    disc = df.groupby("discount").apply(lambda g: g.profit.sum() / g.revenue.sum(), include_groups=False)
    st.markdown(f"""
- **{best_cat}** is the most profitable category.
- **{best_city}** leads revenue among cities.
- **{peak}** is the peak sales month — plan inventory ahead of festive season.
- Margin falls from **{disc.iloc[0]:.0%}** (no discount) to **{disc.iloc[-1]:.0%}** at the highest discount tier.
""")
    st.download_button("⬇️ Export filtered data", df.to_csv(index=False), "retail_sales_filtered.csv")
