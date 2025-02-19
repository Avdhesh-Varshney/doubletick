import streamlit as st
import random
import os

if os.path.dirname(__file__) == "":
    BASE_DIR = st.secrets['doubletick']['BASE_PATH']
else:
    BASE_DIR = f"{os.path.dirname(__file__)}/{st.secrets['doubletick']['BASE_PATH']}"

icons = ["🚀", "⚡", "⭐", "🔥", "🎉", "💥", "☀️", "☁️", "🎈", "💡", "⚙️", "🔔", "🌍", "🏆", "📝"]
sections_items = {
    "Outgoing Messages": "outgoing_messages", "Chat Messages": "chat_messages",
    "Broadcast Groups": "broadcast_groups", "Template": "template",
    "Wallet": "wallet", "Media": "media"
}

if __name__ == "__main__":
    sections = {name: f"{BASE_DIR}/{path}" for name, path in sections_items.items()}
    all_pages = {"": [st.Page(page=f"{BASE_DIR}/home.py", title="Home", icon="🏠")]}
    all_pages.update({
        section: [st.Page(page=f"{path}/{f}", title=f.replace('.py', '').replace('_', ' ').title(), icon=random.choice(icons))
                  for f in os.listdir(path) if f.endswith('.py')]
        for section, path in sections.items()
    })
    st.navigation(all_pages).run()
