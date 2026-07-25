import os
import streamlit as st
import streamlit.components.v1 as components

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Orion AI Assistant",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- 2. Custom CSS to clean up UI ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

# --- 3. Load Custom 3D Component ---
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "3d_components")

planet_viewer = components.declare_component("planet_viewer", path=build_dir)

# Render the 3D viewport iframe
selected_world = planet_viewer(key="orion_3d", default=None)

# --- 4. Update Active Location from 3D Viewport Clicks ---
if selected_world:
    st.session_state["active_world"] = selected_world.get("name")
    st.session_state["world_type"] = selected_world.get("type")

current_world = st.session_state.get("active_world", "Event Horizon")
st.caption(f"📍 **Current Location:** {current_world}")

# --- 5. Streamlit Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Greetings. I am Orion AI, stationed at **{current_world}**. How can I assist you today?"}
    ]

# Render past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
if prompt := st.chat_input("Ask Orion AI..."):
    # Append & display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    response_text = f"Transmitting from **{current_world}**: Received message: *'{prompt}'*"
    
    with st.chat_message("assistant"):
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
