import streamlit as st
import requests

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": st.secrets['doubletick']['API_KEY']
}
url = f"{st.secrets['doubletick']['BASE_URL']}/whatsapp/message/text"

def send_whatsapp_text_message():
    st.header("Send WhatsApp Text Message!")
    st.write("This platform is designed to help you send a WhatsApp text message using the DoubleTick API.")

    sender_phone = st.number_input("Sender Phone Number with Country Code", min_value=1000000000, max_value=999999999999999)
    customer_phone = st.number_input("Customer Phone Number with Country Code", min_value=1000000000, max_value=999999999999999)
    message = st.text_area("Text Message")

    if st.button("Send Message"):
        if customer_phone and message:
            payload = {
                "from": f"{sender_phone}",
                "to": customer_phone,
                "content": { "text": message }
            }
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                st.toast("Message sent successfully!", icon="🚀")
                st.success(f'Message sent to {response_data["recipient"]}', icon="✅")
            else:
                st.toast("Failed to send message. Please try again.", icon="🚨")
                st.error(f'Error: {response_data["message"]}', icon="❌")
        else:
            st.warning("Please fill all the fields to send a message.", icon="⚠️")

send_whatsapp_text_message()
