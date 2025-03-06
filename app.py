#streamlit
import streamlit as st
import pandas as pd
import os
from io import BytesIO
import plotly.express as px

# Setup
st.set_page_config(page_title="Data Sweeper", page_icon="🧹", layout="wide")
st.title("🧹 Data Sweeper - AI-Powered Data Cleaning & Transformation")
st.write("Upload CSV or Excel files, clean your data, visualize insights, and convert between formats seamlessly with AI-powered automation!")

# File uploader
uploaded_files = st.file_uploader("📂 Upload Your Files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read file based on extension
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"❌ Error reading {file.name}: {e}")
            continue
        
        # Display file info
        st.write(f"### 📂 File: {file.name}")
        st.write(f"**Size:** {file.size / 1024:.2f} KB")
        st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Show data preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())
        
        # Data cleaning options
        st.subheader("🛠 Advanced Data Cleaning")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success(" Duplicates Removed!")
            
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing Values Filled!")
            
            # Outlier detection & removal
            if st.checkbox(f"Detect and Remove Outliers from {file.name}"):
                for col in df.select_dtypes(include=["number"]).columns:
                    q1, q3 = df[col].quantile([0.25, 0.75])
                    iqr = q3 - q1
                    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                    df = df[(df[col] >= lower) & (df[col] <= upper)]
                st.success("Outliers Removed!")
        
        # Column selection
        st.subheader("📌 Select Columns")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
        
        # Data visualization
        st.subheader("📊 Advanced Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_cols = df.select_dtypes(include="number").columns
            if len(numeric_cols) >= 2:
                fig = px.bar(df, x=numeric_cols[0], y=numeric_cols[1], title="Data Overview")
                st.plotly_chart(fig)
            else:
                st.warning("⚠ Not enough numeric columns for visualization.")
        
        # File conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            file_name = file.name.replace(file_ext, f".{conversion_type.lower()}")
            
            try:
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    mime_type = "text/csv"
                else:
                    df.to_excel(buffer, index=False)
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                
                # Download button
                st.download_button(
                    label=f"📥 Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
            except Exception as e:
                st.error(f"Error converting {file.name}: {e}")
        
st.success("All files processed successfully!")







