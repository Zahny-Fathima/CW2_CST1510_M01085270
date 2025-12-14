import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from app.mydata.incident import get_all_incidents, insert_incident, update_incident_status, delete_incident
from app.mydata.db import connect_database

import streamlit as st
import pandas as pd
import numpy as np
import os

from openai import OpenAI

st.set_page_config(page_title="Cyber Incidents Dashboard", page_icon="🛡️", layout="wide")

# Initialize OpenAI client
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

client = None
if st.session_state.openai_api_key:
    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
    except:
        pass

# Ensure state keys exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

# If logged in, show dashboard content
st.title("🛡️ Cyber Incidents Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

# Create tabs
tab_incidents, tab_analytics, tab_ai = st.tabs(
    ["🚨 Incidents", "📊 Analytics", "🤖 AI Assistant"]
)

with tab_incidents:
    st.subheader("🚨 Cyber Incidents Management")
    st.info("Manage, view, and update reported cyber incidents here.")

    conn = connect_database()

    st.markdown("### ➕ Report New Incident")

    with st.form("add_incident_form"):
        date = st.date_input("Date")
        incident_type = st.text_input("Incident Type")
        severity = st.selectbox("Severity", ["Low", "Medium", "High"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
        description = st.text_area("Description")
        submitted = st.form_submit_button("Add Incident")

        if submitted:
            insert_incident(
                conn,
                str(date),
                incident_type,
                severity,
                status,
                description,
                st.session_state.username
            )
            st.success("Incident added successfully")
            st.rerun()

    st.divider()

    st.markdown("### 📋 All Incidents")
    incidents_df = get_all_incidents(conn)

    if incidents_df.empty:
        st.info("No incidents reported yet.")
    else:
        st.dataframe(incidents_df, width="stretch")

    st.markdown("### ✏️ Update Incident Status")

    incident_id = st.number_input("Incident ID", min_value=1, step=1)
    new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved"], key="update_status")

    if st.button("Update Status"):
        rows = update_incident_status(conn, incident_id, new_status)
        if rows:
            st.success("Incident status updated")
            st.rerun()
        else:
            st.error("Incident ID not found")

    st.markdown("### 🗑️ Delete Incident")

    delete_id = st.number_input("Incident ID to delete", min_value=1, step=1, key="delete_id")

    if st.button("Delete Incident"):
        rows = delete_incident(conn, delete_id)
        if rows:
            st.success("Incident deleted")
            st.rerun()
        else:
            st.error("Incident ID not found")

    conn.close()
    
    # CSV Data Viewer Section
    st.divider()
    st.markdown("### 📄 CSV Data Viewer")
    
    csv_path = r"F:\CST1510_CW2\DATA\cyber_incidents.csv"
    
    if os.path.exists(csv_path):
        try:
            csv_df = pd.read_csv(csv_path)
            
            # Show summary statistics
            st.write(f"**Rows:** {len(csv_df)} | **Columns:** {len(csv_df.columns)}")
            
            # Display the data
            st.dataframe(csv_df, width="stretch")
            
            # Optional: Add filtering
            if st.checkbox("Show column statistics"):
                st.write(csv_df.describe())
                
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")
    else:
        st.warning(f"CSV file not found at: {csv_path}")
        st.info("You can upload a CSV file instead:")
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="cyber_csv")
        if uploaded_file is not None:
            csv_df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(csv_df, width="stretch")


with tab_analytics:
    st.subheader("📊 Security Analytics Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Threats Detected", 247, delta="+12")

    with col2:
        st.metric("Vulnerabilities", 8, delta="-3")

    with col3:
        st.metric("Incidents", 3, delta="+1")

    st.divider()

    threat_data = {
        "Malware": 89,
        "Phishing": 67,
        "DDoS": 45,
        "Intrusion": 46
    }

    st.subheader("🛑 Threat Distribution")
    st.bar_chart(threat_data)

    severity_data = {
        "Low": 12,
        "Medium": 7,
        "High": 3
    }

    st.subheader("⚠️ Incidents by Severity")
    st.line_chart(severity_data)


with tab_ai:
    st.title("🔍 AI Incident Analyzer")
    
    # API Key Input Section
    st.markdown("### 🔑 OpenAI API Configuration")
    
    api_key_input = st.text_input(
        "Enter your OpenAI API Key:",
        type="password",
        value=st.session_state.openai_api_key,
        help="Your API key is stored only for this session and is not saved."
    )
    
    if st.button("Save API Key"):
        st.session_state.openai_api_key = api_key_input
        st.success("API Key saved for this session!")
        st.rerun()
    
    if not st.session_state.openai_api_key:
        st.warning("⚠️ Please enter your OpenAI API key to use the AI Incident Analyzer.")
        st.info("You can get your API key from: https://platform.openai.com/api-keys")
        st.stop()
    
    # Initialize client with the stored API key
    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        st.stop()
    
    st.divider()
    
    # Rest of your AI tab code
    conn = connect_database()
    incidents_df = get_all_incidents(conn)
    conn.close()
    
    if not incidents_df.empty:
        incidents = incidents_df.to_dict(orient="records")

        incident_options = [
            f"{inc['id']}: {inc['incident_type']} - {inc['severity']}" for inc in incidents
        ]

        selected_idx = st.selectbox(
            "Select incident to analyze:",
            range(len(incidents)),
            format_func=lambda i: incident_options[i]
        )

        incident = incidents[selected_idx]

        st.subheader("📋 Incident Details")
        st.write(f"**Type:** {incident['incident_type']}")
        st.write(f"**Severity:** {incident['severity']}")
        st.write(f"**Description:** {incident['description']}")

        st.subheader("🤖 AI Analysis")

        user_prompt = st.text_area(
            "Ask the AI about this incident:",
            value=f"Analyze the following incident and suggest actions: {incident['description']}"
        )

        if st.button("Analyze with AI"):
            if user_prompt.strip():
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": user_prompt}]
                    )
                    ai_text = response.choices[0].message.content
                    st.markdown(f"**AI Response:** {ai_text}")
                except Exception as e:
                    st.error(f"Error calling OpenAI API: {str(e)}")
                    st.info("Please check your API key and try again.")
            else:
                st.warning("Please enter a prompt for the AI.")
    else:
        st.info("No incidents found in the database.")

# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")