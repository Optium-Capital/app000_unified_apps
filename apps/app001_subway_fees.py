import streamlit as st
import pandas as pd
import io

def run():
    # ✅ Load the data and cache it
    @st.cache_data
    def load_data():
        return pd.read_csv('data/app001_subway_fees.csv', dtype={'entity_id': str})

    # ✅ Report generator function (wildcard-compatible)
    def generate_report(df, entity_patterns):
        pattern = '|'.join(p.strip('%') for p in entity_patterns)
        df_filtered = df[df['entity_id'].astype(str).str.contains(pattern, na=False)]

        summary = df_filtered.groupby('entity_id')[
            ['visa fees', 'mastercard fees', 'visa sales', 'mastercard sales']
        ].sum()

        total = summary.sum().to_frame().T
        total.index = ['TOTAL']

        return pd.concat([summary, total]), df_filtered

    # ✅ Load dataset
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("⚠️ Data file not found at 'data/app001_subway_fees.csv'.")
        st.stop()

    # ✅ Title
    st.title("Franchisee Financial Report 2005–2019")

    # ✅ Setup session state
    if 'entity_input' not in st.session_state:
        st.session_state.entity_input = ""
    if 'report' not in st.session_state:
        st.session_state.report = None
    if 'monthly_report' not in st.session_state:
        st.session_state.monthly_report = None

    # 🔍 Search form
    def handle_search():
        input_text = st.session_state.entity_input
        patterns = [e.strip() for e in input_text.split(",") if e.strip()]
        report, filtered = generate_report(df, patterns)
        st.session_state.report = report
        st.session_state.monthly_report = filtered

    with st.form("search_form", clear_on_submit=False):
        st.text_input(
            "Enter ENTITY_IDs separated by commas (wildcards like %12345% allowed):",
            key="entity_input"
        )
        submitted = st.form_submit_button("Search", on_click=handle_search)

    # 📊 Show summary report
    if st.session_state.report is not None:
        st.dataframe(st.session_state.report)

        # 📥 Download main report
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            st.session_state.report.to_excel(writer, index=True, sheet_name='Summary')
        st.download_button(
            label="📄 Download Report (Excel)",
            data=buffer.getvalue(),
            file_name="financial_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # 📆 Monthly breakdown
        if 'month' in df.columns:
            show_monthly = st.checkbox("📊 Show month-by-month breakdown", key="show_months")
            if show_monthly and st.session_state.monthly_report is not None:
                monthly = st.session_state.monthly_report.groupby(['entity_id', 'month'])[
                    ['visa fees', 'mastercard fees', 'visa sales', 'mastercard sales']
                ].sum().reset_index()

                st.subheader("Monthly Breakdown")
                st.dataframe(monthly)

                if not monthly.empty:
                    monthly_buffer = io.BytesIO()
                    with pd.ExcelWriter(monthly_buffer, engine='xlsxwriter') as writer:
                        monthly.to_excel(writer, index=False, sheet_name='Monthly Breakdown')
                    st.download_button(
                        label="📄 Download Monthly Breakdown (Excel)",
                        data=monthly_buffer.getvalue(),
                        file_name="monthly_breakdown.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

    # 📦 Final caption
    st.caption(f"{len(df):,} rows loaded from combined dataset.")