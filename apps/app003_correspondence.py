import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_parquet("data/app003_correspondence.parquet")
    return df

def run():
    df = load_data()
    
    st.title("📬 Correspondence Lookup")
    tin_input = st.text_input("Enter one or more TINs (comma-separated)", max_chars=300)

    if tin_input:
        tin_list = [tin.strip() for tin in tin_input.split(",") if tin.strip()]
        results = df[df["TIN"].astype(str).isin(tin_list)]

        if results.empty:
            st.warning("No correspondence found for the given TIN(s).")
        else:
            for tin in tin_list:
                tin_results = results[results["TIN"].astype(str) == tin]
                if not tin_results.empty:
                    merchant_name = tin_results["Merchant Name"].iloc[0]
                    st.subheader(f"Merchant: {merchant_name} (TIN: {tin})")

                    sorted_df = tin_results.sort_values(by="Sent Date", ascending=False)
                    display_df = sorted_df[["Letter Title", "Sent Date", "Response Deadline"]].reset_index(drop=True)
                    display_df.index = range(1, len(display_df) + 1)
                    display_df.index.name = "#"
                    st.dataframe(display_df)
                else:
                    st.info(f"No correspondence found for TIN: {tin}")