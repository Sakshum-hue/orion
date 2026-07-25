import os
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. PAGE SETUP
# ==========================================
st.set_page_config(
    page_title="Orion AI Assistant",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. CUSTOM GLASSMORPHISM & UI OVERRIDES
# ==========================================
st.markdown("""
<style>
/* Hide standard Streamlit header & footer */
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0rem !important;
    max-width: 100% !important;
}

/* Floating Glassmorphic Chat Messages */
[data-testid="stChatMessage"] {
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 240, 255, 0.2) !important;
    border-radius: 12px !important;
    margin-bottom: 12px !important;
    color: #e2e8f0 !important;
    padding: 12px 18px !important;
}

/* Glassmorphic Chat Input Bar Fixed at Bottom */
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
# 3. EMBEDDED THREE.JS 3D BLACK HOLE CANVAS
# ==========================================
BLACK_HOLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background-color: #030712; }
        canvas { display: block; width: 100vw; height: 100vh; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Starfield Background
        const starsGeometry = new THREE.BufferGeometry();
        const starsCount = 2500;
        const starPositions = new Float32Array(starsCount * 3);
        for(let i = 0; i < starsCount * 3; i++) {
            starPositions[i] = (Math.random() - 0.5) * 120;
        }
        starsGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
        const starsMaterial = new THREE.PointsMaterial({ color: 0x88ccff, size: 0.12 });
        const starField = new THREE.Points(starsGeometry, starsMaterial);
        scene.add(starField);

        // Event Horizon (Black Hole Center)
        const sphereGeo = new THREE.SphereGeometry(1.8, 64, 64);
        const sphereMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
        const blackHole = new THREE.Mesh(sphereGeo, sphereMat);
        scene.add(blackHole);

        // Accretion Ring Glow
        const ringGeo = new THREE.RingGeometry(2.1, 4.8, 64);
        const ringMat = new THREE.MeshBasicMaterial({ 
            color: 0x00f0ff, 
            side: THREE.DoubleSide, 
            transparent: true, 
            opacity: 0.75 
        });
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.rotation.x = Math.PI / 2.3;
        scene.add(ring);

        camera.position.z = 6;

        // Animation Loop
        function animate() {
            requestAnimationFrame(animate);
            ring.rotation.z += 0.006;
            starField.rotation.y += 0.0003;
            renderer.render(scene, camera);
        }
        animate();

        // Responsive resizing
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

# Render 3D WebGL Canvas
components.html(BLACK_HOLE_HTML, height=750, scrolling=False)

# ==========================================
# 4. CHAT STATE & MESSAGES
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 5. CHAT INPUT & LLM RESPONSE
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", None))

if prompt := st.chat_input("Ask Orion anything..."):
    # Render user prompt immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        if not api_key:
            msg = "⚠️ **API Key missing!** Add `GEMINI_API_KEY = 'your_key'` inside your `.streamlit/secrets.toml` file to enable AI responses."
            st.warning(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        else:
            try:
                from google import genai
                client = genai.Client(api_key=api_key)
                
                response_placeholder = st.empty()
                full_response = ""

                # Stream response live
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
