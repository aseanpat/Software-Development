import streamlit as st
import pandas as pd
import json
import os

# Data file path
DATA_FILE = "data.json"

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    st.title("Simple CRUD Application")
    st.sidebar.title("Navigation")
    
    # Load existing data
    if 'data' not in st.session_state:
        st.session_state.data = load_data()
    
    # Navigation
    page = st.sidebar.selectbox("Choose Operation", ["View Records", "Add Record", "Update Record", "Delete Record"])
    
    if page == "View Records":
        view_records()
    elif page == "Add Record":
        add_record()
    elif page == "Update Record":
        update_record()
    elif page == "Delete Record":
        delete_record()

def view_records():
    """Display all records"""
    st.header("View Records")
    
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        st.dataframe(df, use_container_width=True)
        st.info(f"Total records: {len(st.session_state.data)}")
    else:
        st.warning("No records found. Add some records first!")

def add_record():
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
                new_record = {
                    "id": len(st.session_state.data) + 1,
                    "name": name,
                    "email": email,
                    "age": age,
                    "city": city
                }
                st.session_state.data.append(new_record)
                save_data(st.session_state.data)
                st.success("Record added successfully!")
                st.rerun()
            else:
                st.error("Name and Email are required!")

def update_record():
    """Update existing record"""
    st.header("Update Record")
    
    if not st.session_state.data:
        st.warning("No records to update!")
        return
    
    # Select record to update
    record_options = [f"ID: {r['id']} - {r['name']}" for r in st.session_state.data]
    selected = st.selectbox("Select record to update", record_options)
    
    if selected:
        record_id = int(selected.split(":")[1].split(" -")[0])
        record = next(r for r in st.session_state.data if r['id'] == record_id)
        
        with st.form("update_form"):
            name = st.text_input("Name", value=record['name'])
            email = st.text_input("Email", value=record['email'])
            age = st.number_input("Age", min_value=1, max_value=120, value=record['age'])
            city = st.text_input("City", value=record['city'])
            
            submitted = st.form_submit_button("Update Record")
            
            if submitted:
                if name and email:
                    # Update the record
                    for i, r in enumerate(st.session_state.data):
                        if r['id'] == record_id:
                            st.session_state.data[i] = {
                                "id": record_id,
                                "name": name,
                                "email": email,
                                "age": age,
                                "city": city
                            }
                            break
                    
                    save_data(st.session_state.data)
                    st.success("Record updated successfully!")
                    st.rerun()
                else:
                    st.error("Name and Email are required!")

def delete_record():
    """Delete existing record"""
    st.header("Delete Record")
    
    if not st.session_state.data:
        st.warning("No records to delete!")
        return
    
    # Select record to delete
    record_options = [f"ID: {r['id']} - {r['name']}" for r in st.session_state.data]
    selected = st.selectbox("Select record to delete", record_options)
    
    if selected:
        record_id = int(selected.split(":")[1].split(" -")[0])
        record = next(r for r in st.session_state.data if r['id'] == record_id)
        
        # Show record details
        st.write("**Record to delete:**")
        st.json(record)
        
        if st.button("Confirm Delete", type="primary"):
            st.session_state.data = [r for r in st.session_state.data if r['id'] != record_id]
            save_data(st.session_state.data)
            st.success("Record deleted successfully!")
            st.rerun()

if __name__ == "__main__":
    main()