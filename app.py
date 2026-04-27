import auth_module
print(dir(auth_module))
import streamlit as st
import pandas as pd
from db import get_connection
from auth_module import register_user, login_user
import datetime

st.title("📊 Client Query Management System")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- REGISTER ----------------
if choice == "Register":
    st.subheader("Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Client", "Support"])

    if st.button("Register"):
        register_user(username, password, role)
        st.success("User Registered Successfully")

# ---------------- LOGIN ----------------
elif choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)

        if user:
            st.success("Login Successful")

            role = user[2]

            # CLIENT PAGE
            if role == "Client":
                st.subheader("Submit Query")

                email = st.text_input("Email")
                mobile = st.text_input("Mobile")
                heading = st.text_input("Heading")
                description = st.text_area("Description")

                if st.button("Submit Query"):
                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO queries 
                        (mail_id, mobile_number, query_heading, query_description, status, query_created_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (email, mobile, heading, description, "Open", datetime.datetime.now()))

                    conn.commit()
                    conn.close()

                    st.success("Query Submitted Successfully")

            # SUPPORT PAGE
            elif role == "Support":
                st.subheader("Support Dashboard")

                conn = get_connection()
                df = pd.read_sql("SELECT * FROM queries", conn)

                st.dataframe(df)

                query_id = st.number_input("Enter Query ID to Close")

                if st.button("Close Query"):
                    cursor = conn.cursor()

                    cursor.execute("""
                        UPDATE queries 
                        SET status='Closed', query_closed_time=%s 
                        WHERE query_id=%s
                    """, (datetime.datetime.now(), query_id))

                    conn.commit()
                    st.success("Query Closed")

                conn.close()

        else:
            st.error("Invalid Credentials")