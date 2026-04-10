import requests
import streamlit as st

BASE_URL = "http://localhost:8000"


def get(endpoint, params=None):
    try:
        res = requests.get(f"{BASE_URL}{endpoint}", params=params)
        return res.json() if res.status_code == 200 else []
    except:
        return []


def post(endpoint, body):
    try:
        return requests.post(f"{BASE_URL}{endpoint}", json=body)
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None


def put(endpoint, body, params=None):
    try:
        return requests.put(f"{BASE_URL}{endpoint}", json=body, params=params)
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None


def delete(endpoint, params=None):
    try:
        return requests.delete(f"{BASE_URL}{endpoint}", params=params)
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None