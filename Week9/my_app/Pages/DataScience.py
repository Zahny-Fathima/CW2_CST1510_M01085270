import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from app.mydata.datasets import get_all_datasets, insert_dataset, update_dataset_records, delete_dataset
from app.mydata.db import connect_database

import streamlit as st
import pandas as pd
import numpy as np
import os

from openai import OpenAI

st.set_page_config(page_title="Data Science Dashboard", page_icon="📊", layout="wide")

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
st.title("📊 Data Science Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

# Create tabs
tab_datasets, tab_analytics, tab_ai = st.tabs(
    ["📁 Datasets", "📈 Analytics", "🤖 AI Assistant"]
)

with tab_datasets:
    st.subheader("📁 Dataset Management")
    st.info("Manage, view, and update dataset metadata here.")

    conn = connect_database()

    st.markdown("### ➕ Register New Dataset")

    with st.form("add_dataset_form"):
        dataset_name = st.text_input("Dataset Name")
        category = st.selectbox("Category", ["Customer", "Sales", "Marketing", "Finance", "Operations", "Other"])
        source = st.text_input("Source (e.g., API, Database, File)")
        last_updated = st.date_input("Last Updated")
        record_count = st.number_input("Record Count", min_value=0, step=1)
        file_size_mb = st.number_input("File Size (MB)", min_value=0.0, step=0.1, format="%.2f")
        submitted = st.form_submit_button("Register Dataset")

        if submitted:
            if dataset_name and source:
                insert_dataset(
                    conn,
                    dataset_name,
                    category,
                    source,
                    str(last_updated),
                    record_count,
                    file_size_mb
                )
                st.success("Dataset registered successfully")
                st.rerun()
            else:
                st.error("Dataset Name and Source are required")

    st.divider()

    st.markdown("### 📋 All Datasets")
    datasets_df = get_all_datasets(conn)

    if datasets_df.empty:
        st.info("No datasets registered yet.")
    else:
        st.dataframe(datasets_df, width="stretch")

    st.markdown("### ✏️ Update Dataset Record Count")

    dataset_id = st.number_input("Dataset ID", min_value=1, step=1)
    new_record_count = st.number_input("New Record Count", min_value=0, step=1, key="new_records")

    if st.button("Update Record Count"):
        rows = update_dataset_records(conn, dataset_id, new_record_count)
        if rows:
            st.success("Dataset record count updated")
            st.rerun()
        else:
            st.error("Dataset ID not found")

    st.markdown("### 🗑️ Delete Dataset")

    delete_id = st.number_input("Dataset ID to delete", min_value=1, step=1, key="delete_id")

    if st.button("Delete Dataset"):
        rows = delete_dataset(conn, delete_id)
        if rows:
            st.success("Dataset deleted")
            st.rerun()
        else:
            st.error("Dataset ID not found")

    conn.close()
    
    # CSV Data Viewer Section
    st.divider()
    st.markdown("### 📄 CSV Data Viewer")
    
    csv_path = r"F:\CST1510_CW2\DATA\datasets_metadata.csv"
    
    if os.path.exists(csv_path):
        try:
            csv_df = pd.read_csv(csv_path)
            
            # Show summary statistics
            st.write(f"**Rows:** {len(csv_df)} | **Columns:** {len(csv_df.columns)}")
            
            # Display the data
            st.dataframe(csv_df, width="stretch")
            
            # Optional: Add filtering
            if st.checkbox("Show column statistics", key="ds_csv_stats"):
                st.write(csv_df.describe())
                
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")
    else:
        st.warning(f"CSV file not found at: {csv_path}")
        st.info("You can upload a CSV file instead:")
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="ds_csv")
        if uploaded_file is not None:
            csv_df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(csv_df, width="stretch")


with tab_analytics:
    st.subheader("📈 Data Analytics Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Datasets", 127, delta="+8")

    with col2:
        st.metric("Total Records", "2.4M", delta="+150K")

    with col3:
        st.metric("Storage Used", "847 GB", delta="+23 GB")

    st.divider()

    category_data = {
        "Customer": 42,
        "Sales": 35,
        "Marketing": 28,
        "Finance": 15,
        "Operations": 7
    }

    st.subheader("📊 Datasets by Category")
    st.bar_chart(category_data)

    growth_data = {
        "Jan": 98,
        "Feb": 105,
        "Mar": 112,
        "Apr": 119,
        "May": 127
    }

    st.subheader("📈 Dataset Growth Over Time")
    st.line_chart(growth_data)

    st.divider()

    st.subheader("💾 Storage Distribution")
    storage_data = pd.DataFrame({
        "Category": ["Customer", "Sales", "Marketing", "Finance", "Operations"],
        "Storage (GB)": [340, 285, 132, 58, 32]
    })
    st.bar_chart(storage_data.set_index("Category"))


with tab_ai:
    st.title("🔍 AI Data Advisor")
    
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
        st.warning("⚠️ Please enter your OpenAI API key to use the AI Data Advisor.")
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
    datasets_df = get_all_datasets(conn)
    conn.close()
    
    if not datasets_df.empty:
        datasets = datasets_df.to_dict(orient="records")

        dataset_options = [
            f"{ds['id']}: {ds['dataset_name']} - {ds['category']} ({ds['record_count']} records)" 
            for ds in datasets
        ]

        selected_idx = st.selectbox(
            "Select dataset to analyze:",
            range(len(datasets)),
            format_func=lambda i: dataset_options[i]
        )

        dataset = datasets[selected_idx]

        st.subheader("📋 Dataset Details")
        st.write(f"**Name:** {dataset['dataset_name']}")
        st.write(f"**Category:** {dataset['category']}")
        st.write(f"**Source:** {dataset['source']}")
        st.write(f"**Records:** {dataset['record_count']:,}")
        st.write(f"**Size:** {dataset['file_size_mb']:.2f} MB")
        st.write(f"**Last Updated:** {dataset['last_updated']}")

        st.subheader("🤖 AI Analysis")

        user_prompt = st.text_area(
            "Ask the AI about this dataset:",
            value=f"Suggest analysis approaches for a {dataset['category']} dataset with {dataset['record_count']} records named '{dataset['dataset_name']}'"
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
        st.info("No datasets found in the database.")

# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")