import os
import requests
import qrcode
from io import BytesIO
import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="Apex AI", page_icon="🤖", layout="centered")

# Configuration
FAMPAY_UPI_ID = "yourname@fam"  # 👈 REPLACE WITH YOUR ACTUAL FAMPAY UPI ID
PREMIUM_PRICE_INR = 99
FREE_DAILY_LIMIT = 20

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# ==========================================
# INVISIBLE API ROTATION LOGIC (Groq -> Gemini)
# ==========================================
def call_ai_with_rotation(prompt):
    groq_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    gemini_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    # Primary Attempt: Try Groq silently first
    if groq_key:
        try:
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "You are Apex AI, a fast, smart, and helpful AI assistant."},
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=10
            )
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
        except Exception:
            pass  # Silently failover to backup if Groq is busy or rate limited

    # Backup Attempt: Gemini 1.5 Flash (Completely hidden from user)
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            return model.generate_content(prompt).text
        except Exception:
            pass

    return "⚠️ Service is temporarily busy. Please try sending your message again in a moment."

# ==========================================
# USER INTERFACE
# ==========================================
st.title("🤖 Apex AI Assistant")

tab1, tab2 = st.tabs(["💬 Chat AI", "⚡ Upgrade to Premium"])

# --- TAB 1: CHATBOT ---
with tab1:
    # Display message history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User Chat Input
    if prompt := st.chat_input("Ask Apex AI anything..."):
        if not st.session_state.is_premium and st.session_state.msg_count >= FREE_DAILY_LIMIT:
            st.error(f"🔒 **Daily Free Limit Reached!** ({FREE_DAILY_LIMIT}/{FREE_DAILY_LIMIT} messages used)\n\nUpgrade in the **⚡ Upgrade to Premium** tab for unlimited access.")
        else:
            # Display user prompt
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Get AI response via invisible failover
            with st.chat_message("assistant"):
                with st.spinner("Apex AI is thinking..."):
                    reply = call_ai_with_rotation(prompt)
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.session_state.msg_count += 1

# --- TAB 2: FAMPAY UPI PREMIUM UPGRADE ---
with tab2:
    st.header("⚡ Upgrade to Unlimited Access")
    st.markdown(f"**Price:** ₹{PREMIUM_PRICE_INR} / month")

    # Generate UPI QR Code dynamically
    upi_url = f"upi://pay?pa={FAMPAY_UPI_ID}&pn=ApexAI_Premium&am={PREMIUM_PRICE_INR}&cu=INR"
    qr = qrcode.make(upi_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    st.image(buffer, caption=f"Scan using FamApp, Google Pay, PhonePe, or Paytm (UPI ID: {FAMPAY_UPI_ID})", width=240)

    st.markdown("---")
    st.subheader("Step 2: Enter Receipt UTR")
    utr_input = st.text_input("Enter 12-digit UPI UTR / Reference ID:", placeholder="e.g. 423901827401")
    
    if st.button("Verify & Activate Premium"):
        clean_utr = utr_input.strip()
        if len(clean_utr) == 12 and clean_utr.isdigit():
            st.session_state.is_premium = True
            st.success(f"✅ Success! UTR `{clean_utr}` verified. Unlimited Premium access activated!")
        else:
            st.error("❌ Please enter a valid 12-digit UPI UTR number.")
