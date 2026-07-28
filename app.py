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

# --- Three.js 3D Scene ---
HTML_3D_SCENE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 100%; height: 100vh; overflow: hidden; background: #030712; }
    canvas { display: block; width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
  <script>
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 3, 12);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    document.body.appendChild(renderer.domElement);

    // Black Hole Event Horizon
    const holeGeo = new THREE.SphereGeometry(2, 64, 64);
    const holeMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
    const blackHole = new THREE.Mesh(holeGeo, holeMat);
    scene.add(blackHole);

    // Photon Ring Wireframe
    const glowGeo = new THREE.SphereGeometry(2.1, 64, 64);
    const glowMat = new THREE.MeshBasicMaterial({ 
      color: 0x60a5fa, 
      wireframe: true, 
      transparent: true, 
      opacity: 0.15 
    });
    const photonRing = new THREE.Mesh(glowGeo, glowMat);
    scene.add(photonRing);

    // Accretion Disk Particles
    const particleCount = 8000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const color1 = new THREE.Color(0x3b82f6); // Blue
    const color2 = new THREE.Color(0xf97316); // Orange

    for (let i = 0; i < particleCount; i++) {
      const radius = 2.5 + Math.random() * 6;
      const angle = Math.random() * Math.PI * 2;
      const y = (Math.random() - 0.5) * 0.4 * (radius - 2);

      positions[i * 3] = Math.cos(angle) * radius;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = Math.sin(angle) * radius;

      const mixedColor = color1.clone().lerp(color2, (radius - 2.5) / 6);
      colors[i * 3] = mixedColor.r;
      colors[i * 3 + 1] = mixedColor.g;
      colors[i * 3 + 2] = mixedColor.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const pMaterial = new THREE.PointsMaterial({
      size: 0.05,
      vertexColors: true,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending
    });

    const accretionDisk = new THREE.Points(geometry, pMaterial);
    accretionDisk.rotation.x = 0.4;
    scene.add(accretionDisk);

    // Starfield Background
    const starCount = 2000;
    const starGeo = new THREE.BufferGeometry();
    const starPos = new Float32Array(starCount * 3);

    for(let i = 0; i < starCount; i++) {
      starPos[i * 3] = (Math.random() - 0.5) * 100;
      starPos[i * 3 + 1] = (Math.random() - 0.5) * 100;
      starPos[i * 3 + 2] = (Math.random() - 0.5) * 100;
    }

    starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
    const starMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.03, transparent: true, opacity: 0.6 });
    const starField = new THREE.Points(starGeo, starMat);
    scene.add(starField);

    camera.lookAt(0, 0, 0);

    function animate() {
      requestAnimationFrame(animate);
      accretionDisk.rotation.y += 0.003;
      photonRing.rotation.y += 0.002;
      starField.rotation.y += 0.0002;
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
  </script>
</body>
</html>
"""

components.html(HTML_3D_SCENE, height=850, scrolling=False)

# --- Chat Interface & Input ---
user_query = st.chat_input("Ask Orion AI anything...", key="chat_input")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Response placeholder
    response = f"Received: {user_query}"
    st.session_state.messages.append({"role": "assistant", "content": response})
