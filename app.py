import streamlit as st
import pandas as pd
from database import init_db, add_user, verify_user, fetch_user_transactions, add_transaction
from datetime import date

# 1. Page Configuration (Always at the very top)
st.set_page_config(page_title="Private Budget Planner", layout="wide")

# 2. Initialize Database
init_db()

# 3. Initialize Session State (Memory for the Login)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = None
    st.session_state['username'] = ""

# --- LOGIN / SIGNUP PAGE ---
if not st.session_state['logged_in']:
    st.title(" Secure Budget Vault")
    
    tab1, tab2 = st.tabs(["Login", "Create Account"])
    
    with tab1:
        u_name = st.text_input("Username", key="login_user")
        u_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user_id = verify_user(u_name, u_pass)
            if user_id:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user_id
                st.session_state['username'] = u_name
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Register"):
            if add_user(new_user, new_pass):
                st.success("Account created successfully! Go to the Login tab.")
            else:
                st.error("Username already exists.")

# --- MAIN DASHBOARD
else:
    st.title(f"Welcome back, {st.session_state['username']}! ")
    
    # Sidebar for Logout and Input
    with st.sidebar:
        st.header("Add Transaction")
        with st.form("input_form", clear_on_submit=True):
            t_date = st.date_input("Date", date.today())
            t_cat = st.selectbox("Category", ["Salary", "Food", "Rent", "Travel", "Bills", "Other"])
            t_amt = st.number_input("Amount", min_value=0.0, step=10.0)
            t_type = st.radio("Type", ["Income", "Expense"])
            submitted = st.form_submit_button("Save to Records")

            if submitted:
                if t_amt > 0:
                    # Logic: Passing the user_id so it saves to YOUR private vault
                    add_transaction(st.session_state['user_id'], str(t_date), t_cat, t_amt, t_type)
                    st.success("Transaction Saved!")
                    st.rerun()
                else:
                    st.error("Please enter an amount > 0")
        
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    # Data Processing Logic
    data = fetch_user_transactions(st.session_state['user_id'])
    df = pd.DataFrame(data, columns=['id', 'user_id', 'date', 'category', 'amount', 'type'])

    if not df.empty:
        # Calculate Income vs Expense
        total_inc = df[df['type'] == 'Income']['amount'].sum()
        total_exp = df[df['type'] == 'Expense']['amount'].sum()
        savings = total_inc - total_exp

        # Display Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"₹{total_inc}")
        col2.metric("Total Expenses", f"₹{total_exp}")
        col3.metric("Net Savings", f"₹{savings}")

        st.markdown("---")
        
        # Spending Analysis Chart
        st.subheader("Spending Analysis")
        exp_df = df[df['type'] == 'Expense']
        if not exp_df.empty:
            chart_data = exp_df.groupby('category')['amount'].sum()
            st.bar_chart(chart_data)
        else:
            st.info("Add an expense to see the chart!")
            
        # Raw Data Table
        st.subheader("Transaction History")
        st.dataframe(df[['date', 'category', 'amount', 'type']], use_container_width=True)
    else:
        st.info("Your vault is empty! Add an entry in the sidebar to start tracking.")