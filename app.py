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
    Streams response text and yields token usage metadata upon stream completion.
    """
    provider_pool = [("groq", k) for k in groq_keys] + [("gemini", k) for k in gemini_keys]
    last_exception = None

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
                    stream_options={"include_usage": True},  # Enables token usage reporting
                )

                usage_info = None
                for chunk in completion:
                    if chunk.choices and chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content, None

                    # Extract usage metadata from final chunk
                    if hasattr(chunk, "usage") and chunk.usage:
                        usage_info = {
                            "provider": "Groq (Llama 3.3 70B)",
                            "prompt": chunk.usage.prompt_tokens,
                            "completion": chunk.usage.completion_tokens,
                            "total": chunk.usage.total_tokens,
                        }

                if usage_info:
                    yield "", usage_info
                return

            elif provider == "gemini":
                client = genai.Client(api_key=key)
                formatted_contents = [{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}]
                for msg in messages_history:
                    formatted_contents.append({
                        "role": "user" if msg["role"] == "user" else "model",
                        "parts": [{"text": msg["content"]}]
                    })

                # Active Gemini model identifier
                response_stream = client.models.generate_content_stream(
                    model="gemini-2.0-flash",
                    contents=formatted_contents
                )

                usage_info = None
                for chunk in response_stream:
                    if chunk.text:
                        yield chunk.text, None

                    # Extract usage metadata from stream chunk
                    if hasattr(chunk, "usage_metadata") and chunk.usage_metadata:
                        usage_info = {
                            "provider": "Gemini 2.0 Flash",
                            "prompt": chunk.usage_metadata.prompt_token_count or 0,
                            "completion": chunk.usage_metadata.candidates_token_count or 0,
                            "total": chunk.usage_metadata.total_token_count or 0,
                        }

                if usage_info:
                    yield "", usage_info
                return

        except Exception as e:
            last_exception = e
            continue

    yield f"\n\n⚠️ **All API keys exhausted or rate-limited.** Details: `{last_exception}`", None

# 3. Streamlit Chat Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "usage" in message and message["usage"]:
            u = message["usage"]
            st.caption(
                f"⚡ **{u['provider']}** | "
                f"Prompt: `{u['prompt']}` | Completion: `{u['completion']}` | Total: `{u['total']}` tokens"
            )

# User Chat Input
if user_input := st.chat_input("Ask Orion anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        token_usage = None

        for token, usage in generate_response_stream(st.session_state.messages):
            if token:
                full_response += token
                response_placeholder.markdown(full_response + "▌")
            if usage:
                token_usage = usage

        response_placeholder.markdown(full_response)

        if token_usage:
            st.caption(
                f"⚡ **{token_usage['provider']}** | "
                f"Prompt: `{token_usage['prompt']}` | Completion: `{token_usage['completion']}` | Total: `{token_usage['total']}` tokens"
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "usage": token_usage
    })
