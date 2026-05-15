import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# =========================================================
# INITIAL SETUP
# =========================================================
fake = Faker()

np.random.seed(42)
random.seed(42)

# =========================================================
# CONFIGURATION
# =========================================================
NUM_RECORDS = 50000

countries = [
    "Botswana",
    "South Africa",
    "Namibia",
    "Zimbabwe",
    "Zambia",
    "Kenya",
    "Mozambique",
    "Tanzania"
]

regions = {
    "Botswana": "Southern Africa",
    "South Africa": "Southern Africa",
    "Namibia": "Southern Africa",
    "Zimbabwe": "Southern Africa",
    "Zambia": "Southern Africa",
    "Kenya": "East Africa",
    "Mozambique": "Southern Africa",
    "Tanzania": "East Africa"
}

services = [
    "AI Cybersecurity",
    "Cloud Security",
    "Threat Monitoring",
    "Digital Transformation",
    "AI Assistant",
    "Data Analytics",
    "Cyber Risk Assessment"
]

traffic_sources = [
    "Direct",
    "Search",
    "Social Media",
    "Referral",
    "Email Campaign"
]

devices = [
    "Desktop",
    "Mobile",
    "Tablet"
]

endpoints = [
    "/index.html",
    "/about.html",
    "/services.html",
    "/solutions.html",
    "/contact.html",
    "/scheduledemo.php",
    "/event.php",
    "/aiassistant.php",
    "/jobs.php",
    "/prototype.php"
]

sales_members = [
    "sales1",
    "sales2",
    "sales3"
]

methods = ["GET", "POST"]

status_codes = [200, 200, 200, 200, 304, 404]

# =========================================================
# GENERATE SYNTHETIC DATA
# =========================================================
records = []

start_date = datetime(2026, 1, 1)

for i in range(NUM_RECORDS):

    timestamp = start_date + timedelta(
        days=random.randint(0, 120),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    country = random.choice(countries)

    endpoint = random.choice(endpoints)

    service = random.choice(services)

    traffic = random.choice(traffic_sources)

    device = random.choice(devices)

    sales_member = random.choice(sales_members)

    engagement_score = round(
        np.random.normal(7, 2),
        2
    )

    engagement_score = max(
        min(engagement_score, 10),
        1
    )

    time_spent = random.randint(20, 600)

    demo_request = 1 if endpoint == "/scheduledemo.php" else random.choice([0, 0, 0, 1])

    event_request = 1 if endpoint == "/event.php" else random.choice([0, 0, 1])

    ai_request = 1 if endpoint == "/aiassistant.php" else random.choice([0, 0, 1])

    converted = 1 if (
        demo_request == 1 and
        engagement_score > 7
    ) else random.choice([0, 0, 0, 1])

    record = {

        "Timestamp": timestamp,

        "IP_Address": fake.ipv4(),

        "Request_Method": random.choice(methods),

        "Endpoint": endpoint,

        "Status_Code": random.choice(status_codes),

        "Country": country,

        "Region": regions[country],

        "Service_Type": service,

        "Traffic_Source": traffic,

        "Device_Type": device,

        "User_ID": f"U{1000 + i}",

        "Session_ID": f"S{10000 + i}",

        "Demo_Request": demo_request,

        "Event_Request": event_request,

        "AI_Assistant_Request": ai_request,

        "Converted_To_Sale": converted,

        "Time_Spent": time_spent,

        "Engagement_Score": engagement_score,

        "Sales_Team_Member": sales_member
    }

    records.append(record)

# =========================================================
# CREATE DATAFRAME
# =========================================================
df = pd.DataFrame(records)

# =========================================================
# CREATE ADDITIONAL ANALYTICS COLUMNS
# =========================================================
df["Hour"] = pd.to_datetime(df["Timestamp"]).dt.hour

df["Day"] = pd.to_datetime(df["Timestamp"]).dt.day_name()

df["Month"] = pd.to_datetime(df["Timestamp"]).dt.month_name()

# =========================================================
# SAVE DATASET
# =========================================================
df.to_csv(
    "CyberNova_SalesLog.csv",
    index=False
)

# =========================================================
# DISPLAY SUMMARY
# =========================================================
print("===================================")
print("CyberNova Synthetic Dataset Created")
print("===================================")

print(f"Total Records: {len(df)}")

print(f"Countries: {df['Country'].nunique()}")

print(f"Services: {df['Service_Type'].nunique()}")

print(f"Sales Members: {df['Sales_Team_Member'].nunique()}")

print("\nDataset Saved As:")
print("CyberNova_SalesLog.csv")

print("\nSample Data:")
print(df.head())