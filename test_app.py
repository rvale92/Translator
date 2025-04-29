import streamlit as st

st.title("🎙️ Voice Translation App - Test")

st.write("This is a test deployment to verify Streamlit Cloud setup.")

# Try to access the API key
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    st.success("✅ API key found in secrets!")
except Exception as e:
    st.error("❌ Could not find API key in secrets")
    st.write("Error:", str(e))

# Display some basic info
st.write("### Environment Information")
st.write("- Python version")
st.code(st.runtime.get_instance().python_version)
st.write("- Streamlit version")
st.code(st.__version__) 