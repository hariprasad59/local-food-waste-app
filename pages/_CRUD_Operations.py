import streamlit as st
from dbutil import run_query, run_modify
import pandas as pd
import datetime

st.title(" CRUD Operations")

st.markdown("""
    <style>
        body {
            background-color: #f0f5f5;
        }
        .stApp {
            background-color: #f0f5f5;
        }
    </style>
""", unsafe_allow_html=True)

section = st.sidebar.selectbox(
    "Select Table to Manage",
    ["Providers", "Receivers", "FoodList", "Claims"]
)
st.header(f"Manage {section}")

if section == "Providers":
    with st.expander(" Add New Provider", expanded=False):
        with st.form("add_provider"):
            pid = st.text_input("Provider_ID")
            name = st.text_input("Name")
            ptype = st.text_input("Type")
            address = st.text_area("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submitted = st.form_submit_button("Add Provider")

            if submitted:
                try:
                    if pid:
                        q = """INSERT INTO Providers (Provider_ID, Name, Type, Address, City, Contact)
                               VALUES (%s,%s,%s,%s,%s,%s)"""
                        params = (int(pid), name, ptype, address, city, contact)
                    else:
                        q = """INSERT INTO Providers (Name, Type, Address, City, Contact)
                               VALUES (%s,%s,%s,%s,%s)"""
                        params = (name, ptype, address, city, contact)
                    cnt = run_modify(q, params)
                    st.success(f"Inserted {cnt} row successfully.")
                except Exception as e:
                    st.error(f"Error: {e}")

    with st.expander(" Update or Delete Provider", expanded=False):
        df = run_query("SELECT * FROM Providers ORDER BY Provider_ID")

        if not df.empty:
            st.dataframe(df, use_container_width=True)
            pid_to_update = st.selectbox("Select Provider_ID to Update/Delete", df["Provider_ID"], key="provider_select")
            selected_provider = df.loc[df["Provider_ID"] == pid_to_update].iloc[0]

            with st.form("update_provider"):
                name = st.text_input("Name", value=selected_provider["Name"])
                ptype = st.text_input("Type", value=selected_provider["Type"])
                address = st.text_area("Address", value=selected_provider["Address"]) 
                city = st.text_input("City", value=selected_provider["City"])
                contact = st.text_input("Contact", value=selected_provider["Contact"])
                update_btn = st.form_submit_button("Update Provider")
                
                if update_btn:
                    q = """UPDATE Providers SET Name=%s, Type=%s, Address=%s, City=%s, Contact=%s WHERE Provider_ID=%s"""
                    run_modify(q, (name, ptype, address, city, contact, pid_to_update))
                    st.success("Provider updated successfully! Refresh to see changes.")
            
            st.markdown("---")

            if st.button(f" Delete Provider {pid_to_update}", key="delete_provider_btn"):
                q = "DELETE FROM Providers WHERE Provider_ID=%s"
                run_modify(q, (pid_to_update,))
                st.warning(f"Provider {pid_to_update} deleted successfully. Please refresh the page.")
        else:
            st.info("No providers found in the database.")


elif section == "Receivers":
    # --- ADD RECEIVER ---
    with st.expander("Add New Receiver", expanded=False):
        with st.form("add_receiver"):
            rid = st.text_input("Receiver_ID (optional)")
            name = st.text_input("Name")
            rtype = st.text_input("Type")
            city = st.text_input("City")
            contact = st.text_input("Contact")
            submitted = st.form_submit_button("Add Receiver")

            if submitted:
                try:
                    if rid:
                        q = """INSERT INTO Receivers (Receiver_ID, Name, Type, City, Contact)
                               VALUES (%s,%s,%s,%s,%s)"""
                        params = (int(rid), name, rtype, city, contact)
                    else:
                        q = """INSERT INTO Receivers (Name, Type, City, Contact)
                               VALUES (%s,%s,%s,%s)"""
                        params = (name, rtype, city, contact)
                    run_modify(q, params)
                    st.success(" Receiver added successfully! Refresh to see it in the table below.")
                except Exception as e:
                    st.error(f"Error: {e}")

 
    with st.expander(" Update or  Delete Receiver", expanded=False):
        df = run_query("SELECT * FROM Receivers ORDER BY Receiver_ID")

        if not df.empty:
            st.dataframe(df, use_container_width=True)
            rid_to_update = st.selectbox("Select Receiver_ID to Update/Delete", df["Receiver_ID"], key="rid_select")

            selected_receiver = df.loc[df["Receiver_ID"] == rid_to_update].iloc[0]

            with st.form("update_receiver"):
                name = st.text_input("Name", value=selected_receiver["Name"])
                rtype = st.text_input("Type", value=selected_receiver["Type"])
                city = st.text_input("City", value=selected_receiver["City"])
                contact = st.text_input("Contact", value=selected_receiver["Contact"])
                
                
                update_btn = st.form_submit_button("Update Receiver")

                if update_btn:
                    q = """UPDATE Receivers SET Name=%s, Type=%s, City=%s, Contact=%s WHERE Receiver_ID=%s"""
                    run_modify(q, (name, rtype, city, contact, rid_to_update))
                    st.success(" Receiver updated! Refresh to see changes.")

            st.markdown("---")
            if st.button(f" Delete Receiver {rid_to_update}", key="delete_rid_btn_outside"):
                q = "DELETE FROM Receivers WHERE Receiver_ID=%s"
                run_modify(q, (rid_to_update,))
                st.warning(" Receiver deleted. Please refresh the page.")
        else:
            st.info("No receivers found in the database.")


elif section == "FoodList":
    with st.expander(" Add New Food Item", expanded=False):
        with st.form("add_food"):
            st.subheader("Item Details")
            fid = st.text_input("Food_ID (optional)")
            name = st.text_input("Food Name")
            type_ = st.text_input("Food Type (e.g., Produce, Prepared)") 
            quantity = st.number_input("Quantity", min_value=0, step=1)
            expiry = st.date_input("Expiry Date")
            
            st.subheader("Relational Details")
            provider_id = st.text_input("Provider_ID (REQUIRED)", key="new_list_pid")
            provider_type = st.text_input("Provider_Type")
            location = st.text_area("Location")
            food_type = st.text_input("Food_Type (e.g., Vegan, Non-Vegetarian)")
            meal_type = st.selectbox("Meal_Type", ["Any", "Breakfast", "Lunch", "Dinner", "Snacks"]) 
            
            submitted = st.form_submit_button("Add Food")
            
            if submitted:
                columns = "Food_Name, Type, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type"
                placeholders = "%s, %s, %s, %s, %s, %s, %s, %s, %s"
                params_base = (name, type_, quantity, expiry, provider_id, provider_type, location, food_type, meal_type)

                try:
                    if fid:
                        q = f"INSERT INTO FoodListings (Food_ID, {columns}) VALUES (%s, {placeholders})"
                        params = (int(fid),) + params_base
                    else:
                        q = f"INSERT INTO FoodListings ({columns}) VALUES ({placeholders})"
                        params = params_base
                        
                    run_modify(q, params)
                    st.success(" Food added successfully! Refresh to see it in the table below.")
                except Exception as e:
                    st.error(f"Error: {e}")

    with st.expander("Update or  Delete Food Item", expanded=False):
        df = run_query("SELECT * FROM FoodListings ORDER BY Food_ID")

        if not df.empty:
            st.dataframe(df, use_container_width=True)
            fid_to_update = st.selectbox("Select Food_ID to Update/Delete", df["Food_ID"], key="fid_select")

            selected_food = df.loc[df["Food_ID"] == fid_to_update].iloc[0]

            with st.form("update_food"):
                name = st.text_input("Food Name", value=selected_food["Food_Name"])
                type_ = st.text_input("Food Type", value=selected_food["Type"] if "Type" in selected_food else "") 
                quantity = st.number_input("Quantity", min_value=0, step=1, value=int(selected_food["Quantity"]))
                
                expiry_date = selected_food["Expiry_Date"]
                if not isinstance(expiry_date, datetime.date):
                    expiry_date = datetime.strptime(str(expiry_date), '%Y-%m-%d').date()
                expiry = st.date_input("Expiry Date", value=expiry_date)
                
                provider_id = st.text_input("Provider_ID (REQUIRED)", value=str(selected_food["Provider_ID"]))
                provider_type = st.text_input("Provider_Type", value=selected_food["Provider_Type"])
                location = st.text_area("Location", value=selected_food["Location"])
                food_type = st.text_input("Food_Type", value=selected_food["Food_Type"])
                
                meal_options = ["Any", "Breakfast", "Lunch", "Dinner", "Snacks"]
                initial_index = meal_options.index(selected_food["Meal_Type"]) if selected_food["Meal_Type"] in meal_options else 0
                meal_type = st.selectbox("Meal_Type", meal_options, index=initial_index)


                update_btn = st.form_submit_button("Update Food Item")

                if update_btn:
                    q = """UPDATE FoodListings 
                           SET Food_Name=%s, Type=%s, Quantity=%s, Expiry_Date=%s, Provider_ID=%s, 
                               Provider_Type=%s, Location=%s, Food_Type=%s, Meal_Type=%s 
                           WHERE Food_ID=%s"""
                    params = (name, type_, quantity, expiry, provider_id, provider_type, location, food_type, meal_type, fid_to_update)
                    run_modify(q, params)
                    st.success(" Food item updated! Refresh to see changes.")

            st.markdown("---")
            if st.button("Delete Selected Food Item", key="delete_fid_btn_outside"):
                q = "DELETE FROM FoodListings WHERE Food_ID=%s"
                run_modify(q, (fid_to_update,))
                st.warning("Food item deleted. Please refresh the page.")
        else:
            st.info("No food listings found in the database.")


elif section == "Claims":
    with st.expander("Add New Claim", expanded=False):
        with st.form("add_claim"):
            cid = st.text_input("Claim_ID (optional)")
            food_id= st.text_input("Food_ID")
            receiver_id = st.text_input("Receiver_ID")
            status = st.selectbox("Status", ["Pending", "Approved", "Rejected"], index=0)
            date = st.date_input("Timestamp")
            submitted = st.form_submit_button("Add Claim")

            if submitted:
                try:
                    if cid:
                        q = "INSERT INTO Claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp) VALUES (%s,%s,%s,%s,%s)"
                        params = (int(cid), food_id, receiver_id, status, date)
                    else:
                        q = "INSERT INTO Claims (Food_ID, Receiver_ID, Status, Timestamp) VALUES (%s,%s,%s,%s)"
                        params = (food_id, receiver_id, status, date)
                    run_modify(q, params)
                    st.success("Claim added successfully! Refresh to see it in the table below.")
                except Exception as e:
                    st.error(f"Error: {e}")

    with st.expander(" Update or  Delete Claim", expanded=False):
        df = run_query("SELECT * FROM Claims ORDER BY Claim_ID")

        if not df.empty:
            st.dataframe(df, use_container_width=True)
            cid_to_update = st.selectbox("Select Claim_ID to Update/Delete", df["Claim_ID"], key="cid_select")

            selected_claim = df.loc[df["Claim_ID"] == cid_to_update].iloc[0]

            with st.form("update_claim"):
                receiver_id = st.text_input("Receiver_ID", value=selected_claim["Receiver_ID"])
                food_id_val = st.text_input("Food_ID", value=selected_claim["Food_ID"])
                
                claim_date_val = selected_claim["Timestamp"]
                if not isinstance(claim_date_val, datetime.date):
                    claim_date_val = datetime.strptime(str(claim_date_val).split(' ')[0], '%Y-%m-%d').date()
                date = st.date_input("Timestamp", value=claim_date_val)
                
                status_options = ["Pending", "Approved", "Rejected"]
                initial_index = status_options.index(selected_claim["Status"])
                status = st.selectbox("Status", status_options, index=initial_index)
                
                update_btn = st.form_submit_button("Update Claim")

                if update_btn:
                    q = """UPDATE Claims SET Food_ID=%s, Receiver_ID=%s, Status=%s, Timestamp=%s WHERE Claim_ID=%s"""
                    run_modify(q, (food_id_val, receiver_id, status, date, cid_to_update))
                    st.success(" Claim updated! Refresh to see changes.")

            st.markdown("---")
            if st.button(f" Delete Claim {cid_to_update}", key="delete_cid_btn_outside"):
                q = "DELETE FROM Claims WHERE Claim_ID=%s"
                run_modify(q, (cid_to_update,))
                st.warning(" Claim deleted. Please refresh the page.")
        else:
            st.info("No claims found in the database.")