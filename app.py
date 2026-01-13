import streamlit as st
import numpy as np
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. Page config
# -----------------------------
st.set_page_config(page_title="Customer Churn Prediction", page_icon="📊", layout="wide")
st.title("📊 Customer Churn Prediction App")
st.write("Predict whether a customer is likely to churn and explore why customers churn using the dashboard.")

# -----------------------------
# 2. Load trained model
# -----------------------------
with open("churn_model.pkl", "rb") as file:
    model = pickle.load(file)

# -----------------------------
# 3. Sidebar for view selection
# -----------------------------
view_option = st.sidebar.selectbox("Choose View", ["Predict Customer Churn", "Churn Dashboard"])

# -----------------------------
# 4. Load dataset for dashboard
# -----------------------------
# Use your dataset for visualizations
df = pd.read_csv("Telco-Customer-Churn.csv")

# -----------------------------
# 5. Prediction Form
# -----------------------------
if view_option == "Predict Customer Churn":
    st.subheader("📝 Customer Details")

    col1, col2, col3 = st.columns(3)

    # Numeric features
    with col1:
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
        MonthlyCharges = st.number_input("Monthly Charges", min_value=0.0, max_value=1000.0, value=70.0)
        TotalCharges = st.number_input("Total Charges", min_value=0.0, max_value=10000.0, value=1500.0)
        SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])

    # Categorical features - Part 1
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        Partner = st.selectbox("Partner", ["Yes", "No"])
        Dependents = st.selectbox("Dependents", ["Yes", "No"])
        PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
        MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
        InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        OnlineSecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        OnlineBackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])

    # Categorical features - Part 2
    with col3:
        DeviceProtection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        TechSupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        StreamingTV = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
        Contract = st.selectbox("Contract", ["Month-to-Month", "One Year", "Two Year"])
        PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
        PaymentMethod = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])

    # -----------------------------
    # Encode categorical features
    # -----------------------------
    gender_map = {"Female":0, "Male":1}
    yes_no_map = {"No":0, "Yes":1}
    internet_map = {"DSL":0, "Fiber optic":1, "No":2}
    contract_map = {"Month-to-Month":0, "One Year":1, "Two Year":2}
    payment_map = {"Electronic check":0, "Mailed check":1, "Bank transfer (automatic)":2, "Credit card (automatic)":3}
    no_internet_map = {"No internet service":0, "Yes":1, "No":2}
    multiple_lines_map = {"No phone service":0, "No":1, "Yes":2}

    gender = gender_map[gender]
    Partner = yes_no_map[Partner]
    Dependents = yes_no_map[Dependents]
    PhoneService = yes_no_map[PhoneService]
    MultipleLines = multiple_lines_map[MultipleLines]
    InternetService = internet_map[InternetService]
    OnlineSecurity = no_internet_map[OnlineSecurity]
    OnlineBackup = no_internet_map[OnlineBackup]
    DeviceProtection = no_internet_map[DeviceProtection]
    TechSupport = no_internet_map[TechSupport]
    StreamingTV = no_internet_map[StreamingTV]
    StreamingMovies = no_internet_map[StreamingMovies]
    Contract = contract_map[Contract]
    PaperlessBilling = yes_no_map[PaperlessBilling]
    PaymentMethod = payment_map[PaymentMethod]

    # -----------------------------
    # Arrange features in correct order
    # -----------------------------
    input_data = np.array([[
        gender, SeniorCitizen, Partner, Dependents, tenure,
        PhoneService, MultipleLines, InternetService, OnlineSecurity,
        OnlineBackup, DeviceProtection, TechSupport, StreamingTV,
        StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
        MonthlyCharges, TotalCharges, 0  # placeholder for missing 20th feature if needed
    ]])

    # -----------------------------
    # Predict button
    # -----------------------------
    st.subheader("Prediction")
    if st.button("Predict Churn"):
        prediction = model.predict(input_data)
        if prediction[0] == 1:
            st.markdown("### ⚠️ Customer is likely to **churn**!", unsafe_allow_html=True)
            st.error("Consider contacting the customer or offering incentives to retain them.")
        else:
            st.markdown("### ✅ Customer is likely to **stay**!", unsafe_allow_html=True)
            st.success("No immediate action required.")

# -----------------------------
# 6. Churn Dashboard
# -----------------------------
if view_option == "Churn Dashboard":
    st.subheader("📊 Churn Insights Dashboard")

    # Churn distribution
    st.markdown("### Churn Distribution")
    churn_counts = df['Churn'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', colors=['#2ca02c','#d62728'])
    st.pyplot(fig1)

    # Churn by Contract
    st.markdown("### Churn by Contract Type")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=df, x="Contract", hue="Churn", palette="coolwarm", ax=ax2)
    st.pyplot(fig2)

    # Churn by Internet Service
    st.markdown("### Churn by Internet Service")
    fig3, ax3 = plt.subplots()
    sns.countplot(data=df, x="InternetService", hue="Churn", palette="Set2", ax=ax3)
    st.pyplot(fig3)

    # Monthly Charges vs Churn
    st.markdown("### Monthly Charges vs Churn")
    fig4, ax4 = plt.subplots()
    sns.boxplot(data=df, x="Churn", y="MonthlyCharges", palette="Set3", ax=ax4)
    st.pyplot(fig4)

    # Tenure vs Churn
    st.markdown("### Tenure vs Churn")
    fig5, ax5 = plt.subplots()
    sns.boxplot(data=df, x="Churn", y="tenure", palette="Set1", ax=ax5)
    st.pyplot(fig5)
