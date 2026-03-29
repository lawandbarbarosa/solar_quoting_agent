import streamlit as st
import requests

# --- CONFIG ---
API_URL = "https://mr2nxcuqfs.us-east-1.awsapprunner.com/generate_quote"

st.set_page_config(
    page_title="SimkoSolar Quote Generator",
    page_icon="☀️",
    layout="centered"
)

# --- HEADER ---
st.title("☀️ SimkoSolar Quote Generator")
st.markdown("Get a personalized solar quote in seconds.")

# --- SIDEBAR ---
st.sidebar.header("About")
st.sidebar.info(
    "This tool generates solar estimates using AI.\n\n"
    "Fill in the details and click *Generate Quote*."
)

# --- FORM ---
with st.form("quote_form"):
    st.subheader("📋 Customer Details")

    location = st.text_input("📍 Location", "10001 (New York)")
    monthly_bill = st.number_input("💵 Monthly Bill ($)", min_value=0, value=180)

    # Note: returns a list. If your API needs a string, change this to selectbox
    roof_type = st.multiselect(
        "🏠 Roof Type",
        ["flat", "shingle", "tile", "metal"],
        default=["flat"]
    )

    shading = st.selectbox(
        "🌳 Shading",
        ["no shading", "partial shading", "heavy shading"]
    )

    battery = st.selectbox(
        "🔋 Battery Interest",
        ["yes", "no"]
    )

    goal = st.text_input(
        "🎯 Primary Goal",
        "Lower electricity bills"
    )

    submitted = st.form_submit_button("🚀 Generate Quote")

# --- PROCESS ---
if submitted:
    if not location or not roof_type:
        st.warning("Please fill all required fields.")
    else:
        payload = {
            "Location": location,
            "monthly_bill": monthly_bill,
            "roof_type": roof_type, 
            "shading": shading,
            "battery_intrest": battery, # Verify spelling matches backend
            "Primary_goal": goal
        }

        with st.spinner("⚡ Generating your solar quote..."):
            try:
                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Quote Generated!")

                    tabs = st.tabs(["✅ Final Quote"])
                    with tabs[0]:
                        final_quote = data.get("refine_node", "No data returned.")
                        escaped_quote = final_quote.replace("$", r"\$").replace("\n", "\n\n")
                        st.markdown(escaped_quote)

                else:
                    st.error(f"❌ API Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"🚫 Connection Error: {e}")