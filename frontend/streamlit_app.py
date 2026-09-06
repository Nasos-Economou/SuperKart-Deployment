
import streamlit as st
import requests
import pandas as pd
import io

# Page configuration
st.set_page_config(page_title="SuperKart Sales Predictor", page_icon="🛒", layout="wide")

st.title("🛒 SuperKart Sales Prediction")
st.markdown("Predict product-level sales revenue for SuperKart stores.")

# Backend API URL - when running in Docker, the containers communicate by service name
API_URL = "http://backend:7860"

# Create two tabs: one for single predictions, one for batch predictions
tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])

with tab1:
    st.subheader("Enter product and store details:")

    col1, col2 = st.columns(2)

    with col1:
        product_weight = st.number_input("Product Weight", min_value=1.0, max_value=30.0, value=12.0, step=0.1)
        sugar_content = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        allocated_area = st.number_input("Allocated Area", min_value=0.001, max_value=0.5, value=0.05, step=0.001, format="%.3f")
        product_mrp = st.number_input("Product MRP", min_value=10.0, max_value=300.0, value=140.0, step=0.5)
        product_id_char = st.selectbox("Product Category", ["FD", "DR", "NC"],
                                        format_func=lambda x: {"FD": "FD (Food)", "DR": "DR (Drinks)", "NC": "NC (Non-Consumable)"}[x])

    with col2:
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
        city_type = st.selectbox("City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
        store_age = st.number_input("Store Age (years)", min_value=1, max_value=50, value=17, step=1)
        product_type_cat = st.selectbox("Product Type", ["Perishables", "Non Perishables"])

    if st.button("Predict Sales", type="primary"):
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": sugar_content,
            "Product_Allocated_Area": allocated_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": city_type,
            "Store_Type": store_type,
            "Product_Id_char": product_id_char,
            "Store_Age_Years": store_age,
            "Product_Type_Category": product_type_cat,
        }

        try:
            response = requests.post(f"{API_URL}/v1/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Predicted Sales: **${result['predicted_sales']:,.2f}**")
            else:
                st.error(f"Error: {response.json()}")
        except Exception as e:
            st.error(f"Could not connect to the API: {e}")

with tab2:
    st.subheader("Upload a CSV file for batch predictions")
    st.markdown("The CSV must have columns: Product_Weight, Product_Sugar_Content, Product_Allocated_Area, Product_MRP, Store_Size, Store_Location_City_Type, Store_Type, Product_Id_char, Store_Age_Years, Product_Type_Category")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(batch_df.head())

        if st.button("Run Batch Prediction", type="primary"):
            try:
                csv_bytes = batch_df.to_csv(index=False).encode("utf-8")
                response = requests.post(
                    f"{API_URL}/v1/predictbatch",
                    files={"file": csv_bytes}
                )

                if response.status_code == 200:
                    predictions = response.json()
                    batch_df["Predicted_Sales"] = [predictions[str(i)] for i in range(len(batch_df))]
                    st.success("Batch predictions completed!")
                    st.dataframe(batch_df)
                else:
                    st.error(f"Error: {response.json()}")
            except Exception as e:
                st.error(f"Could not connect to the API: {e}")
