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
    Streams response text with automatic failover between Groq and Gemini.
    """
    provider_pool = []
    for idx, k in enumerate(groq_keys, start=1):
        provider_pool.append(("groq", k, f"Groq Key #{idx}"))
    for idx, k in enumerate(gemini_keys, start=1):
        provider_pool.append(("gemini", k, f"Gemini Key #{idx}"))

    error_logs = []

    for provider, key, label in provider_pool:
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
                        yield chunk.choices[0].delta.content, {"provider": f"Groq ({label})"}
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
                        yield chunk.text, {"provider": f"Gemini ({label})"}
                return

        except Exception as e:
            error_logs.append(f"❌ **{label}**: `{e}`")
            continue

    error_summary = "\n\n".join(error_logs)
    yield f"\n\n⚠️ **All API keys failed! Here is the breakdown:**\n\n{error_summary}", None

# 3. Streamlit Chat Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "usage" in message and message["usage"]:
            st.caption(f"⚡ **{message['usage']['provider']}**")

# User Chat Input
if user_input := st.chat_input("Ask Orion anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        provider_meta = None

        for token, meta in generate_response_stream(st.session_state.messages):
            if token:
                full_response += token
                response_placeholder.markdown(full_response + "▌")
            if meta:
                provider_meta = meta

        response_placeholder.markdown(full_response)

        if provider_meta:
            st.caption(f"⚡ **{provider_meta['provider']}**")

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "usage": provider_meta
    })
