import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# PAGE CONFIG

st.set_page_config(
    page_title="CyberNova Sales Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# CUSTOM STYLING

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.stMetric {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 10px;
}

h1, h2, h3 {
    color: #4FC3F7;
}
</style>
""", unsafe_allow_html=True)


# USER DATABASE

USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin"
    },
    "sales1": {
        "password": "sales123",
        "role": "sales"
    },
    "sales2": {
        "password": "sales123",
        "role": "sales"
    },
    "sales3": {
        "password": "sales123",
        "role": "sales"
    }
}


# SESSION STATE

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None


# LOGIN SCREEN

if not st.session_state.logged_in:

    st.title("CyberNova Analytics Platform")

    st.subheader("Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in USERS:

            if USERS[username]["password"] == password:

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = USERS[username]["role"]

                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Incorrect Password")

        else:
            st.error("User Not Found")

    st.info("""
    Demo Accounts
    
    ADMIN
    Username: admin
    Password: admin123
    
    SALES
    Username: sales1
    Password: sales123
    """)

    st.stop()


# LOAD DATA

@st.cache_data
def load_data():

    df = pd.read_csv("CYBER_NOVA_MAATLA/CyberNova_SalesLog.csv")
    
    # Clean column names
    df.columns = df.columns.str.strip()


    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    df["Date"] = df["Timestamp"].dt.date

    df["Hour"] = df["Timestamp"].dt.hour

    return df


df = load_data()


# ROLE-BASED DATA ACCESS


# Clean usernames for matching
df["Sales_Team_Member"] = (
    df["Sales_Team_Member"]
    .astype(str)
    .str.strip()
    .str.lower()
)

current_user = (
    st.session_state.username
    .strip()
    .lower()
)

# Individual sales users only see their own records
if st.session_state.role == "sales":

    filtered_user_df = df[
        df["Sales_Team_Member"] == current_user
    ]

else:
    filtered_user_df = df.copy()

# Prevent empty dataframe date errors
if filtered_user_df.empty:

    st.warning("No records found for this user.")
    st.stop()

# SIDEBAR NAVIGATION

st.sidebar.title("CyberNova Navigation")

st.sidebar.success(
    f"Logged in as: {st.session_state.username}"
)

st.sidebar.info(
    f"Role: {st.session_state.role.upper()}"
)

st.sidebar.markdown("---")


# NAVIGATION MENU

if st.session_state.role == "admin":

    navigation = st.sidebar.radio(
        "Dashboard Views",
        [
            "Overview",
            "Sales Performance",
            "Regional Intelligence",
            "Traffic Analysis",
            "AI Assistant Analytics",
            "Demo & Event Requests",
            "Statistics",
            "Data Management",
            "Export Reports"
        ]
    )

else:

    navigation = st.sidebar.radio(
        "Dashboard Views",
        [
            "Overview",
            "My Performance",
            "Regional Intelligence",
            "Traffic Analysis",
            "Statistics",
            "Export Reports"
        ]
    )

st.sidebar.markdown("---")


# FILTERS

st.sidebar.subheader("Dashboard Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [
        filtered_user_df["Date"].min(),
        filtered_user_df["Date"].max()
    ]
)

selected_countries = st.sidebar.multiselect(
    "Countries",
    options=filtered_user_df["Country"].unique(),
    default=filtered_user_df["Country"].unique()
)

selected_services = st.sidebar.multiselect(
    "Services",
    options=filtered_user_df["Service_Type"].unique(),
    default=filtered_user_df["Service_Type"].unique()
)

selected_sources = st.sidebar.multiselect(
    "Traffic Source",
    options=filtered_user_df["Traffic_Source"].unique(),
    default=filtered_user_df["Traffic_Source"].unique()
)

selected_devices = st.sidebar.multiselect(
    "Device Type",
    options=filtered_user_df["Device_Type"].unique(),
    default=filtered_user_df["Device_Type"].unique()
)


# APPLY FILTERS

filtered_df = filtered_user_df.copy()

if len(date_range) == 2:

    filtered_df = filtered_df[
        (filtered_df["Date"] >= date_range[0]) &
        (filtered_df["Date"] <= date_range[1])
    ]

filtered_df = filtered_df[
    filtered_df["Country"].isin(selected_countries)
]

filtered_df = filtered_df[
    filtered_df["Service_Type"].isin(selected_services)
]

filtered_df = filtered_df[
    filtered_df["Traffic_Source"].isin(selected_sources)
]

filtered_df = filtered_df[
    filtered_df["Device_Type"].isin(selected_devices)
]


# LOGOUT BUTTON IN SIDEBAR

st.sidebar.markdown("---")

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

    st.rerun()


# DASHBOARD HEADER

st.title("CyberNova Sales Analytics Dashboard")

if st.session_state.role == "admin":

    st.caption(
        "Management & Collective Performance Dashboard"
    )

else:

    st.caption(
        "Individual Sales Team Dashboard"
    )


# KPI SECTION

st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

total_requests = len(filtered_df)

unique_users = filtered_df["User_ID"].nunique()

demo_requests = filtered_df["Demo_Request"].sum()

ai_requests = filtered_df["AI_Assistant_Request"].sum()

conversion_rate = (
    filtered_df["Converted_To_Sale"].mean() * 100
)

col1.metric("Total Requests", total_requests)

col2.metric("Unique Users", unique_users)

col3.metric("Demo Requests", demo_requests)

col4.metric("AI Requests", ai_requests)

col5.metric(
    "Conversion Rate",
    f"{conversion_rate:.1f}%"
)


# OVERVIEW

if navigation == "Overview":

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Most Requested Pages")

        page_data = (
            filtered_df["Endpoint"]
            .value_counts()
            .reset_index()
        )

        page_data.columns = ["Page", "Requests"]

        fig = px.bar(
            page_data,
            x="Page",
            y="Requests",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("User Geographic Distribution")

        fig = px.pie(
            filtered_df,
            names="Country"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Request Trends Over Time")

    trend_data = (
        filtered_df.groupby("Date")
        .size()
        .reset_index(name="Requests")
    )

    fig = px.line(
        trend_data,
        x="Date",
        y="Requests",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# SALES PERFORMANCE

elif navigation in ["Sales Performance", "My Performance"]:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Conversions by Service")

        service_data = (
            filtered_df.groupby("Service_Type")
            ["Converted_To_Sale"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            service_data,
            x="Service_Type",
            y="Converted_To_Sale",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Traffic Source Performance")

        traffic_data = (
            filtered_df.groupby("Traffic_Source")
            ["Converted_To_Sale"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            traffic_data,
            x="Traffic_Source",
            y="Converted_To_Sale",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# REGIONAL INTELLIGENCE

elif navigation == "Regional Intelligence":

    st.subheader(
        "CyberNova Region Intelligence Model"
    )

    region_scores = (
        filtered_df.groupby("Country")
        .agg({
            "Converted_To_Sale": "mean",
            "Demo_Request": "sum",
            "AI_Assistant_Request": "sum",
            "Engagement_Score": "mean"
        })
        .round(3)
    )

    region_scores["Likelihood Score (%)"] = (

        region_scores["Converted_To_Sale"] * 0.45 +

        (region_scores["Demo_Request"] /
         len(filtered_df)) * 0.30 +

        (region_scores["Engagement_Score"] / 10)
        * 0.25

    ) * 100

    region_scores = region_scores.sort_values(
        "Likelihood Score (%)",
        ascending=False
    )

    st.dataframe(
        region_scores.style.background_gradient(
            cmap="Blues"
        ),
        use_container_width=True
    )

    fig = px.bar(
        region_scores.reset_index(),
        x="Country",
        y="Likelihood Score (%)",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# TRAFFIC ANALYSIS

elif navigation == "Traffic Analysis":

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Hourly Traffic Trends")

        hourly_data = (
            filtered_df.groupby("Hour")
            .size()
            .reset_index(name="Requests")
        )

        fig = px.line(
            hourly_data,
            x="Hour",
            y="Requests",
            markers=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Traffic Source Distribution")

        fig = px.pie(
            filtered_df,
            names="Traffic_Source"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# AI ASSISTANT ANALYTICS

elif navigation == "AI Assistant Analytics":

    ai_df = filtered_df[
        filtered_df["AI_Assistant_Request"] == 1
    ]

    st.subheader(
        "AI Assistant Usage Analytics"
    )

    col1, col2 = st.columns(2)

    with col1:

        ai_country = (
            ai_df["Country"]
            .value_counts()
            .reset_index()
        )

        ai_country.columns = [
            "Country",
            "Requests"
        ]

        fig = px.bar(
            ai_country,
            x="Country",
            y="Requests",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.scatter(
            ai_df,
            x="Engagement_Score",
            y="Time_Spent",
            color="Country"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# DEMO & EVENT REQUESTS

elif navigation == "Demo & Event Requests":

    st.subheader(
        "Demo and Event Request Analysis"
    )

    demo_data = (
        filtered_df.groupby("Country")
        ["Demo_Request"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        demo_data,
        x="Country",
        y="Demo_Request",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# STATISTICS

elif navigation == "Statistics":

    st.subheader("Statistical Summary")

    stats_df = filtered_df[
        [
            "Time_Spent",
            "Engagement_Score"
        ]
    ]

    st.dataframe(
        stats_df.describe(),
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            filtered_df,
            x="Time_Spent",
            nbins=20
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.scatter(
            filtered_df,
            x="Time_Spent",
            y="Engagement_Score",
            color="Country"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# DATA MANAGEMENT (ADMIN ONLY)

elif navigation == "Data Management":

    st.subheader("Data Quality Management")

    st.write(
        "Total Duplicate Records:",
        filtered_df.duplicated().sum()
    )

    st.dataframe(
        filtered_df.head(20),
        use_container_width=True
    )


# EXPORT REPORTS

elif navigation == "Export Reports":

    st.subheader("Export Analytics Reports")

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name="CyberNova_Report.csv",
        mime="text/csv"
    )

    st.success(
        "Report Ready For Download"
    )


# FOOTER

st.markdown("---")

st.caption(
    "CyberNova Analytics Ltd | AI-Driven Sales Intelligence Platform 2026"
)
