import streamlit as st
import streamlit.components.v1 as components

# --- Page Setup ---
st.set_page_config(
    page_title="Orion AI Assistant",
    page_icon="🕳️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Hide Standard Streamlit UI ---
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0rem;}
    .stChatInputContainer {
        position: fixed;
        bottom: 10px;
        background-color: transparent !important;
        border: none !important;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 3D Black Hole Background + Glass UI ---
components.html(
    """
    <style>
        html, body { margin: 0; padding: 0; overflow: hidden; background: #000; }
        #bh-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            display: block;
            z-index: -1;
            background: radial-gradient(ellipse at center, #050510 0%, #000000 70%);
        }

        .glass-panel {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(8.5px);
            -webkit-backdrop-filter: blur(8.5px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            position: fixed;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            pointer-events: none;
        }

        .header-panel {
            top: 6vh;
            width: 80%;
            height: 14vh;
        }

        .orion-text-main {
            color: rgba(255, 255, 255, 0.92);
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-weight: 800;
            font-size: 4.2rem;
            text-shadow: 0 0 25px rgba(90, 160, 255, 0.55);
            letter-spacing: -2px;
            margin: 0;
        }

        .orion-text-sub {
            color: rgba(190, 220, 255, 0.75);
            font-family: 'SF Pro Display', -apple-system, sans-serif;
            font-weight: 500;
            font-size: 1.15rem;
            margin-top: 6px;
            letter-spacing: 4px;
            text-transform: uppercase;
        }

        .hint {
            position: fixed;
            bottom: 4vh;
            left: 50%;
            transform: translateX(-50%);
            color: rgba(255,255,255,0.35);
            font-family: -apple-system, sans-serif;
            font-size: 0.8rem;
            letter-spacing: 1px;
            pointer-events: none;
        }
    </style>

    <canvas id="bh-canvas"></canvas>

    <div style="position: fixed; top: 4vh; left: 50%; transform: translateX(-50%); text-align: center; z-index: 2;">
        <h1 class="orion-text-main">ORION AI</h1>
        <div class="orion-text-sub">Event Horizon Interface</div>
    </div>

    <div class="hint">drag to orbit &nbsp;•&nbsp; scroll to zoom</div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    (function () {
        const canvas = document.getElementById('bh-canvas');
        const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);

        function sizeToWindow() {
            const w = window.innerWidth;
            const h = window.innerHeight;
            renderer.setSize(w, h, false);
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
        }
        sizeToWindow();
        window.addEventListener('resize', sizeToWindow);

        // ---------- Orbit camera controls (no external deps) ----------
        let radius = 14, theta = Math.PI / 2.3, phi = Math.PI / 2.15;
        let targetTheta = theta, targetPhi = phi, targetRadius = radius;
        let isDragging = false, lastX = 0, lastY = 0;
        let autoRotate = true;

        function updateCamera() {
            theta += (targetTheta - theta) * 0.08;
            phi += (targetPhi - phi) * 0.08;
            radius += (targetRadius - radius) * 0.08;
            const x = radius * Math.sin(phi) * Math.cos(theta);
            const y = radius * Math.cos(phi);
            const z = radius * Math.sin(phi) * Math.sin(theta);
            camera.position.set(x, y, z);
            camera.lookAt(0, 0, 0);
        }

        canvas.addEventListener('pointerdown', (e) => {
            isDragging = true; autoRotate = false;
            lastX = e.clientX; lastY = e.clientY;
        });
        window.addEventListener('pointerup', () => { isDragging = false; });
        window.addEventListener('pointermove', (e) => {
            if (!isDragging) return;
            const dx = e.clientX - lastX;
            const dy = e.clientY - lastY;
            lastX = e.clientX; lastY = e.clientY;
            targetTheta -= dx * 0.005;
            targetPhi -= dy * 0.005;
            targetPhi = Math.max(0.35, Math.min(Math.PI - 0.35, targetPhi));
        });
        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            targetRadius += e.deltaY * 0.01;
            targetRadius = Math.max(6, Math.min(28, targetRadius));
        }, { passive: false });

        // ---------- Starfield ----------
        const starGeo = new THREE.BufferGeometry();
        const starCount = 3000;
        const starPos = new Float32Array(starCount * 3);
        for (let i = 0; i < starCount; i++) {
            const r = 80 + Math.random() * 220;
            const t = Math.random() * Math.PI * 2;
            const p = Math.acos(2 * Math.random() - 1);
            starPos[i * 3] = r * Math.sin(p) * Math.cos(t);
            starPos[i * 3 + 1] = r * Math.cos(p);
            starPos[i * 3 + 2] = r * Math.sin(p) * Math.sin(t);
        }
        starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
        const starMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.6, sizeAttenuation: true, transparent: true, opacity: 0.8 });
        scene.add(new THREE.Points(starGeo, starMat));

        // ---------- Soft blue glow halo (sprite from canvas gradient) ----------
        function makeGlowTexture() {
            const size = 256;
            const c = document.createElement('canvas');
            c.width = c.height = size;
            const ctx = c.getContext('2d');
            const g = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
            g.addColorStop(0, 'rgba(160, 210, 255, 0.9)');
            g.addColorStop(0.35, 'rgba(90, 160, 255, 0.45)');
            g.addColorStop(1, 'rgba(20, 40, 90, 0)');
            ctx.fillStyle = g;
            ctx.fillRect(0, 0, size, size);
            return new THREE.CanvasTexture(c);
        }
        const glowTex = makeGlowTexture();
        const glowSprite = new THREE.Sprite(new THREE.SpriteMaterial({
            map: glowTex, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false
        }));
        glowSprite.scale.set(11, 11, 1);
        scene.add(glowSprite);

        // ---------- Event horizon (pure black sphere) ----------
        const horizonRadius = 1.6;
        const horizon = new THREE.Mesh(
            new THREE.SphereGeometry(horizonRadius, 64, 64),
            new THREE.MeshBasicMaterial({ color: 0x000000 })
        );
        scene.add(horizon);

        // Rim glow (simulated light bending at the edge)
        const rim = new THREE.Mesh(
            new THREE.SphereGeometry(horizonRadius * 1.08, 64, 64),
            new THREE.MeshBasicMaterial({
                color: 0x3f7fff, transparent: true, opacity: 0.35,
                side: THREE.BackSide, blending: THREE.AdditiveBlending, depthWrite: false
            })
        );
        scene.add(rim);

        // Thin bright photon ring
        const photonRing = new THREE.Mesh(
            new THREE.TorusGeometry(horizonRadius * 1.15, 0.02, 16, 128),
            new THREE.MeshBasicMaterial({
                color: 0xdff0ff, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false
            })
        );
        photonRing.rotation.x = Math.PI / 2;
        scene.add(photonRing);

        // ---------- Accretion disk (custom shader, bluish swirling gradient) ----------
        const innerR = horizonRadius * 1.3;
        const outerR = horizonRadius * 5.2;
        const diskGeo = new THREE.RingGeometry(innerR, outerR, 128, 8);

        const diskMat = new THREE.ShaderMaterial({
            uniforms: {
                uTime: { value: 0 },
                uInner: { value: innerR },
                uOuter: { value: outerR }
            },
            vertexShader: `
                varying float vDist;
                varying vec2 vUv2;
                void main() {
                    vDist = length(position.xy);
                    vUv2 = uv;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            `,
            fragmentShader: `
                uniform float uTime;
                uniform float uInner;
                uniform float uOuter;
                varying float vDist;
                varying vec2 vUv2;

                void main() {
                    float t = (vDist - uInner) / (uOuter - uInner);
                    t = clamp(t, 0.0, 1.0);

                    vec3 hot = vec3(0.92, 0.97, 1.0);
                    vec3 mid = vec3(0.25, 0.55, 1.0);
                    vec3 deep = vec3(0.03, 0.10, 0.35);

                    vec3 color = mix(hot, mid, smoothstep(0.0, 0.35, t));
                    color = mix(color, deep, smoothstep(0.35, 1.0, t));

                    float angle = atan(vUv2.y - 0.5, vUv2.x - 0.5);
                    float swirl = sin(angle * 10.0 - uTime * 1.8 + t * 6.0) * 0.5 + 0.5;

                    float alpha = (1.0 - t) * (0.55 + 0.45 * swirl);
                    alpha *= smoothstep(0.0, 0.06, t);
                    alpha *= 1.0 - smoothstep(0.82, 1.0, t);

                    gl_FragColor = vec4(color, alpha);
                }
            `,
            transparent: true,
            side: THREE.DoubleSide,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        });

        const disk = new THREE.Mesh(diskGeo, diskMat);
        disk.rotation.x = Math.PI / 2.6;
        scene.add(disk);

        // ---------- Orbiting particle sparkle over the disk ----------
        const particleCount = 900;
        const particleGeo = new THREE.BufferGeometry();
        const particlePos = new Float32Array(particleCount * 3);
        const particleData = [];
        for (let i = 0; i < particleCount; i++) {
            const r = innerR + Math.random() * (outerR - innerR);
            const a = Math.random() * Math.PI * 2;
            particleData.push({ r: r, a: a, speed: (0.15 + Math.random() * 0.35) / r });
            particlePos[i * 3] = r * Math.cos(a);
            particlePos[i * 3 + 1] = 0;
            particlePos[i * 3 + 2] = r * Math.sin(a);
        }
        particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
        const particleMat = new THREE.PointsMaterial({
            color: 0xbfe0ff, size: 0.05, transparent: true, opacity: 0.85,
            blending: THREE.AdditiveBlending, depthWrite: false
        });
        const particles = new THREE.Points(particleGeo, particleMat);
        particles.rotation.x = Math.PI / 2.6;
        scene.add(particles);

        // ---------- Animate ----------
        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();

            diskMat.uniforms.uTime.value = t;
            disk.rotation.z += 0.0015;

            const posAttr = particleGeo.attributes.position;
            for (let i = 0; i < particleCount; i++) {
                const d = particleData[i];
                d.a += d.speed * 0.02;
                posAttr.array[i * 3] = d.r * Math.cos(d.a);
                posAttr.array[i * 3 + 2] = d.r * Math.sin(d.a);
            }
            posAttr.needsUpdate = true;

            glowSprite.scale.setScalar(11 + Math.sin(t * 0.6) * 0.4);

            if (autoRotate) {
                targetTheta += 0.0012;
            }
            updateCamera();
            renderer.render(scene, camera);
        }
        animate();
    })();
    </script>
    """,
    height=850,
    scrolling=False,
)

# Chat input
st.chat_input("Ask Orion AI anything...", key="chat_input")

# Style the chat input to match the glass aesthetic
input_customization = """
    <style>
    .stChatInputContainer input {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(120, 170, 255, 0.25) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        padding-left: 20px !important;
        font-family: 'SF Pro Display', sans-serif !important;
    }
    .stTabs button {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(5px) !important;
        color: rgba(255, 255, 255, 0.6) !important;
    }
    .stTabs button[aria-selected="true"] {
        background: rgba(90, 160, 255, 0.15) !important;
        color: white !important;
    }
    </style>
"""
st.markdown(input_customization, unsafe_allow_html=True)
