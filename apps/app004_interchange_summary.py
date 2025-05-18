import streamlit as st
import pandas as pd
from io import BytesIO

def run():
    st.title("🧾 Interchange Fee Summary")

    @st.cache_data
    def load_data():
        df = pd.read_parquet("data/app004_interchange_summary.parquet")
        return df.drop(columns=["IngestedFrom"], errors="ignore")

    df = load_data()

    st.markdown("Enter one or more **IDs** (comma-separated):")
    id_input = st.text_input("Search by ID(s):", max_chars=300)

    if id_input:
        id_list = [i.strip() for i in id_input.split(",") if i.strip()]
        filtered = df[df["id"].isin(id_list)]

        if filtered.empty:
            st.warning("No matching records found.")
        else:
            for id_value in id_list:
                subset = filtered[filtered["id"] == id_value].copy()
                if subset.empty:
                    st.info(f"No rows for ID {id_value}")
                    continue

                merchant = subset["TransactionMerchantName"].iloc[0] if "TransactionMerchantName" in subset.columns else "Unknown"
                st.subheader(f"🧾 ID: {id_value}  |  Merchant: {merchant}")

                # Preserve original column order
                desired_order = [
                    "id", "Year", "CardAcceptorId", "AcquirerBIN",
                    "TransactionMerchantName", "City", "State", "ZipCode",
                    "TransactionTotal", "SalesVolumeTotal", "TotalInterchangeFees"
                ]
                cols = [col for col in desired_order if col in subset.columns] + \
                       [col for col in subset.columns if col not in desired_order]
                display_df = subset[cols]

                st.dataframe(display_df, use_container_width=True)

                # Convert to numeric for totals
                for col in ["TransactionTotal", "SalesVolumeTotal", "TotalInterchangeFees"]:
                    if col in subset.columns:
                        subset[col] = pd.to_numeric(subset[col], errors="coerce")

                totals = subset[["TransactionTotal", "SalesVolumeTotal", "TotalInterchangeFees"]].sum()

                st.markdown("### 📊 Totals")
                st.markdown(f"- Sum of **TransactionTotal**: {int(totals['TransactionTotal']):,}")
                st.markdown(f"- Sum of **SalesVolumeTotal**: ${totals['SalesVolumeTotal']:,.2f}")
                st.markdown(f"- Sum of **TotalInterchangeFees**: ${totals['TotalInterchangeFees']:,.2f}")

                # 📥 Download Excel
                def to_excel(df):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df.to_excel(writer, index=False, sheet_name="Interchange")
                    return output.getvalue()

                excel_data = to_excel(display_df)
                st.download_button(
                    label="📥 Download Results as Excel",
                    data=excel_data,
                    file_name=f"interchange_summary_{id_value}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

if __name__ == "__main__":
    run()