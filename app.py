import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from messages import app_instructions, message_body, message_2
from data import mass_mail

st.set_page_config(page_title="EcoTotes Chaser")   

st.title("Proof and Company's automated ecoTotes Chaser")

selected = option_menu(menu_title=None, options=["Home", "Send Emails"],orientation="horizontal")

if selected == "Home":
    st.write(app_instructions())

elif selected == "Send Emails":

    try:
        file = st.file_uploader("Upload your Excel file here", type="xlsx")
    except ValueError:
        st.warning("Please ensure that all required sheets and columns are included in your file.")
        st.warning("Note: Sheet and column names are case-sensitive")
    
    if file is not None:
        sheet_names = ["Mastersheet", "Branch with Emails", "Recording"]
        master_df, email_df, recording_df = [pd.read_excel(file, sheet_name = sheet) for sheet in sheet_names]
        branch_names_mastersheet = master_df["Branch"].unique()

        email_type = st.selectbox("Email Type", options=["1st Email Chaser", "2nd Email Chaser"], placeholder="Choose your email type")
        
        with st.form("Credentials", clear_on_submit=True):
            col1, col2 = st.columns(2)
            first_name = col1.text_input("First name", placeholder="John")
            last_name = col2.text_input("Last name", placeholder="Doe")
        
            if first_name == "" or last_name == "":
                st.warning("Ensure all the above fields are filled up")
                
            submit_btn = st.form_submit_button("Send Mails")

        if submit_btn:
            recorded_by = f"{first_name} {last_name}"
            
            params=[master_df, email_df, recording_df, file, branch_names_mastersheet, recorded_by] 
            
            if email_type == "1st Email Chaser":
                params.insert(5, message_body)
                
            elif email_type == "2nd Email Chaser":
                params.insert(5, message_2)
                
            mass_mail(*params)

            with pd.ExcelWriter("updated.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay", date_format="DD-MM") as writer:
                master_df.to_excel(writer, sheet_name="Mastersheet", index=False)
                email_df.to_excel(writer, sheet_name="Branch with Emails", index=False)
                recording_df.to_excel(writer, sheet_name="Recording", startrow=0, index=False)
                
            st.download_button(label="Download updated excel sheet", data=f"updated.xlsx", file_name=f"{file.name.split(".")[0]}_updated.xlsx", mime="application/vnd.ms-excel")