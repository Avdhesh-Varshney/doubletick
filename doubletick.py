import streamlit as st
import random
import os

base = f"{os.path.dirname(__file__)}/doubletick"
st.write(os.path.dirname(__file__), base)

icons = ["🚀", "⚡", "⭐", "🔥", "🎉", "💥", "☀️", "☁️", "🎈", "💡", "⚙️", "🔔", "🌍", "🏆", "📝"]
sections_items = {
    "Outgoing Messages": "outgoing_messages", "Chat Messages": "chat_messages",
    "Broadcast Groups": "broadcast_groups", "Template": "template",
    "Wallet": "wallet", "Media": "media"
}

if __name__ == "__main__":
    sections = {name: f"{base}/{path}" for name, path in sections_items.items()}
    all_pages = {"": [st.Page(page=f"{base}/home.py", title="Home", icon="🏠")]}
    all_pages.update({
        section: [st.Page(page=f"{path}/{f}", title=f.replace('.py', '').replace('_', ' ').title(), icon=random.choice(icons))
                  for f in os.listdir(path) if f.endswith('.py')]
        for section, path in sections.items()
    })
    st.navigation(all_pages).run()
