import streamlit as st
import pandas as pd
from database import init_db, add_transaction, fetch_all_transactions
from datetime import date

#initialize the database
init_db()

st.set_page_config(page_title = "Budget Planner", layout = "wide")
st.title("Simple Budget Planner")

#sidebar for user input
st.sidebar.header("Add Transaction")
with st.sidebar.form("input_form", clear_on_submit=True):
    t_date = st.date_input("Date", date.today())
    t_cat = st.selectbox("Category", ["Salary", "Food", "Rent", "Travel", "Bills", "Other"])
    t_amt = st.number_input("Amount", min_value = 0.0, step = 10.0)
    t_type = st.radio("Type", ["Income", "Expense"])

    #save data when button is clicked
    submitted = st.form_submit_button("Save to Records")
    if submitted:
        if t_amt > 0:
            add_transaction(str(t_date), t_cat, t_amt, t_type)
            st.sidebar.success("Saved successfully")
        else:
            st.sidebar.error("Not Saved!... Please enter an amount greater than 0")

#Monthly savings report
df = fetch_all_transactions()

if not df.empty:
    #calculate income vs expense
    total_inc = df[df['type'] == 'Income']['amount'].sum()
    total_exp = df[df['type'] == 'Expense']['amount'].sum()
    savings = total_inc - total_exp

    #display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_inc}")
    col2.metric("Total Expenses", f"₹{total_exp}")
    col3.metric("Net Savings", f"₹{savings}")

    #Visualizations
    st.subheader("Spending Analysis")
    st.bar_chart(df[df['type'] == 'Expense'].groupby('category')['amount'].sum())
    
    st.subheader("Transaction History")
    st.dataframe(df.sort_values(by="date", ascending=False))
else:
    st.info("Your vault is empty! Add an entry in the sidebar.")

            
