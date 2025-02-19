import streamlit as st
import requests

headers = {
    "accept": "application/json",
    "Authorization": st.secrets['doubletick']['API_KEY']
}
url = f"{st.secrets['doubletick']['BASE_URL']}/media/upload"

def upload_media():
    st.header("Upload Media 🗃️")
    st.write("This platform is designed to help you upload media using the DoubleTick API.")

    media_file = st.file_uploader("Choose a media file", type=None)
    if st.button("Upload") and media_file:
        files = {"file": (media_file.name, media_file, media_file.type)}
        response = requests.post(url, headers=headers, files=files)
        response_data = response.json()

        if response.status_code == 200:
            st.success(f'Media Uploaded: {response_data["mediaUrl"]}', icon="✅")
            st.info(f"URL Expires In: {response_data['expiresIn']} seconds", icon="⏳")
        else:
            st.error(f'Error: {response_data["message"]}', icon="❌")

upload_media()
