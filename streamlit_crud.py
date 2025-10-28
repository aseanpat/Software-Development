import streamlit as st
import pandas as pd
import sqlite3
import os

# Database file path
DB_FILE = "data.db"

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            city TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all_records():
    """Get all records from database"""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

def add_record(name, email, age, city):
    """Add new record to database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, age, city) VALUES (?, ?, ?, ?)", 
                   (name, email, age, city))
    conn.commit()
    conn.close()

def update_record(record_id, name, email, age, city):
    """Update existing record in database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name=?, email=?, age=?, city=? WHERE id=?", 
                   (name, email, age, city, record_id))
    conn.commit()
    conn.close()

def delete_record(record_id):
    """Delete record from database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (record_id,))
    conn.commit()
    conn.close()

def main():
    st.title("SQL CRUD Application - Patrick Salamera")
    st.sidebar.title("Navigation")
    
    # Initialize database
    init_db()
    
    # Navigation
    page = st.sidebar.selectbox("Choose Operation", ["View Records", "Add Record", "Update Record", "Delete Record"])
    
    if page == "View Records":
        view_records()
    elif page == "Add Record":
        add_new_record()
    elif page == "Update Record":
        update_existing_record()
    elif page == "Delete Record":
        delete_existing_record()

def view_records():
    """Display all records"""
    st.header("View Records")
    
    df = get_all_records()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.info(f"Total records: {len(df)}")
    else:
        st.warning("No records found. Add some records first!")

def add_new_record():
    """Add new record"""
    st.header("Add New Record")
    
    with st.form("add_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        city = st.text_input("City")
        
        submitted = st.form_submit_button("Add Record")
        
        if submitted:
            if name and email:
                add_record(name, email, age, city)
                st.success("Record added successfully!")
                st.rerun()
            else:
                st.error("Name and Email are required!")

def update_existing_record():
    """Update existing record"""
    st.header("Update Record")
    
    df = get_all_records()
    if df.empty:
        st.warning("No records to update!")
        return
    
    # Select record to update
    record_options = [f"ID: {row['id']} - {row['name']}" for _, row in df.iterrows()]
    selected = st.selectbox("Select record to update", record_options)
    
    if selected:
        record_id = int(selected.split(":")[1].split(" -")[0])
        record = df[df['id'] == record_id].iloc[0]
        
        with st.form("update_form"):
            name = st.text_input("Name", value=record['name'])
            email = st.text_input("Email", value=record['email'])
            age = st.number_input("Age", min_value=1, max_value=120, value=int(record['age']))
            city = st.text_input("City", value=record['city'])
            
            submitted = st.form_submit_button("Update Record")
            
            if submitted:
                if name and email:
                    update_record(record_id, name, email, age, city)
                    st.success("Record updated successfully!")
                    st.rerun()
                else:
                    st.error("Name and Email are required!")

def delete_existing_record():
    """Delete existing record"""
    st.header("Delete Record")
    
    df = get_all_records()
    if df.empty:
        st.warning("No records to delete!")
        return
    
    # Select record to delete
    record_options = [f"ID: {row['id']} - {row['name']}" for _, row in df.iterrows()]
    selected = st.selectbox("Select record to delete", record_options)
    
    if selected:
        record_id = int(selected.split(":")[1].split(" -")[0])
        record = df[df['id'] == record_id].iloc[0]
        
        # Show record details
        st.write("**Record to delete:**")
        st.json(record.to_dict())
        
        if st.button("Confirm Delete", type="primary"):
            delete_record(record_id)
            st.success("Record deleted successfully!")
            st.rerun()

if __name__ == "__main__":
    main()
