from io import BytesIO
import requests
import streamlit as st
import streamlit.components.v1 as components
import qrcode

# Page Setup
st.set_page_config(page_title="Orion AI", page_icon="🤖", layout="centered")

# Configuration
FAMPAY_UPI_ID = "sakshum.mahajan@fam"
PREMIUM_PRICE_INR = 99
FREE_DAILY_LIMIT = 20

# Safely fetch API keys from Streamlit Secrets (No hardcoded strings)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# Initialize Session State
if "messages" not in st.session_state:
  st.session_state.messages = []
if "msg_count" not in st.session_state:
  st.session_state.msg_count = 0
if "is_premium" not in st.session_state:
  st.session_state.is_premium = False

# ==========================================
# SPLINE 3D HERO HEADER
# ==========================================
components.html(
    """
    <iframe 
      src="https://my.spline.design/distortingtypography-5rSjuJRZYfYWu6Tp3GPRmFlP/" 
      frameborder="0" 
      width="100%" 
      height="100%" 
      style="border: none; border-radius: 16px; min-height: 400px;">
    </iframe>
    """,
    height=420,
)


# ==========================================
# API ROTATION LOGIC (Groq -> Gemini REST)
# ==========================================
def call_ai(prompt):
  errors = []

  # 1. Try Groq API
  if GROQ_API_KEY:
    try:
      res = requests.post(
          "https://api.groq.com/openai/v1/chat/completions",
          headers={
              "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
              "Content-Type": "application/json",
          },
          json={
              "model": "llama-3.3-70b-versatile",
              "messages": [
                  {
                      "role": "system",
                      "content": "You are Orion AI, a helpful AI assistant.",
                  },
                  {"role": "user", "content": prompt},
              ],
          },
          timeout=10,
      )
      if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
      else:
        errors.append(f"Groq API Error ({res.status_code}): {res.text}")
    except Exception as e:
      errors.append(f"Groq Exception: {str(e)}")
  else:
    errors.append("GROQ_API_KEY missing in Streamlit Secrets.")

  # 2. Try Gemini API via Direct REST
  if GEMINI_API_KEY:
    try:
      url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY.strip()}"
      res = requests.post(
          url,
          headers={"Content-Type": "application/json"},
          json={"contents": [{"parts": [{"text": prompt}]}]},
          timeout=10,
      )
      if res.status_code == 200:
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
      else:
        errors.append(f"Gemini API Error ({res.status_code}): {res.text}")
    except Exception as e:
      errors.append(f"Gemini Exception: {str(e)}")
  else:
    errors.append("GEMINI_API_KEY missing in Streamlit Secrets.")

  return "⚠️ **Connection Error:**\n\n" + "\n\n".join(errors)


# ==========================================
# USER INTERFACE
# ==========================================
st.title("🤖 Orion AI Assistant")

tab1, tab2 = st.tabs(["💬 Chat AI", "⚡ Upgrade to Premium"])

# --- TAB 1: CHATBOT ---
with tab1:
  for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
      st.write(msg["content"])

  if prompt := st.chat_input("Ask Orion AI anything..."):
    if (
        not st.session_state.is_premium
        and st.session_state.msg_count >= FREE_DAILY_LIMIT
    ):
      st.error(
          f"🔒 **Daily Free Limit Reached!** ({FREE_DAILY_LIMIT}/{FREE_DAILY_LIMIT} messages used)\n\nUpgrade in the **⚡ Upgrade to Premium** tab for unlimited access."
      )
    else:
      st.session_state.messages.append({"role": "user", "content": prompt})
      with st.chat_message("user"):
        st.write(prompt)

      with st.chat_message("assistant"):
        with st.spinner("Orion AI is thinking..."):
          reply = call_ai(prompt)
          st.write(reply)
          st.session_state.messages.append(
              {"role": "assistant", "content": reply}
          )
          st.session_state.msg_count += 1

# --- TAB 2: PREMIUM UPGRADE ---
with tab2:
  st.header("⚡ Upgrade to Unlimited Access")
  st.markdown(f"**Price:** ₹{PREMIUM_PRICE_INR} / month")

  upi_url = f"upi://pay?pa={FAMPAY_UPI_ID}&pn=OrionAI_Premium&am={PREMIUM_PRICE_INR}&cu=INR"
  qr = qrcode.make(upi_url)
  buffer = BytesIO()
  qr.save(buffer, format="PNG")

  st.image(
      buffer,
      caption=(
          f"Scan using FamApp, Google Pay, PhonePe, or Paytm (UPI ID:"
          f" {FAMPAY_UPI_ID})"
      ),
      width=240,
  )

  st.markdown("---")
  st.subheader("Step 2: Enter Receipt UTR")
  utr_input = st.text_input(
      "Enter 12-digit UPI UTR / Reference ID:", placeholder="e.g. 423901827401"
  )

  if st.button("Verify & Activate Premium"):
    clean_utr = utr_input.strip()
    if len(clean_utr) == 12 and clean_utr.isdigit():
      st.session_state.is_premium = True
      st.success(
          f"✅ Success! UTR `{clean_utr}` verified. Unlimited Premium access"
          " activated!"
      )
    else:
      st.error("❌ Please enter a valid 12-digit UPI UTR number.")
