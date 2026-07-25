import os
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. PAGE SETUP & GLASSMORPHISM CSS
# ==========================================
st.set_page_config(
    page_title="Orion AI Assistant",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0rem !important; max-width: 100% !important; }

/* Translucent floating chat messages */
[data-testid="stChatMessage"] {
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 240, 255, 0.2) !important;
    border-radius: 12px !important;
    margin-bottom: 12px !important;
    color: #e2e8f0 !important;
    padding: 12px 18px !important;
}

/* Glassmorphic input bar fixed at the bottom */
.stChatInputContainer {
    position: fixed !important;
    bottom: 25px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 65% !important;
    max-width: 800px !important;
    z-index: 1000 !important;
    background-color: rgba(15, 23, 42, 0.85) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(0, 240, 255, 0.4) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8) !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. YOUR ORIGINAL THREE.JS ENGINE
# ==========================================
# Paste your exact HTML / Three.js / GLSL Shader code here inside triple quotes
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <!-- YOUR ORIGINAL FULL HTML & THREE.JS HEAD & SHADERS HERE -->
</head>
<body>
    <!-- YOUR ORIGINAL CANVAS & SCRIPT HERE -->
</body>
</html>
"""

# Render your full 3D canvas
components.html(HTML_CODE, height=850, scrolling=False)

# ==========================================
# 3. CHAT HISTORY & AI RESPONSE LOGIC
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history above the input bar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Retrieve API key from secrets or environment
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", None))

if prompt := st.chat_input("Ask Orion anything..."):
    # Render user prompt immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream AI response
    with st.chat_message("assistant"):
        if not api_key:
            msg = "⚠️ **API Key missing!** Add `GEMINI_API_KEY = 'your_key'` in `.streamlit/secrets.toml`."
            st.warning(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        else:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                
                response_placeholder = st.empty()
                full_response = ""

                response_stream = client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                for chunk in response_stream:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"Error generating AI response: {e}")
