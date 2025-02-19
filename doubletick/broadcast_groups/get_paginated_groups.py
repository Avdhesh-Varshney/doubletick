from datetime import datetime, time
from dateutil import parser
import streamlit as st
import requests

headers = {
    "accept": "application/json",
    "Authorization": st.secrets['doubletick']['API_KEY']
}
url = f"{st.secrets['doubletick']['BASE_URL']}/groups"

def create_card(group):
    return f"""
        <div style="border: 1px solid #e1e1e1; border-radius: 10px; padding: 16px 32px; margin: 16px 0; position: relative;">
            <h4>📢 {group.get("groupChatName", "-")}</h4>
            <p><strong>Group ID:</strong> {group.get("groupId", "-")}</p>
            <p><strong>Members:</strong> {group.get("memberCount", 0)}</p>
            <p><strong>Type:</strong> {group.get("groupType", "-")}</p>
            <p><strong>Created At:</strong> {datetime.fromtimestamp(group.get("dateCreated") / 1000).strftime('%Y-%m-%d %H:%M:%S') if group.get("dateCreated") else "-"}</p>
            <p><strong>Last Message:</strong> {parser.parse(group.get("lastMessageAt")).strftime('%Y-%m-%d %H:%M:%S') if group.get("lastMessageAt") else "-"}</p>
            <p><strong>Internal:</strong> {"✅" if group.get("isInternal") else "❌"}</p>
        </div>
    """

def get_paginated_groups():
    st.header("Get Broadcast Groups 📄")
    st.write("This platform is designed to help you get paginated broadcast groups using the DoubleTick API.")

    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("🔍 Search Query", placeholder="Enter group name or keyword")
        after_group_id = st.text_input("🔢 After Group ID", placeholder="Enter group ID")
        after_group_name = st.text_input("🏷️ After Group Name", placeholder="Enter group name")
    
    with col2:
        order_by = st.selectbox("📑 Order By", options=["NAME", "DATE_CREATED"])
        format_option = st.selectbox("📐 Order Format", options=["ASCENDING", "DESCENDING"])

    with col3:
        after_date = st.date_input("📅 After Date Created", format="YYYY-MM-DD")
        after_time = st.time_input("⏰ After Time Created", value=time(0, 0))
        after_date_created = f"{after_date}T{after_time.strftime('%H:%M:%S')}.000Z" if after_date else None

    if st.button("Get Groups"):
        params = {
            "searchQuery": search_query,
            "orderBy": order_by,
            "format": format_option,
            "afterGroupId": after_group_id,
            "afterGroupName": after_group_name,
            "afterDateCreated": after_date_created
        }
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        if response.status_code == 200:
            groups = response_data["groups"]
            st.toast(f"{len(groups)} Groups Fetched Successfully!", icon="✅")
            for i in range(0, len(groups), 2):
                cols = st.columns(2)
                for col, group in zip(cols, groups[i:i+2]):
                    with col:
                        card_html = create_card(group)
                        col.markdown(card_html, unsafe_allow_html=True)
            if response_data['paginationParams']['hasMore']:
                with st.expander("Loading More Groups..."):
                    st.info(f"Use this `afterGroupId` to load more groups: {response_data['paginationParams']['afterGroupId']}", icon="🔜")
                    st.info(f"Use this `afterGroupName` to load more groups: {response_data['paginationParams']['afterGroupName']}", icon="🔜")
        else:
            st.error(f'Error: {response_data["message"]}', icon="❌")

get_paginated_groups()
