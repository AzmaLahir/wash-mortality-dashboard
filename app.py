import streamlit as st
import pandas as pd
import plotly.express as px

#Configuration page
st.set_page_config(
    page_title="WASH Mortality Dashboard",
    page_icon="💧",
    layout="wide"
)

#Loading the data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_mortality_data.csv")
    return df

df = load_data()

# SidePanel with filters
st.sidebar.title("💧 WASH Dashboard")
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filters")

# st.multiselect()
all_categories = sorted(df["Risk_Category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Select Risk Category",
    options=all_categories,
    default=all_categories
)

# st.slider()
min_rate = float(df["Mortality_Rate_2019"].min())
max_rate = float(df["Mortality_Rate_2019"].max())
rate_range = st.sidebar.slider(
    "Mortality Rate Range (per 1,000)",
    min_value=min_rate,
    max_value=max_rate,
    value=(min_rate, max_rate),
    step=0.1
)

# st.slider() for top N
top_n = st.sidebar.slider("Top N Countries (Bar Chart)", min_value=5, max_value=30, value=15)

# st.selectbox()
sort_order = st.sidebar.selectbox(
    "Sort Bar Chart By",
    options=["Highest First", "Lowest First"]
)

# st.checkbox()
show_table = st.sidebar.checkbox("Show Data Table", value=True)
show_insights = st.sidebar.checkbox("Show Key Insights", value=True)

st.sidebar.markdown("---")
st.sidebar.caption("Data Source: World Bank Data360 (2019)")

# Apply filters to the DataFrame
filtered_df = df[
    (df["Risk_Category"].isin(selected_categories)) &
    (df["Mortality_Rate_2019"] >= rate_range[0]) &
    (df["Mortality_Rate_2019"] <= rate_range[1])
]

# Header and description
st.title("💧 Global Under-5 Mortality from Unsafe WASH (2019)")
st.markdown(
    "**WASH** = Water, Sanitation & Hygiene | "
    "Data Source: [World Bank Data360](https://data360.worldbank.org/en/indicator/WB_WDI_SH_STA_WASH_P5) | "
    "Mortality rate per 1,000 live births"
)
st.markdown("---")

# Validation check
if len(selected_categories) == 0:
    st.error("⚠️ Please select at least one Risk Category from the sidebar.")
    st.stop()

if len(filtered_df) == 0:
    st.warning("No countries match the current filters. Please adjust the sliders or categories.")
    st.stop()

#KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌍 Countries Shown", len(filtered_df))
col2.metric("📈 Highest Rate", f"{filtered_df['Mortality_Rate_2019'].max():.2f}")
col3.metric("📉 Lowest Rate",  f"{filtered_df['Mortality_Rate_2019'].min():.2f}")
col4.metric("📊 Average Rate", f"{filtered_df['Mortality_Rate_2019'].mean():.2f}")

st.markdown("---")

# Row 1: World Map + Donut Chart
col_map, col_pie = st.columns([2, 1])

with col_map:
    st.subheader("🗺️ World Map — Mortality Rate by Country")
    fig_map = px.choropleth(
        filtered_df,
        locations="Country_Code",
        color="Mortality_Rate_2019",
        hover_name="Country_Name",
        hover_data={"Mortality_Rate_2019": ":.2f", "Risk_Category": True},
        color_continuous_scale="Reds",
        labels={"Mortality_Rate_2019": "Mortality Rate"}
    )
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_colorbar=dict(title="Rate per 1,000")
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col_pie:
    st.subheader("🏷️ Risk Category Distribution")
    risk_counts = filtered_df["Risk_Category"].value_counts().reset_index()
    risk_counts.columns = ["Risk_Category", "Count"]
    fig_pie = px.pie(
        risk_counts,
        names="Risk_Category",
        values="Count",
        color_discrete_sequence=px.colors.sequential.RdBu,
        hole=0.4
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    fig_pie.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

#Row 2: Bar Chart (with sort_order from selectbox)
st.subheader(f"📊 Top {top_n} Countries by Mortality Rate")
top_countries = filtered_df.nlargest(top_n, "Mortality_Rate_2019")
ascending = (sort_order == "Lowest First")
top_countries = top_countries.sort_values("Mortality_Rate_2019", ascending=ascending)

fig_bar = px.bar(
    top_countries,
    x="Mortality_Rate_2019",
    y="Country_Name",
    color="Risk_Category",
    orientation="h",
    labels={"Mortality_Rate_2019": "Mortality Rate (per 1,000)", "Country_Name": "Country"},
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_bar.update_layout(margin=dict(l=0, r=0, t=10, b=0), yaxis_title="")
st.plotly_chart(fig_bar, use_container_width=True)

# Row 3: Histogram + Box Plot 
col_hist, col_box = st.columns(2)

with col_hist:
    st.subheader("📈 Distribution of Mortality Rates")
    fig_hist = px.histogram(
        filtered_df,
        x="Mortality_Rate_2019",
        nbins=30,
        color="Risk_Category",
        labels={"Mortality_Rate_2019": "Mortality Rate (per 1,000)"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_hist.update_layout(margin=dict(l=0, r=0, t=10, b=0), bargap=0.05)
    st.plotly_chart(fig_hist, use_container_width=True)

with col_box:
    st.subheader("📦 Mortality Rate by Risk Category")
    fig_box = px.box(
        filtered_df,
        x="Risk_Category",
        y="Mortality_Rate_2019",
        color="Risk_Category",
        labels={
            "Mortality_Rate_2019": "Mortality Rate (per 1,000)",
            "Risk_Category": "Risk Category"
        },
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_box.update_layout(margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

#  Key Insights: uses st.success / st.warning / st.info
if show_insights:
    st.subheader("💡 Key Insights")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.error("🔴 **Highest Mortality** — Lesotho (108.1), Chad (99.2), and Somalia (99.2) top the list. All are in Sub-Saharan Africa.")
    with c2:
        st.warning("🟠 **Very High Risk** — 7.95% of countries fall in this category, yet represent a disproportionate burden of child deaths linked to poor WASH access.")
    with c3:
        st.success("🟢 **Low Risk Progress** — 43.2% of countries are in the Low risk category, reflecting global improvements in water and sanitation access.")

# Data Table, controlled by st.checkbox 
if show_table:
    st.subheader("📋 Explore the Data")

    # st.text_input()
    search = st.text_input("🔎 Search by Country Name", "")
    display_df = filtered_df.copy()
    if search:
        display_df = display_df[display_df["Country_Name"].str.contains(search, case=False)]

    display_df = display_df.sort_values("Mortality_Rate_2019", ascending=False).reset_index(drop=True)
    display_df.index += 1

    # st.info() 
    st.info(f"Showing {len(display_df)} countries based on current filters.")
    st.dataframe(display_df, use_container_width=True)

# Footer 
st.markdown("---")
st.caption(
    "📌 Dashboard developed for 5DATA004C Data Science Project Lifecycle | "
    "University of Westminster | Data: World Bank Data360 (2019)"
)