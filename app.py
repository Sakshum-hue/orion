import streamlit as st
from google import genai
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Orion AI Assistant",
    page_icon="🌌",
    layout="wide",
)

st.title("🌌 Orion AI Assistant")

# 2. Retrieve Secrets & Setup Fallback Streamer
SYSTEM_PROMPT = (
    "You are Orion, an advanced, intelligent, and articulate sci-fi AI assistant. "
    "Provide clear, crisp, insightful answers with a touch of cosmic warmth."
)

groq_keys = st.secrets.get("GROQ_API_KEYS", [])
gemini_keys = st.secrets.get("GEMINI_API_KEYS", [])

def generate_response_stream(messages_history):
    """
    Streams response text with automatic failover between underlying engines,
    keeping all provider details strictly hidden from end-users.
    """
    provider_pool = [("groq", k) for k in groq_keys] + [("gemini", k) for k in gemini_keys]

    for provider, key in provider_pool:
        try:
            if provider == "groq":
                client = Groq(api_key=key)
                formatted_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                for msg in messages_history:
                    formatted_messages.append({"role": msg["role"], "content": msg["content"]})

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=formatted_messages,
                    stream=True,
                )

                for chunk in completion:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
                return

            elif provider == "gemini":
                client = genai.Client(api_key=key)
                formatted_contents = [{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}]
                for msg in messages_history:
                    formatted_contents.append({
                        "role": "user" if msg["role"] == "user" else "model",
                        "parts": [{"text": msg["content"]}]
                    })

                response_stream = client.models.generate_content_stream(
                    model="gemini-2.0-flash",
                    contents=formatted_contents
                )

                for chunk in response_stream:
                    if chunk.text:
                        yield chunk.text
                return

        except Exception:
            # Silently skip any key or provider error and try the next one
            continue

    yield "\n\n⚠️ **System temporarily unavailable.** Please try again in a few moments."

# 3. Streamlit Chat Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
if user_input := st.chat_input("Ask Orion anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        for token in generate_response_stream(st.session_state.messages):
            full_response += token
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
    })
