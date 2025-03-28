# AIzaSyAYJzZuqrttYLdNt7NULVqtHbDy3Bvmc5I

import os
os.system('pip install plotly')
import plotly.express as px

import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# 🔹 Configure Gemini AI (Use Free Version)
API_KEY = "AIzaSyAYJzZuqrttYLdNt7NULVqtHbDy3Bvmc5I"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Load Gemini Model
try:
    model = genai.GenerativeModel("gemini-1.5-flash")  # Free, fast model
except Exception as e:
    st.error(f"Error initializing Gemini Model: {e}")

# 🔹 Streamlit UI
st.set_page_config(page_title="FinTalk by Career Craaft", page_icon="📊")
st.title("📊 FinTalk by Career Craaft - AI-Powered Financial Data Analysis & AI chatbot")
st.subheader(":gray[Upload your financial Excel/CSV files and analyze the data with AI-powered insights]", divider='rainbow')

# 🔹 File Upload Section
uploaded_files = st.file_uploader("Upload Excel or CSV files", type=["xlsx", "csv"], accept_multiple_files=True)

# Dictionary to store uploaded data
data_dict = {}

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        try:
            if file_name.endswith(".xlsx"):
                xls = pd.ExcelFile(uploaded_file)
                sheets = xls.sheet_names
                st.write(f"📂 **{file_name}** - Sheets: {sheets}")
                data_dict[file_name] = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in sheets}
            else:
                data_dict[file_name] = pd.read_csv(uploaded_file)
                st.write(f"📂 **{file_name}** - Loaded CSV")
        except Exception as e:
            st.error(f"Error processing {file_name}: {e}")

# 🔹 Display Uploaded Data
if data_dict:
    st.subheader("📋 Preview Uploaded Data")
    selected_file = st.selectbox("Select a file to preview:", list(data_dict.keys()))

    if isinstance(data_dict[selected_file], dict):  # Excel with multiple sheets
        selected_sheet = st.selectbox("Select a sheet:", list(data_dict[selected_file].keys()))
        df = data_dict[selected_file][selected_sheet]
    else:
        df = data_dict[selected_file]

    st.dataframe(df.head())

    # 🔹 Data Summary & EDA
    st.subheader(":rainbow[Basic Data Analysis]", divider="rainbow")

    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Top & Bottom Rows", "Data Types", "Columns"])

    with tab1:
        st.write(f"📊 **Rows:** {df.shape[0]}, **Columns:** {df.shape[1]}")
        st.subheader("📈 Statistical Summary")
        st.dataframe(df.describe())

    with tab2:
        toprows = st.slider("Top Rows", 1, df.shape[0], key="topslider")
        st.dataframe(df.head(toprows))

        bottomrows = st.slider("Bottom Rows", 1, df.shape[0], key="bottomslider")
        st.dataframe(df.tail(bottomrows))

    with tab3:
        st.subheader("📌 Data Types")
        st.dataframe(df.dtypes)

    with tab4:
        st.subheader("📌 Column Names")
        st.write(list(df.columns))

    # 🔹 Column Value Counts
    st.subheader(":rainbow[Column Value Counts & Visualization]", divider="rainbow")
    with st.expander("🔍 View Value Counts"):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox("Choose column", options=list(df.columns))
        with col2:
            toprows = st.number_input("Top Rows", min_value=1, step=1)

        if st.button("Show Counts"):
            result = df[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)

            st.subheader("📊 Visualization")
            fig = px.bar(result, x=column, y="count", text="count", template="plotly_white")
            st.plotly_chart(fig)

            fig = px.line(result, x=column, y="count", text="count", template="plotly_white")
            st.plotly_chart(fig)

            fig = px.pie(result, names=column, values="count", template="plotly_white")
            st.plotly_chart(fig)

    # 🔹 GroupBy Analysis
    st.subheader(":rainbow[GroupBy: Simplify Your Data Analysis]", divider='rainbow')
    with st.expander("🔍 Group By Columns"):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect("Group By", options=list(df.columns))
        with col2:
            operation_col = st.selectbox("Operation Column", options=list(df.columns))
        with col3:
            operation = st.selectbox("Operation", ["sum", "max", "min", "mean", "median", "count"])

        if groupby_cols:
            result = df.groupby(groupby_cols).agg({operation_col: operation}).reset_index()
            st.dataframe(result)

            st.subheader("📊 Data Visualization")
            graph_type = st.selectbox("Select Graph Type", ['line', 'bar', 'scatter', 'pie', 'sunburst'])

            if graph_type == 'line':
                x_axis = st.selectbox('X axis', options=list(result.columns))
                y_axis = st.selectbox('Y axis', options=list(result.columns))
                color = st.selectbox('Color Info', options=[None] + list(result.columns))
                fig = px.line(result, x=x_axis, y=y_axis, color=color, markers='o')
                st.plotly_chart(fig)
            elif graph_type == 'bar':
                x_axis = st.selectbox('X axis', options=list(result.columns))
                y_axis = st.selectbox('Y axis', options=list(result.columns))
                color = st.selectbox('Color Info', options=[None] + list(result.columns))
                fig = px.bar(result, x=x_axis, y=y_axis, color=color, barmode='group')
                st.plotly_chart(fig)
            elif graph_type == 'scatter':
                x_axis = st.selectbox('X axis', options=list(result.columns))
                y_axis = st.selectbox('Y axis', options=list(result.columns))
                color = st.selectbox('Color Info', options=[None] + list(result.columns))
                size = st.selectbox('Size Column', options=[None] + list(result.columns))
                fig = px.scatter(result, x=x_axis, y=y_axis, color=color, size=size)
                st.plotly_chart(fig)
            elif graph_type == 'pie':
                values = st.selectbox('Numerical Values', options=list(result.columns))
                names = st.selectbox('Labels', options=list(result.columns))
                fig = px.pie(result, values=values, names=names)
                st.plotly_chart(fig)
            elif graph_type == 'sunburst':
                path = st.multiselect('Choose Path', options=list(result.columns))
                fig = px.sunburst(result, path=path, values=operation_col)
                st.plotly_chart(fig)

# 🔹 AI-Powered Q&A Section
st.subheader("🔍 Ask AI Questions Based on Your Data")
user_query = st.text_area("Enter your financial question:")

if st.button("Get AI Answer"):
    if not user_query:
        st.warning("Please enter a question.")
    elif not data_dict:
        st.warning("Please upload files first.")
    else:
        try:
            # Convert Data to String for AI Processing
            context = ""
            for file, content in data_dict.items():
                if isinstance(content, dict):  # Excel with multiple sheets
                    for sheet, df in content.items():
                        context += f"\n\n### File: {file}, Sheet: {sheet}\n{df.to_string(index=False)}"
                else:  # CSV file
                    context += f"\n\n### File: {file}\n{content.to_string(index=False)}"

            # AI Prompt
            prompt = f"Data:\n{context}\n\nUser Question: {user_query}"
            response = model.generate_content(prompt)

            st.success("🤖 AI Response:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error generating response: {e}")
