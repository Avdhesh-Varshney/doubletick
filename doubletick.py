import streamlit as st
import random
import os

icons = ["🚀", "⚡", "⭐", "🔥", "🎉", "💥", "☀️", "☁️", "🎈", "💡", "⚙️", "🔔", "🌍", "🏆", "📝"]
sections_items = {
    "Outgoing Messages": "outgoing_messages", "Chat Messages": "chat_messages",
    "Broadcast Groups": "broadcast_groups", "Template": "template",
    "Customer": "customer", "Team Member": "team_member", "Wallet": "wallet",
    "Teams": "teams", "Roles": "roles", "Media": "media", "Webhook": "webhook"
}

if __name__ == "__main__":
    base = st.secrets['doubletick']['BASE_PATH']
    sections = {name: f"{base}/{path}" for name, path in sections_items.items()}
    all_pages = {"": [st.Page(page=f"{base}/home.py", title="Home", icon="🏠")]}
    all_pages.update({
        section: [st.Page(page=f"{path}/{f}", title=f.replace('.py', '').replace('_', ' ').title(), icon=random.choice(icons))
                  for f in os.listdir(path) if f.endswith('.py')]
        for section, path in sections.items()
    })
    st.navigation(all_pages).run()
