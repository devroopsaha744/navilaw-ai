import streamlit as st
import requests


# Streamlit UI Enhancements

# Set page config (optional, for title and icon in the browser tab)
st.set_page_config(page_title="Law Navigator System", page_icon="⚖️")

# Sidebar for branding or navigation
st.sidebar.title("Law Navigator System")
st.sidebar.markdown("Your AI-powered legal research engine")

# Header and welcome section
st.title("⚖️ Law Navigator System")
st.markdown("#### *Your go-to AI-powered legal assistant!*")
st.write(
    "Upload your legal documents and ask any legal query. "
    "Our AI will assist you with legal advice, generate reports, or predict case outcomes."
)

# File uploader (multiple files)
st.markdown("### Upload your legal documents:")
uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

# Text input for user query
st.markdown("### Enter your legal query:")
query = st.text_area("Describe your legal issue or ask a question:")

# Dropdown for task selection
st.markdown("### What would you like assistance with?")
option = st.selectbox(
    "Select a task:",
    ["Legal Advisory", "Legal Report Generation", "Case Outcome Prediction"]
)

# Button to submit the query and files
if st.button("Submit"):
    if not uploaded_files or not query or not option:
        st.error("Please upload files, enter a query, and select an option.")
    else:
        # Create multipart form-data request payload
        files = [("files", (file.name, file, file.type)) for file in uploaded_files]
        data = {
            "query": query,
            "option": option
        }

        # Call the API (replace the URL with your API endpoint)
        api_url = "https://navilaw-ai.onrender.com/legal-assistance/"
        response = requests.post(api_url, files=files, data=data)

        # Check response and display result
        if response.status_code == 200:
            result = response.json()
            st.success("Response received successfully!")
            if "result" in result:
                st.markdown(f"### ⚖️ Legal Advice:\n{result['result']}")
            elif "report" in result:
                st.markdown(f"### 📄 Legal Report:\n{result['report']}")
            elif "prediction" in result:
                st.markdown(f"### 🔮 Case Outcome Prediction:\n{result['prediction']}")
        else:
            st.error(f"Error: {response.status_code}, {response.text}")

# Footer with branding and links
st.markdown("---")
st.markdown("##### Powered by [Law Navigator AI](https://law-navigator.example.com)")
st.markdown("🔗 Connect with us: [LinkedIn](https://www.linkedin.com/in/devroop-saha-datafreak/) | [GitHub](https://github.com/devroopsaha744/navilaw-ai)")
st.sidebar.markdown("---")
st.sidebar.info("Having trouble? Contact us at [devroopsaha844@gmail.com](mailto:devroopsaha844@gmail.com)")



