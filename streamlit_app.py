import streamlit as st
import requests

st.set_page_config(page_title="Doc Q&A", page_icon="📄")
st.title(" YOUR ASSISTANT- Document Q&A using Ollama + LLM")

backend_url = "http://localhost:8000"

model_options = ["llama3"]
selected_model = st.selectbox(" Choose a model", model_options, index=0)

uploaded_file = st.file_uploader(" Upload a PDF", type=["pdf"])
if uploaded_file:
    with st.spinner(" Uploading..."):
        try:
            response = requests.post(
                f"{backend_url}/upload/",
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            )
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(response.json().get("error", "Upload failed."))
        except requests.exceptions.RequestException as e:
            st.error(f" Upload failed: {e}")

    question = st.text_input(" Ask a question about the uploaded document:")
    if question:
        with st.spinner(" Getting answer..."):
            payload = {
                "question": question,
                "filename": uploaded_file.name,
                "model": selected_model
            }

            try:
                response = requests.post(f"{backend_url}/query/", json=payload, timeout=120)
                if response.status_code == 200:
                    st.text_area(" Answer", value=response.json()["answer"], height=200)
                else:
                    st.error(response.json().get("error", "Query failed."))
            except requests.exceptions.Timeout:
                st.error(" Timed out. Try a smaller model.")
            except requests.exceptions.RequestException as e:
                st.error(f" Request failed: {e}")
