import streamlit as st
import requests

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": st.secrets['doubletick']['API_KEY']
}
url = f"{st.secrets['doubletick']['BASE_URL']}/wallet/balance"

def get_wallet_balance():
    st.header("Get Wallet Balance!")
    st.write("This platform is designed to help you get the wallet balance using the DoubleTick API.")

    if st.button("Get Balance"):
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            st.success(f'Wallet Balance: {response_data["currencyCode"]} {response_data["balance"]}', icon="✅")
        else:
            st.error(f'Error: {response_data["message"]}', icon="❌")

get_wallet_balance()
