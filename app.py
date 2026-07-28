import streamlit as st
import streamlit.components.v1 as components

# --- Page Setup ---
st.set_page_config(
    page_title="Orion AI Assistant",
    page_icon="🕳️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Hide Standard Streamlit UI & Custom CSS ---
st.markdown(
    """
    <style>
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0rem !important; }
    
    /* Fixed Chat Input Overlay */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        width: 60% !important;
        max-width: 800px;
        z-index: 999;
    }
    div[data-testid="stChatInput"] input {
        background: rgba(15, 23, 42, 0.65) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(120, 170, 255, 0.3) !important;
        backdrop-filter: blur(12px) !important;
        color: #ffffff !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- Three.js Background Component ---
# (Pasting your HTML string here)
HTML_3D_SCENE = """
<!DOCTYPE html>
<html>
... <!-- Your Three.js canvas & script content -->
</html>
"""

components.html(HTML_3D_SCENE, height=820, scrolling=False)

# --- Chat Interface & Input ---
user_query = st.chat_input("Ask Orion AI anything...", key="chat_input")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Example response generation placeholder
    response = f"Received: {user_query}"
    st.session_state.messages.append({"role": "assistant", "content": response})
