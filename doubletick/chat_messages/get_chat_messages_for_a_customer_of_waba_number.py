import streamlit as st
import requests
from datetime import datetime, timedelta

headers = {
    "accept": "application/json",
    "Authorization": st.secrets['doubletick']['API_KEY']
}
url = f"{st.secrets['doubletick']['BASE_URL']}/chat-messages"

def format_count(label, count, emoji):
    return f"{emoji} {label}: {count}"

def create_chat_card(chat):
    sender = chat.get("senderId", "-").split('(')[0]
    message_text = chat.get("message", {}).get("text", "No message")
    message_type = chat.get("message", {}).get("messageType", "N/A").capitalize()
    origin = chat.get("messageOriginType", "-").capitalize()
    timestamp = chat.get("messageMetadata", {}).get("status") or "N/A"

    stats = [
        format_count("Sent", chat.get("sentCount", 0), "📤"),
        format_count("Read", chat.get("readCount", 0), "✅"),
        format_count("Delivered", chat.get("deliveryCount", 0), "📬"),
        format_count("Errored", chat.get("erroredCount", 0), "❌"),
        format_count("Replies", chat.get("repliesCount", 0), "💬"),
    ]
    bg_color = {
        "USER": "#37474F",
        "SYSTEM": "#4A148C",
        "BOT": "#2E7D32"
    }.get(origin.upper(), "#424242")

    return f"""
    <div style="border-radius: 16px; padding: 16px; margin: 16px 0; background-color: #12151e;">
        <p><strong>👤 Sender:</strong> {sender}</p>
        <p><strong>📩 Message Type:</strong> {message_type} | <strong>🌍 Origin:</strong> {origin}</p>
        <p><strong>🕒 Timestamp:</strong> {timestamp}</p>
        <div style="border-radius: 10px; padding: 10px; background-color: {bg_color}; margin: 10px 0;">
            🗨️ <em>{message_text}</em>
        </div>
        {" | ".join(stats)}
    </div>
    """

def get_chat_messages_for_a_customer_of_waba_number():
    st.header("Get Chat Messages for a Customer of WABA Number 📨")
    st.write("This platform is designed to help you get chat messages for a customer of a WABA number using the DoubleTick API.")

    waba_number = st.number_input("Enter WABA Number with Country Code", min_value=1000000000, max_value=999999999999999)
    customer_number = st.number_input("Enter Customer Number", min_value=1000000000, max_value=999999999999999)
    if st.checkbox("Use Start and End Date"):
        start_date = st.date_input("Start Date", value=datetime.now().date()-timedelta(days=2))
        end_date = st.date_input("End Date")
        start_date_str = start_date.strftime("%d-%m-%Y")
        end_date_str = end_date.strftime("%d-%m-%Y")
        params = {"wabaNumber": waba_number, "customerNumber": customer_number, "startDate": start_date_str, "endDate": end_date_str}
    else:
        params = {"wabaNumber": waba_number, "customerNumber": customer_number}

    if st.button("Get Chat Messages") and waba_number and customer_number:
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        if response.status_code == 200:
            chats = response_data.get("messages", [])
            st.success(f"Total Chats: {len(chats)}", icon="✅")
            for i in range(0, len(chats), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(chats):
                        cols[j].markdown(create_chat_card(chats[i + j]), unsafe_allow_html=True)
        else:
            st.error(f'Error: {response_data["message"]}', icon="❌")

get_chat_messages_for_a_customer_of_waba_number()
