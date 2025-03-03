import streamlit as st
import requests

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": st.secrets['doubletick']['API_KEY']
}
url = f"{st.secrets['doubletick']['BASE_URL']}/whatsapp/message/text"
template_url = f"{st.secrets['doubletick']['BASE_URL']}/v2/templates?status=ALL"

@st.cache_data
def fetch_templates():
    response = requests.get(template_url, headers=headers)
    response_data = response.json()
    template_names = [template.get('name') for template in response_data]
    return template_names

def send_whatsapp_template_message():
    st.title("Send WhatsApp Template Message")
    st.write("Use this form to send a WhatsApp template message to a user.")

    col1, col2 = st.columns(2)
    with col1:
        sender_number = st.number_input("Sender Number", min_value=1000000000, max_value=999999999999999)
        template_name = st.selectbox("Select Template", options=fetch_templates())
    with col2:
        customer_number = st.number_input("Customer Number", min_value=1000000000, max_value=999999999999999)
        template_language = st.selectbox("Select Template Language", options=["en", "en_US", "en_GB", "pt_BR", "es", "id"])

    with st.checkbox("Add Customize Template Data", key="customize_template_data"):
        # optional template data object
        col3, col4 = st.columns(2)
        with col3:
            ## header
            header_type = st.selectbox("Header Type", options=["TEXT", "IMAGE", "DOCUMENT", "VIDEO", "LOCATION"])
            if header_type == 'TEXT':
                header_placeholder = st.text_input("Header Text", help="Enter the header text.")
                header_content = {"type": header_type, "text": header_placeholder}
            elif header_type == 'IMAGE':
                header_mediaUrl = st.text_input("Enter the header image URL")
                header_caption = st.text_input("Enter the image caption")
                header_content = {"type": header_type, "mediaUrl": header_mediaUrl, "filename": header_caption}
            elif header_type == 'DOCUMENT':
                header_mediaUrl = st.text_input("Enter the header document URL")
                header_filename = st.text_input("Enter the document filename")
                header_content = {"type": header_type, "mediaUrl": header_mediaUrl, "filename": header_filename}
            elif header_type == 'VIDEO':
                header_mediaUrl = st.text_input("Enter the header video URL")
                header_caption = st.text_input("Enter the video caption.")
                header_content = {"type": header_type, "mediaUrl": header_mediaUrl, "filename": header_caption}
            elif header_type == 'LOCATION':
                header_latitude = st.number_input("Latitude", help="Enter the location latitude.")
                header_longitude = st.number_input("Longitude", help="Enter the location longitude.")
                header_content = {"type": header_type, "latitude": header_latitude, "longitude": header_longitude}

        with col4:
            ## body
            body_placeholders = st.number_input("Enter the number of body texts", min_value=1, max_value=10)
            placeholders_list = []
            for i in range(body_placeholders):
                body_text = st.text_input(f"Body Text {i+1}", help="Enter the body text.")
                placeholders_list.append(body_text)
            body_content = { "placeholders": placeholders_list }

        ## buttons
        button_url = st.text_input("Button URL", help="Enter the button URL.")
        button_content = [ { "type": "URL", "parameter": button_url } ]

        template_data = {
            "header": header_content,
            "body": body_content,
            "buttons": button_content
        }

    if st.button("Send Template Message", key="send_whatsapp_template_message") and sender_number and customer_number and template_name and template_language:
        if template_data:
            payload = { "messages": [
                {
                    "to": sender_number,
                    "from": customer_number,
                    "content": {
                        "templateName": template_name,
                        "language": template_language,
                        "templateData": {
                            "header": header_content,
                            "body": body_content,
                            "buttons": button_content
                        }
                    }
                }]
            }
        else:
            payload = { "messages": [
                {
                    "to": sender_number,
                    "from": customer_number,
                    "content": {
                        "templateName": template_name,
                        "language": template_language
                    }
                }]
            }
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            st.success(f"Template Message Sent Successfully!", icon="✅")
            st.write(response_data)
        else:
            st.error(f'Error: {response_data["message"]}', icon="❌")

send_whatsapp_template_message()
