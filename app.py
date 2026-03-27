import streamlit as st
import pandas as pd
from database import init_db, add_user, verify_user, fetch_user_transactions, add_transaction
from datetime import date

st.set_page_config(page_title="Budget Vault", layout="wide")
init_db()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = None
    st.session_state['username'] = ""

if not st.session_state['logged_in']:
    st.title("Budget Planner Portal")
    tab1, tab2 = st.tabs(["Login", "Register New User"])
    
    with tab1:
        u_name = st.text_input("Username")
        u_pass = st.text_input("Password", type="password")
        if st.button("Access Vault"):
            user_id = verify_user(u_name, u_pass)
            if user_id:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user_id
                st.session_state['username'] = u_name
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials")

    with tab2:
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")
        if st.button("Create Your Account"):
            if add_user(new_user, new_pass):
                st.success("Account Saved!")
            else:
                st.error("Username already exists in vault.")

else:
    st.title(f"Financial Summary: {st.session_state['username']}")
    
    with st.sidebar:
        st.header("New Entry")
        with st.form("entry_form", clear_on_submit=True):
            t_date = st.date_input("Date", date.today())
            t_cat = st.selectbox("Category", ["Salary", "Food", "Rent", "Travel", "Fees", "Misc"])
            t_amt = st.number_input("Amount (INR)", min_value=0.0)
            t_type = st.radio("Type", ["Income", "Expense"])
            if st.form_submit_button("Save"):
                if t_amt > 0:
                    add_transaction(st.session_state['user_id'], str(t_date), t_cat, t_amt, t_type)
                    st.rerun()
        
        if st.button("Secure Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

    # Data Calculations
    data = fetch_user_transactions(st.session_state['user_id'])
    df = pd.DataFrame(data, columns=['id', 'user_id', 'date', 'category', 'amount', 'type'])

    if not df.empty:
        inc = df[df['type'] == 'Income']['amount'].sum()
        exp = df[df['type'] == 'Expense']['amount'].sum()
        savings = inc - exp

        # --- ADVANCED UI: COLORED METRICS ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Income", f"₹{inc}")
        c2.metric("Total Expense", f"₹{exp}")
        # Delta color changes based on profit/loss
        c3.metric("Net Savings", f"₹{savings}", delta=f"₹{savings}", delta_color="normal" if savings >= 0 else "inverse")

        st.markdown("---")
        
        # Spending Chart
        exp_df = df[df['type'] == 'Expense']
        if not exp_df.empty:
            st.subheader("Expense Distribution")
            chart_data = exp_df.groupby('category')['amount'].sum()
            st.bar_chart(chart_data)
            
        # --- ADVANCED UI: DATA EXPORT ---
        st.subheader("Transaction History")
        st.dataframe(df[['date', 'category', 'amount', 'type']], use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Transaction Report (CSV)",
            data=csv,
            file_name=f"{st.session_state['username']}_report.csv",
            mime='text/csv'
        )
    else:
        st.info("Vault is currently empty. Please add your first transaction.")