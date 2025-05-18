import streamlit as st
from apps import app001_subway_fees, app002_subway_tax_id, app003_correspondence, app004_interchange_summary

# Sidebar app selector
st.sidebar.title("🧭 Navigation")
app_choice = st.sidebar.radio("Select App", [
    "💡 Choose an App",
    "001 Search By Entity ID",
    "002 Search By Tax ID",
    "003 Correspondence by Tax ID",
    "004 Subway Research Request Responses"
])

# ⛔ Detect app switch and clear cache
if "last_app_choice" not in st.session_state:
    st.session_state.last_app_choice = app_choice
elif st.session_state.last_app_choice != app_choice:
    st.cache_data.clear()  # 🔥 Clear cached datasets
    st.session_state.last_app_choice = app_choice

# ✅ Route to selected app
if app_choice == "001 Search By Entity ID":
    app001_subway_fees.run()
elif app_choice == "002 Search By Tax ID":
    app002_subway_tax_id.run()
elif app_choice == "003 Correspondence by Tax ID":
    app003_correspondence.run()
elif app_choice == "004 Subway Research Request Responses":
    app004_interchange_summary.run()
else:
    st.title("👋 Welcome")
    st.markdown("Use the menu on the left to select an app.")