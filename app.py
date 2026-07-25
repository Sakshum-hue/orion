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
            background: #000000;
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
        const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false });
        const pixelRatio = Math.min(window.devicePixelRatio, 2);
        renderer.setPixelRatio(pixelRatio);
        renderer.autoClear = true;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);

        // ---------- Offscreen render target (for lensing + bloom post-process) ----------
        let rt = new THREE.WebGLRenderTarget(1, 1, {
            minFilter: THREE.LinearFilter,
            magFilter: THREE.LinearFilter,
            format: THREE.RGBAFormat
        });

        function sizeToWindow() {
            const w = window.innerWidth;
            const h = window.innerHeight;
            renderer.setSize(w, h, false);
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
            rt.setSize(w * pixelRatio, h * pixelRatio);
            if (postMat) postMat.uniforms.uResolution.value.set(w, h);
        }
        window.addEventListener('resize', sizeToWindow);

        // ---------- Orbit camera controls (no external deps) ----------
        let radius = 13, theta = Math.PI / 2.25, phi = Math.PI / 2.05;
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

        // ---------- Starfield (dense, layered for parallax depth) ----------
        function makeStarfield(count, minR, maxR, size, opacity) {
            const geo = new THREE.BufferGeometry();
            const pos = new Float32Array(count * 3);
            for (let i = 0; i < count; i++) {
                const r = minR + Math.random() * (maxR - minR);
                const t = Math.random() * Math.PI * 2;
                const p = Math.acos(2 * Math.random() - 1);
                pos[i * 3] = r * Math.sin(p) * Math.cos(t);
                pos[i * 3 + 1] = r * Math.cos(p);
                pos[i * 3 + 2] = r * Math.sin(p) * Math.sin(t);
            }
            geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
            const mat = new THREE.PointsMaterial({
                color: 0xffffff, size: size, sizeAttenuation: true,
                transparent: true, opacity: opacity
            });
            return new THREE.Points(geo, mat);
        }
        scene.add(makeStarfield(2600, 60, 160, 0.5, 0.7));
        scene.add(makeStarfield(900, 160, 320, 1.0, 0.9));

        // ---------- Soft blue glow halo (sprite from canvas gradient) ----------
        function makeGlowTexture() {
            const size = 256;
            const c = document.createElement('canvas');
            c.width = c.height = size;
            const ctx = c.getContext('2d');
            const g = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
            g.addColorStop(0, 'rgba(200, 225, 255, 0.95)');
            g.addColorStop(0.3, 'rgba(110, 175, 255, 0.5)');
            g.addColorStop(1, 'rgba(20, 40, 90, 0)');
            ctx.fillStyle = g;
            ctx.fillRect(0, 0, size, size);
            return new THREE.CanvasTexture(c);
        }
        const glowTex = makeGlowTexture();
        const glowSprite = new THREE.Sprite(new THREE.SpriteMaterial({
            map: glowTex, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false
        }));
        glowSprite.scale.set(10, 10, 1);
        scene.add(glowSprite);

        // ---------- Event horizon (pure black sphere) ----------
        const horizonRadius = 1.5;
        const horizon = new THREE.Mesh(
            new THREE.SphereGeometry(horizonRadius, 96, 96),
            new THREE.MeshBasicMaterial({ color: 0x000000 })
        );
        scene.add(horizon);

        // Rim glow (simulated light bending at the edge)
        const rim = new THREE.Mesh(
            new THREE.SphereGeometry(horizonRadius * 1.06, 64, 64),
            new THREE.MeshBasicMaterial({
                color: 0x5f9fff, transparent: true, opacity: 0.4,
                side: THREE.BackSide, blending: THREE.AdditiveBlending, depthWrite: false
            })
        );
        scene.add(rim);

        // Thin bright photon ring (Einstein ring at the horizon edge)
        const photonRing = new THREE.Mesh(
            new THREE.TorusGeometry(horizonRadius * 1.12, 0.015, 16, 128),
            new THREE.MeshBasicMaterial({
                color: 0xf0f8ff, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending, depthWrite: false
            })
        );
        scene.add(photonRing);

        // ---------- Accretion disk shader (shared code, turbulence + Doppler beaming) ----------
        const diskVertex = `
            varying float vDist;
            varying vec2 vUv2;
            void main() {
                vDist = length(position.xy);
                vUv2 = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `;
        const diskFragment = `
            uniform float uTime;
            uniform float uInner;
            uniform float uOuter;
            uniform float uOpacity;
            varying float vDist;
            varying vec2 vUv2;

            float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1,311.7))) * 43758.5453123); }
            float noise(vec2 p){
                vec2 i = floor(p); vec2 f = fract(p);
                float a = hash(i), b = hash(i+vec2(1.0,0.0)), c = hash(i+vec2(0.0,1.0)), d = hash(i+vec2(1.0,1.0));
                vec2 u = f*f*(3.0-2.0*f);
                return mix(a,b,u.x) + (c-a)*u.y*(1.0-u.x) + (d-b)*u.x*u.y;
            }
            float fbm(vec2 p){
                float v = 0.0; float amp = 0.55;
                for (int i = 0; i < 4; i++) { v += amp * noise(p); p *= 2.15; amp *= 0.5; }
                return v;
            }

            void main() {
                float t = clamp((vDist - uInner) / (uOuter - uInner), 0.0, 1.0);
                float angle = atan(vUv2.y - 0.5, vUv2.x - 0.5);

                float turb = fbm(vec2(angle * 2.4, vDist * 0.9 - uTime * 0.55));

                vec3 hot = vec3(1.0, 0.98, 0.94);
                vec3 whiteBlue = vec3(0.78, 0.9, 1.0);
                vec3 blue = vec3(0.22, 0.52, 1.0);
                vec3 deep = vec3(0.02, 0.07, 0.28);

                vec3 color = mix(hot, whiteBlue, smoothstep(0.0, 0.16, t));
                color = mix(color, blue, smoothstep(0.16, 0.52, t));
                color = mix(color, deep, smoothstep(0.52, 1.0, t));

                // relativistic Doppler beaming: one side brighter, other dimmer, as disk spins
                float beam = 0.5 + 0.5 * cos(angle - uTime * 0.5);
                color *= mix(0.55, 1.5, beam);

                float density = 0.35 + 0.65 * turb;
                float alpha = (1.0 - t) * density * uOpacity;
                alpha *= smoothstep(0.0, 0.06, t);
                alpha *= 1.0 - smoothstep(0.8, 1.0, t);

                gl_FragColor = vec4(color, alpha);
            }
        `;

        function makeDiskMaterial(inner, outer, opacity) {
            return new THREE.ShaderMaterial({
                uniforms: {
                    uTime: { value: 0 },
                    uInner: { value: inner },
                    uOuter: { value: outer },
                    uOpacity: { value: opacity }
                },
                vertexShader: diskVertex,
                fragmentShader: diskFragment,
                transparent: true,
                side: THREE.DoubleSide,
                blending: THREE.AdditiveBlending,
                depthWrite: false
            });
        }

        const innerR = horizonRadius * 1.28;
        const outerR = horizonRadius * 5.4;

        // Main tilted accretion disk
        const diskMat = makeDiskMaterial(innerR, outerR, 1.0);
        const disk = new THREE.Mesh(new THREE.RingGeometry(innerR, outerR, 160, 10), diskMat);
        disk.rotation.x = Math.PI / 2.55;
        scene.add(disk);

        // Secondary "lensed" halo ring standing more upright, mimicking the far side
        // of the disk bent by gravity to appear above/below the horizon (Interstellar-style halo)
        const haloMat = makeDiskMaterial(innerR * 0.92, outerR * 0.62, 0.55);
        const halo = new THREE.Mesh(new THREE.RingGeometry(innerR * 0.92, outerR * 0.62, 160, 8), haloMat);
        halo.rotation.x = Math.PI / 2 - 0.28;
        halo.rotation.z = Math.PI / 2;
        scene.add(halo);

        // ---------- Orbiting sparkle particles within the disk ----------
        const particleCount = 1100;
        const particleGeo = new THREE.BufferGeometry();
        const particlePos = new Float32Array(particleCount * 3);
        const particleData = [];
        for (let i = 0; i < particleCount; i++) {
            const r = innerR + Math.random() * (outerR - innerR);
            const a = Math.random() * Math.PI * 2;
            particleData.push({ r: r, a: a, speed: (0.18 + Math.random() * 0.4) / r });
            particlePos[i * 3] = r * Math.cos(a);
            particlePos[i * 3 + 1] = (Math.random() - 0.5) * 0.05;
            particlePos[i * 3 + 2] = r * Math.sin(a);
        }
        particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
        const particleMat = new THREE.PointsMaterial({
            color: 0xd0e8ff, size: 0.045, transparent: true, opacity: 0.9,
            blending: THREE.AdditiveBlending, depthWrite: false
        });
        const particles = new THREE.Points(particleGeo, particleMat);
        particles.rotation.x = Math.PI / 2.55;
        scene.add(particles);

        // ---------- Post-processing pass: gravitational lensing distortion + bloom ----------
        const postScene = new THREE.Scene();
        const postCamera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
        const postMat = new THREE.ShaderMaterial({
            uniforms: {
                tDiffuse: { value: rt.texture },
                uBHScreen: { value: new THREE.Vector2(0.5, 0.5) },
                uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) }
            },
            vertexShader: `
                varying vec2 vUv;
                void main() {
                    vUv = uv;
                    gl_Position = vec4(position, 1.0);
                }
            `,
            fragmentShader: `
                uniform sampler2D tDiffuse;
                uniform vec2 uBHScreen;
                uniform vec2 uResolution;
                varying vec2 vUv;

                vec3 sampleBloom(vec2 uv) {
                    vec3 col = vec3(0.0);
                    float total = 0.0;
                    for (int x = -2; x <= 2; x++) {
                        for (int y = -2; y <= 2; y++) {
                            vec2 offset = vec2(float(x), float(y)) * 2.2 / uResolution;
                            float w = 1.0 / (1.0 + float(x*x + y*y));
                            col += texture2D(tDiffuse, uv + offset).rgb * w;
                            total += w;
                        }
                    }
                    return col / total;
                }

                void main() {
                    vec2 uv = vUv;
                    float aspect = uResolution.x / uResolution.y;
                    vec2 toCenter = uv - uBHScreen;
                    toCenter.x *= aspect;
                    float dist = length(toCenter);

                    float lensStrength = 0.05;
                    float warp = lensStrength / (dist * dist + 0.015);
                    vec2 dir = dist > 0.0001 ? toCenter / dist : vec2(0.0);
                    vec2 dirUv = vec2(dir.x / aspect, dir.y);
                    vec2 warpedUV = uv - dirUv * warp * 0.045;
                    warpedUV = clamp(warpedUV, vec2(0.001), vec2(0.999));

                    vec3 base = texture2D(tDiffuse, warpedUV).rgb;

                    float ca = clamp(warp * 0.5, 0.0, 0.02);
                    base.r = texture2D(tDiffuse, clamp(warpedUV + dirUv * ca, 0.001, 0.999)).r;
                    base.b = texture2D(tDiffuse, clamp(warpedUV - dirUv * ca, 0.001, 0.999)).b;

                    vec3 bloom = sampleBloom(uv);
                    float brightness = dot(bloom, vec3(0.299, 0.587, 0.114));
                    vec3 bloomGlow = bloom * smoothstep(0.32, 1.0, brightness) * 0.9;

                    vec3 color = base + bloomGlow;

                    float vig = smoothstep(0.95, 0.25, length(uv - 0.5));
                    color *= mix(0.65, 1.0, vig);

                    gl_FragColor = vec4(color, 1.0);
                }
            `
        });
        const postQuad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), postMat);
        postScene.add(postQuad);

        sizeToWindow();

        function projectToScreen(object3D) {
            const v = new THREE.Vector3();
            v.setFromMatrixPosition(object3D.matrixWorld);
            v.project(camera);
            return new THREE.Vector2((v.x + 1) / 2, (v.y + 1) / 2);
        }

        // ---------- Animate ----------
        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();

            diskMat.uniforms.uTime.value = t;
            haloMat.uniforms.uTime.value = t * 0.8;
            disk.rotation.z += 0.0015;
            halo.rotation.y += 0.0009;

            const posAttr = particleGeo.attributes.position;
            for (let i = 0; i < particleCount; i++) {
                const d = particleData[i];
                d.a += d.speed * 0.02;
                posAttr.array[i * 3] = d.r * Math.cos(d.a);
                posAttr.array[i * 3 + 2] = d.r * Math.sin(d.a);
            }
            posAttr.needsUpdate = true;

            glowSprite.scale.setScalar(10 + Math.sin(t * 0.6) * 0.35);

            if (autoRotate) {
                targetTheta += 0.0012;
            }
            updateCamera();
            horizon.updateMatrixWorld();

            const screenPos = projectToScreen(horizon);
            postMat.uniforms.uBHScreen.value.copy(screenPos);

            renderer.setRenderTarget(rt);
            renderer.render(scene, camera);
            renderer.setRenderTarget(null);
            renderer.render(postScene, postCamera);
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
