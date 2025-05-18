import streamlit as st
from apps import app001_subway_fees, app002_subway_tax_id, app003_correspondence, app004_interchange_summary

# Sidebar app selector
st.sidebar.title("🧭 Navigation")
app_choice = st.sidebar.radio("Select App", [
    "💡 Choose an App",
    "001 Subway Fees",
    "002 Subway Tax Id",
    "003 Correspondence Lookup",
    "004 Interchange Summary"
])

# ⛔ Detect app switch and clear cache
if "last_app_choice" not in st.session_state:
    st.session_state.last_app_choice = app_choice
elif st.session_state.last_app_choice != app_choice:
    st.cache_data.clear()  # 🔥 Clear cached datasets
    st.session_state.last_app_choice = app_choice

# ✅ Route to selected app
if app_choice == "001 Subway Fees":
    app001_subway_fees.run()
elif app_choice == "002 Subway Tax Id":
    app002_subway_tax_id.run()
elif app_choice == "003 Correspondence Lookup":
    app003_correspondence.run()
elif app_choice == "004 Interchange Summary":
    app004_interchange_summary.run()
else:
    st.title("👋 Welcome")
    st.markdown("Use the menu on the left to select an app.")