import streamlit as st
import pandas as pd
from io import BytesIO

def run():
    st.title("Tax ID Lookup - Recovery & Interchange Summary")

    @st.cache_data
    def load_data():
        return pd.read_parquet("data/app002_franchisee_tax_id.parquet")

    df = load_data()

    tax_id_input = st.text_input("Enter one or more Tax IDs (comma-separated):")

    if tax_id_input:
        tax_ids = [tid.strip() for tid in tax_id_input.split(",") if tid.strip()]
        filtered = df[df["Tax ID"].isin(tax_ids)]

        if not filtered.empty:
            st.subheader("Matching Tax IDs")

            # Prepare display dataframe
            display_df = filtered[["Tax ID", "Initial Open Date", "Recovery", "Total Interchange"]].copy()
            display_df["Total Interchange"] = display_df["Total Interchange"].map(lambda x: f"{x:.8f}")
            display_df = display_df.reset_index(drop=True)
            display_df.index += 1
            display_df.index.name = "#"

            st.dataframe(display_df, use_container_width=True)

            # Show totals
            total_recovery = filtered["Recovery"].sum()
            total_interchange = filtered["Total Interchange"].sum()

            st.markdown(f"**Total Recovery:** ${total_recovery:,.2f}")
            st.markdown(f"**Total Interchange:** {total_interchange:.8f}")

            # Download
            def to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Matches")
                return output.getvalue()

            excel_data = to_excel(filtered)
            st.download_button(
                "📥 Download as Excel",
                data=excel_data,
                file_name="tax_id_lookup.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:
            st.warning("No matching Tax IDs found.")