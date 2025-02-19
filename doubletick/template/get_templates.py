import streamlit as st
import requests

headers = {
    "accept": "application/json",
    "Authorization": st.secrets['doubletick']['API_KEY']
}
url = f"{st.secrets['doubletick']['BASE_URL']}/v2/templates"

def template_card(template):
    return f"""
        <div style="background-color:#12151e; padding:16px 32px; border-radius:16px; margin:15px 0;">
            <h5>📄 {template.get('name', 'N/A')}</h5>
            <p><strong>Created By:</strong> {template.get('createdBy', 'N/A')}</p>
            <p><strong>WABA Phone Number:</strong> {template.get('wabaPhoneNumber', 'N/A')}</p>
            <p><strong>Body:</strong> {template.get('components', [{}])[0].get('text', 'N/A')}</p>
        </div>
    """

def get_templates():
    st.header("Get Templates 📝")
    st.write("This platform is designed to help you get templates using the DoubleTick API.")

    col1, col2, col3 = st.columns(3)
    with col1:
        status = st.selectbox("📊 Status", options=["APPROVED", "REJECTED", "PENDING", "PAUSED"], help="Select the template status.")
        name = st.text_input("📝 Template Name", placeholder="Enter template name")

    with col2:
        language = st.selectbox("🌐 Template Language", options=['af', 'sq', 'ar', 'az', 'bn', 'bg', 'ca', 'zh_CN', 'zh_HK', 'zh_TW', 'hr', 'cs', 'da', 'nl', 'en', 'en_GB', 'en_US', 'et', 'fil', 'fi', 'fr', 'ka', 'de', 'el', 'gu', 'ha', 'he', 'hi', 'hu', 'id', 'ga', 'it', 'ja', 'kn', 'kk', 'rw_RW', 'ko', 'ky_KG', 'lo', 'lv', 'lt', 'mk', 'ms', 'ml', 'mr', 'nb', 'fa', 'pl', 'pt_BR', 'pt_PT', 'pa', 'ro', 'ru', 'sr', 'sk', 'sl', 'es', 'es_AR', 'es_ES', 'es_MX', 'sw', 'sv', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'uz'], help="Select the template language.")
        category = st.selectbox("🏷️ Template Category", options=["MARKETING", "UTILITY"], help="Choose the template category.")

    with col3:
        waba_phone_numbers = st.text_input("📞 WABA Phone Numbers", placeholder="Enter comma-separated numbers")
        all_waba_phone_numbers = st.checkbox("🔄 All WABA Phone Numbers", value=False, help="Check to fetch templates for all waba phone numbers.")

    if st.button("Get Templates", key="get_templates"):
        params = {
            "status": status,
            "name": name,
            "language": language,
            "category": category,
            "wabaPhoneNumbers": waba_phone_numbers,
            "allWabaPhoneNumbers": all_waba_phone_numbers
        }
        params = {k: v for k, v in params.items() if v}
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        if response.status_code == 200:
            st.success(f"{len(response_data)} Templates Fetched Successfully!", icon="✅")
            cols = st.columns(2)
            for i, template in enumerate(response_data):
                with cols[i % 2]:
                    st.markdown(template_card(template), unsafe_allow_html=True)
        else:
            st.error(f'Error: {response_data["message"]}', icon="❌")

get_templates()
