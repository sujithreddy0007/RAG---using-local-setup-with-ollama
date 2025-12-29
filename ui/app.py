import streamlit as st
import requests
import time

import os
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")


st.set_page_config(page_title="Session-Based RAG App", layout="centered")
st.title("📄 Session-Based RAG Application")

# --------------------------------------------------
# BACKEND HEALTH CHECK
# --------------------------------------------------
def wait_for_backend(retries=10, delay=1):
    for _ in range(retries):
        try:
            r = requests.get(f"{FASTAPI_URL}/docs", timeout=2)
            if r.status_code == 200:
                return True
        except:
            time.sleep(delay)
    return False


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# SESSION CREATION
# --------------------------------------------------
st.header("🔑 Session")

if st.button("Create New Session"):
    with st.spinner("Connecting to backend..."):
        if not wait_for_backend():
            st.error("Backend is not ready yet. Please wait a few seconds and try again.")
        else:
            try:
                res = requests.post(
                    f"{FASTAPI_URL}/session/create",
                    timeout=5
                )
                if res.status_code == 200:
                    st.session_state.session_id = res.json()["session_id"]
                    st.session_state.chat_history = []  # reset chat on new session
                    st.success(f"Session created: {st.session_state.session_id}")
                else:
                    st.error("Failed to create session")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")

if st.session_state.session_id:
    st.info(f"Current Session ID: {st.session_state.session_id}")


# --------------------------------------------------
# DOCUMENT INGESTION
# --------------------------------------------------
st.header("📤 Upload Document")

uploaded_file = st.file_uploader("Upload a .txt or .pdf file")

if uploaded_file and st.session_state.session_id:
    if st.button("Ingest Document"):
        with st.spinner("Ingesting document..."):
            try:
                files = {
                    "file": (uploaded_file.name, uploaded_file.getvalue())
                }
                params = {
                    "session_id": st.session_state.session_id
                }
                res = requests.post(
                    f"{FASTAPI_URL}/ingest",
                    params=params,
                    files=files,
                    timeout=30
                )

                if res.status_code == 200:
                    st.success("Document ingested successfully.")
                else:
                    st.error("Document ingestion failed")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")


# --------------------------------------------------
# CHAT SECTION (WITH HISTORY)
# --------------------------------------------------
st.header("💬 Chat")

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask a question")

if user_input and st.session_state.session_id:
    # Store user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "session_id": st.session_state.session_id,
                    "question": user_input
                }
                res = requests.post(
                    f"{FASTAPI_URL}/chat",
                    json=payload,
                    timeout=60
                )

                if res.status_code == 200:
                    answer = res.json()["answer"]
                else:
                    answer = "Failed to get answer from backend."

            except requests.exceptions.RequestException as e:
                answer = f"Connection error: {e}"

            st.markdown(answer)

    # Store assistant response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })
