import streamlit as st
import pandas as pd
from classify_emails import classify_emails

st.set_page_config(page_title="CEO Email Classifier", layout="wide")

st.title("Email Classification Dashboard")

n_emails = st.slider("Number of latest emails to fetch", 1, 20, 5)

if st.button("Fetch & Classify Emails"):
    results = classify_emails(n=n_emails)
    
    concerning = [r for r in results if r["concern"] == "Y"]
    not_concerning = [r for r in results if r["concern"] == "N"]
    
    tab1, tab2 = st.tabs(["⚠️ Concerning Mails", "✅ Not Concerning Mails"])
    
    with tab1:
        if concerning:
            df_con = pd.DataFrame(concerning)
            st.dataframe(df_con[["urgency_level", "category", "from", "subject"]])
        else:
            st.info("No concerning emails found.")
    
    with tab2:
        if not_concerning:
            df_not_con = pd.DataFrame(not_concerning)
            st.dataframe(df_not_con[["urgency_level", "category", "from", "subject"]])
        else:
            st.info("No non-concerning emails found.")
