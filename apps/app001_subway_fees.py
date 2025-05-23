import streamlit as st
import pandas as pd
import io


def run():
    st.title("Franchisee Financial Report 2005–2019")

    tab1, tab2 = st.tabs(["Normal Search", "Partial Search"])

    @st.cache_data
    def load_data():
        return pd.read_csv('data/app001_subway_fees.csv', dtype={'entity_id': str})

    def generate_report(df, entity_ids):
        df_filtered = df[df['entity_id'].astype(str).str.contains('|'.join(entity_ids))]

        summary = df_filtered.groupby('entity_id')[
            ['visa fees', 'mastercard fees', 'visa sales', 'mastercard sales']
        ].sum()

        total = summary.sum().to_frame().T
        total.index = ['TOTAL']

        return pd.concat([summary, total]), df_filtered

    try:
        df = load_data()
    except FileNotFoundError:
        st.error("⚠️ Data file not found at 'data/app001_subway_fees.csv'.")
        st.stop()

    with tab1:
        st.markdown("<h5>Advanced comma-separated search (wildcards allowed)</h5>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:16px'>Use wildcards like <code>%255000000190397%</code> for partial matches. Example:</p>", unsafe_allow_html=True)
        st.code("%255000000190397%,000255000003134640,000255000000011809")

        with st.form("search_form_normal"):
            entity_input = st.text_input("Enter ENTITY_IDs separated by commas:")
            submitted = st.form_submit_button("Search")

        if submitted:
            patterns = [e.strip().replace('%', '') for e in entity_input.split(',') if e.strip()]
            report, filtered = generate_report(df, patterns)

            st.subheader("Summary")
            st.dataframe(report, use_container_width=True)

            total_buffer = io.BytesIO()
            with pd.ExcelWriter(total_buffer, engine='xlsxwriter') as writer:
                report.to_excel(writer, index=True, sheet_name='Summary')
            st.download_button("📄 Download Report (Excel)", total_buffer.getvalue(), "financial_report.xlsx")

            if 'month' in df.columns:
                show_monthly = st.checkbox("📊 Show month-by-month breakdown", key="normal_monthly")
                if show_monthly:
                    monthly = filtered.groupby(['entity_id', 'month'])[
                        ['visa fees', 'mastercard fees', 'visa sales', 'mastercard sales']
                    ].sum().reset_index()

                    st.subheader("Monthly Breakdown")
                    st.dataframe(monthly)

                    monthly_buffer = io.BytesIO()
                    with pd.ExcelWriter(monthly_buffer, engine='xlsxwriter') as writer:
                        monthly.to_excel(writer, index=False, sheet_name='Monthly Breakdown')
                    st.download_button("📄 Download Monthly Breakdown (Excel)", monthly_buffer.getvalue(), "monthly_breakdown.xlsx")

    with tab2:
        st.markdown("<h5>Single partial search</h5>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:16px'>Enter any part of the ENTITY_ID (e.g. <code>190397</code>) to find matches.</p>", unsafe_allow_html=True)

        partial_input = st.text_input("Enter part of an ENTITY_ID:", key="partial_input")
        if partial_input:
            df_partial = df[df['entity_id'].astype(str).str.contains(partial_input)]

            if not df_partial.empty:
                st.subheader("Summary")
                summary = df_partial.groupby('entity_id')[
                    ['visa fees', 'mastercard fees', 'visa sales', 'mastercard sales']
                ].sum()
                total = summary.sum().to_frame().T
                total.index = ['TOTAL']

                st.dataframe(pd.concat([summary, total]), use_container_width=True)

                if 'month' in df.columns:
                    show_monthly_partial = st.checkbox("📊 Show month-by-month breakdown", key="partial_monthly")
                    if show_monthly_partial:
                        monthly = df_partial.groupby(['entity_id', 'month'])[
                            ['visa fees', 'mastercard fees', 'visa sales', 'mastercard sales']
                        ].sum().reset_index()

                        st.subheader("Monthly Breakdown")
                        st.dataframe(monthly)

    st.caption(f"{len(df):,} rows loaded from combined dataset.")


if __name__ == "__main__":
    run()
