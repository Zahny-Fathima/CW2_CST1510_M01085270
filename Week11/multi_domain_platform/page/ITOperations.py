import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from app.mydata.tickets import get_all_tickets, insert_ticket, update_ticket_status, resolve_ticket, delete_ticket
from app.mydata.db import connect_database

import streamlit as st
import pandas as pd
import numpy as np
import os

from openai import OpenAI

st.set_page_config(page_title="IT Operations Dashboard", page_icon="🖥️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #cfe8ff;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize OpenAI client
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

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
st.title("🖥️ IT Operations Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

# Create tabs
tab_tickets, tab_analytics, tab_ai = st.tabs(
    ["🎫 Tickets", "📊 Analytics", "🤖 AI Assistant"]
)

with tab_tickets:
    st.subheader("🎫 IT Ticket Management")
    st.info("Manage, view, and update IT support tickets here.")

    conn = connect_database()

    st.markdown("### ➕ Create New Ticket")

    with st.form("add_ticket_form"):
        ticket_id = st.text_input("Ticket ID (e.g., TKT-001)")
        created_date = st.date_input("Created Date")
        category = st.selectbox("Category", ["Hardware", "Software", "Network", "Access", "Other"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
        subject = st.text_input("Subject")
        description = st.text_area("Description")
        assigned_to = st.text_input("Assigned To (optional)")
        submitted = st.form_submit_button("Create Ticket")

        if submitted:
            if ticket_id and subject:
                insert_ticket(
                    conn,
                    ticket_id,
                    status,
                    category,
                    subject,
                    description,
                    str(created_date),
                    assigned_to if assigned_to else None
                )
                st.success("Ticket created successfully")
                st.rerun()
            else:
                st.error("Ticket ID and Subject are required")

    st.divider()

    st.markdown("### 📋 All Tickets")
    tickets_df = get_all_tickets(conn)

    if tickets_df.empty:
        st.info("No tickets created yet.")
    else:
        st.dataframe(tickets_df, width="stretch")

    st.markdown("### ✏️ Update Ticket Status")

    update_ticket_id = st.text_input("Ticket ID", key="update_ticket")
    new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"], key="update_status")

    if st.button("Update Status"):
        rows = update_ticket_status(conn, update_ticket_id, new_status)
        if rows:
            st.success("Ticket status updated")
            st.rerun()
        else:
            st.error("Ticket ID not found")

    st.markdown("### ✅ Resolve Ticket")

    resolve_ticket_id = st.text_input("Ticket ID to Resolve", key="resolve_ticket")
    resolved_date = st.date_input("Resolved Date", key="resolved_date")

    if st.button("Mark as Resolved"):
        rows = resolve_ticket(conn, resolve_ticket_id, str(resolved_date))
        if rows:
            st.success("Ticket marked as resolved")
            st.rerun()
        else:
            st.error("Ticket ID not found")

    st.markdown("### 🗑️ Delete Ticket")

    delete_ticket_id = st.text_input("Ticket ID to delete", key="delete_ticket")

    if st.button("Delete Ticket"):
        rows = delete_ticket(conn, delete_ticket_id)
        if rows:
            st.success("Ticket deleted")
            st.rerun()
        else:
            st.error("Ticket ID not found")

    conn.close()
    
    # CSV Data Viewer Section
    st.divider()
    st.markdown("### 📄 CSV Data Viewer")
    
    csv_path = r"F:\CST1510_CW2\DATA\it_tickets.csv"
    
    if os.path.exists(csv_path):
        try:
            csv_df = pd.read_csv(csv_path)
            
            # Show summary statistics
            st.write(f"**Rows:** {len(csv_df)} | **Columns:** {len(csv_df.columns)}")
            
            # Display the data
            st.dataframe(csv_df, width="stretch")
            
            # Optional: Add filtering
            if st.checkbox("Show column statistics", key="it_csv_stats"):
                st.write(csv_df.describe())
                
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")
    else:
        st.warning(f"CSV file not found at: {csv_path}")
        st.info("You can upload a CSV file instead:")
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="it_csv")
        if uploaded_file is not None:
            csv_df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(csv_df, width="stretch")


with tab_analytics:
    st.subheader("📊 IT Operations Analytics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Open Tickets", 42, delta="+5")

    with col2:
        st.metric("Resolved Today", 18, delta="+3")

    with col3:
        st.metric("Avg Resolution Time", "4.2 hrs", delta="-0.5")

    st.divider()

    ticket_category_data = {
        "Hardware": 35,
        "Software": 48,
        "Network": 29,
        "Access": 22,
        "Other": 15
    }

    st.subheader("🎫 Tickets by Category")
    st.bar_chart(ticket_category_data)

    status_data = {
        "Open": 42,
        "In Progress": 28,
        "Resolved": 85,
        "Closed": 94
    }

    st.subheader("📈 Ticket Status Distribution")
    st.line_chart(status_data)


with tab_ai:
    st.title("🔍 AI Ticket Analyzer")
    
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
        st.warning("⚠️ Please enter your OpenAI API key to use the AI Ticket Analyzer.")
        st.info("You can get your API key from: https://platform.openai.com/api-keys")
        st.stop()
    
    # Initialize client with the stored API key
    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        st.stop()
    
    st.divider()
    
    conn = connect_database()
    tickets_df = get_all_tickets(conn)
    conn.close()
    
    if not tickets_df.empty:
        tickets = tickets_df.to_dict(orient="records")

        ticket_options = [
            f"{ticket['ticket_id']}: {ticket['subject']} - {ticket['status']}" for ticket in tickets
        ]

        selected_idx = st.selectbox(
            "Select ticket to analyze:",
            range(len(tickets)),
            format_func=lambda i: ticket_options[i]
        )

        ticket = tickets[selected_idx]

        st.subheader("📋 Ticket Details")
        st.write(f"**Ticket ID:** {ticket['ticket_id']}")
        st.write(f"**Category:** {ticket['category']}")
        st.write(f"**Status:** {ticket['status']}")
        st.write(f"**Subject:** {ticket['subject']}")
        st.write(f"**Description:** {ticket['descripton']}")

        st.subheader("🤖 AI Analysis")

        user_prompt = st.text_area(
            "Ask the AI about this ticket:",
            value=f"Analyze the following IT ticket and suggest resolution steps: {ticket['descripton']}"
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
        st.info("No tickets found in the database.")

# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")