import streamlit as st
import pandas as pd
from db import get_connection
from auth_module import register_user, login_user
from datetime import datetime


st.title("Client Query Management System")

if "user" not in st.session_state:
    st.session_state.user = None


def logout():
    st.session_state.user = None


def show_client_dashboard():
    st.subheader("Submit Query")

    with st.form("submit_query_form", clear_on_submit=True):
        email = st.text_input("Email")
        mobile = st.text_input("Mobile Number")
        heading = st.text_input("Query Heading")
        description = st.text_area("Query Description")
        submitted = st.form_submit_button("Submit Query")

    if submitted:
        if not email or not mobile or not heading:
            st.warning("Please fill all required fields")
            return

        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO queries
                    (mail_id, mobile_number, query_heading, query_description, status, query_created_time)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (email, mobile, heading, description, "Open", datetime.now()),
            )
            conn.commit()
            st.success("Query submitted successfully")
        except Exception as e:
            st.error(f"Database Error: {e}")
        finally:
            if conn:
                conn.close()


def show_support_dashboard():
    st.subheader("Support Dashboard")

    conn = None
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM queries", conn)

        if df.empty:
            st.info("No queries available")
        else:
            st.dataframe(df)

        with st.form("close_query_form"):
            query_id = st.number_input("Enter Query ID to Close", min_value=1, step=1)
            close_clicked = st.form_submit_button("Close Query")

        if close_clicked:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE queries
                SET status=%s, query_closed_time=%s
                WHERE query_id=%s
                """,
                ("Closed", datetime.now(), query_id),
            )
            conn.commit()

            if cursor.rowcount:
                st.success("Query closed successfully")
                st.rerun()
            else:
                st.warning("No query found with that ID")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if conn:
            conn.close()


if st.session_state.user:
    username, role = st.session_state.user[1], st.session_state.user[2]
    st.sidebar.write(f"Logged in as {username} ({role})")
    st.sidebar.button("Logout", on_click=logout)

    if role == "Client":
        show_client_dashboard()
    elif role == "Support":
        show_support_dashboard()
else:
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Register":
        st.subheader("Create Account")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Client", "Support"])

        if st.button("Register"):
            if not username or not password:
                st.warning("Please fill all fields")
            else:
                try:
                    register_user(username, password, role)
                    st.success("User registered successfully")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif choice == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)

            if user:
                st.session_state.user = user
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")
