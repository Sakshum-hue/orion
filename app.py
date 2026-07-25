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

        // ---------- High-resolution deep-space skybox (nebula + stars, painted procedurally) ----------
        function makeSpaceSkyboxTexture() {
            const w = 4096, h = 2048;
            const c = document.createElement('canvas');
            c.width = w; c.height = h;
            const ctx = c.getContext('2d');

            // Deep space base gradient (near-black with a faint navy tone)
            const base = ctx.createLinearGradient(0, 0, 0, h);
            base.addColorStop(0, '#02030a');
            base.addColorStop(0.5, '#04050f');
            base.addColorStop(1, '#020208');
            ctx.fillStyle = base;
            ctx.fillRect(0, 0, w, h);

            // Soft nebula clouds in blues/violets/teals, all matching the theme
            const nebulaColors = [
                'rgba(70, 110, 220, 0.10)',
                'rgba(40, 160, 210, 0.09)',
                'rgba(110, 80, 210, 0.08)',
                'rgba(20, 60, 140, 0.12)'
            ];
            for (let i = 0; i < 26; i++) {
                const x = Math.random() * w;
                const y = Math.random() * h;
                const r = 150 + Math.random() * 420;
                const g = ctx.createRadialGradient(x, y, 0, x, y, r);
                const color = nebulaColors[i % nebulaColors.length];
                g.addColorStop(0, color);
                g.addColorStop(1, 'rgba(0,0,0,0)');
                ctx.fillStyle = g;
                ctx.beginPath();
                ctx.ellipse(x, y, r, r * (0.4 + Math.random() * 0.5), Math.random() * Math.PI, 0, Math.PI * 2);
                ctx.fill();
            }

            // Faint wispy dust lanes
            ctx.globalAlpha = 0.05;
            for (let i = 0; i < 6; i++) {
                ctx.strokeStyle = 'rgba(150,180,255,0.5)';
                ctx.lineWidth = 40 + Math.random() * 80;
                ctx.beginPath();
                const sy = Math.random() * h;
                ctx.moveTo(0, sy);
                ctx.bezierCurveTo(w*0.3, sy + (Math.random()-0.5)*300, w*0.7, sy + (Math.random()-0.5)*300, w, sy + (Math.random()-0.5)*200);
                ctx.stroke();
            }
            ctx.globalAlpha = 1.0;

            // Background stars: many tiny faint dots
            for (let i = 0; i < 9000; i++) {
                const x = Math.random() * w;
                const y = Math.random() * h;
                const b = Math.random();
                const size = b < 0.85 ? 0.7 : (b < 0.97 ? 1.3 : 2.0);
                const alpha = 0.25 + Math.random() * 0.55;
                // subtle warm/cool tint variety, mostly white-blue like real star photography
                const tint = Math.random();
                let color;
                if (tint < 0.7) color = `rgba(255,255,255,${alpha})`;
                else if (tint < 0.9) color = `rgba(190,215,255,${alpha})`;
                else color = `rgba(255,235,210,${alpha})`;
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(x, y, size, 0, Math.PI * 2);
                ctx.fill();
            }

            // Foreground hero stars with soft glow + subtle cross flare
            for (let i = 0; i < 55; i++) {
                const x = Math.random() * w;
                const y = Math.random() * h;
                const r = 3 + Math.random() * 5;
                const glow = ctx.createRadialGradient(x, y, 0, x, y, r * 6);
                glow.addColorStop(0, 'rgba(255,255,255,0.9)');
                glow.addColorStop(0.25, 'rgba(200,225,255,0.35)');
                glow.addColorStop(1, 'rgba(200,225,255,0)');
                ctx.fillStyle = glow;
                ctx.beginPath();
                ctx.arc(x, y, r * 6, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = 'rgba(255,255,255,0.95)';
                ctx.beginPath();
                ctx.arc(x, y, r, 0, Math.PI * 2);
                ctx.fill();

                ctx.strokeStyle = 'rgba(220,235,255,0.35)';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(x - r * 5, y); ctx.lineTo(x + r * 5, y);
                ctx.moveTo(x, y - r * 5); ctx.lineTo(x, y + r * 5);
                ctx.stroke();
            }

            const texture = new THREE.CanvasTexture(c);
            texture.mapping = THREE.EquirectangularReflectionMapping;
            texture.magFilter = THREE.LinearFilter;
            texture.minFilter = THREE.LinearMipmapLinearFilter;
            texture.wrapS = THREE.RepeatWrapping;
            return texture;
        }
        scene.background = makeSpaceSkyboxTexture();

        // A handful of crisp foreground stars for subtle parallax as the camera orbits
        function makeForegroundStars(count, minR, maxR) {
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
                color: 0xe8f2ff, size: 0.55, sizeAttenuation: true,
                transparent: true, opacity: 0.75
            });
            return new THREE.Points(geo, mat);
        }
        scene.add(makeForegroundStars(500, 60, 150));

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

        // ---------- Lighting for planets (the disk acts as the light source) ----------
        scene.add(new THREE.AmbientLight(0x1a2a4a, 0.55));
        const diskLight = new THREE.PointLight(0xbfe0ff, 2.4, 90, 2);
        diskLight.position.set(0, 0, 0);
        scene.add(diskLight);

        // ---------- Orbiting planets (procedurally textured, lit, with rim glow) ----------
        function makeRockyPlanetTexture(baseColor, accentColor) {
            const w = 512, h = 256;
            const c = document.createElement('canvas');
            c.width = w; c.height = h;
            const ctx = c.getContext('2d');
            ctx.fillStyle = baseColor;
            ctx.fillRect(0, 0, w, h);
            for (let i = 0; i < 300; i++) {
                const x = Math.random() * w;
                const y = Math.random() * h;
                const r = 2 + Math.random() * 12;
                ctx.fillStyle = accentColor;
                ctx.globalAlpha = 0.1 + Math.random() * 0.2;
                ctx.beginPath();
                ctx.arc(x, y, r, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.globalAlpha = 1.0;
            return new THREE.CanvasTexture(c);
        }

        function makeBandedPlanetTexture(colors) {
            const w = 512, h = 256;
            const c = document.createElement('canvas');
            c.width = w; c.height = h;
            const ctx = c.getContext('2d');
            const bands = 12;
            for (let i = 0; i < bands; i++) {
                ctx.fillStyle = colors[i % colors.length];
                const y0 = (h / bands) * i;
                ctx.fillRect(0, y0, w, h / bands + 2);
            }
            ctx.globalAlpha = 0.18;
            for (let i = 0; i < 45; i++) {
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1 + Math.random() * 2;
                ctx.beginPath();
                const y = Math.random() * h;
                ctx.moveTo(0, y);
                ctx.bezierCurveTo(w * 0.3, y + (Math.random() - 0.5) * 20, w * 0.7, y + (Math.random() - 0.5) * 20, w, y + (Math.random() - 0.5) * 10);
                ctx.stroke();
            }
            ctx.globalAlpha = 1.0;
            return new THREE.CanvasTexture(c);
        }

        const ringFragment = `
            uniform vec3 uColor;
            uniform float uInner;
            uniform float uOuter;
            varying float vDist;
            void main() {
                float t = clamp((vDist - uInner) / (uOuter - uInner), 0.0, 1.0);
                float stripe = sin(t * 45.0) * 0.15 + 0.85;
                float alpha = (0.3 + 0.35 * stripe) * smoothstep(0.0, 0.06, t) * (1.0 - smoothstep(0.9, 1.0, t));
                gl_FragColor = vec4(uColor * stripe, alpha);
            }
        `;

        const planetsConfig = [
            { size: 0.55, orbit: 10.5, speed: 0.0055, tilt: 0.16, spin: 0.012,
              texture: makeRockyPlanetTexture('#8a4a3a', '#e0895c'), rimColor: 0xff9a66 },
            { size: 0.4, orbit: 12.8, speed: 0.0042, tilt: -0.1, spin: 0.014,
              texture: makeRockyPlanetTexture('#2a5a8a', '#7fc4ff'), rimColor: 0x7fd0ff },
            { size: 1.0, orbit: 16.5, speed: 0.0026, tilt: 0.06, spin: 0.02,
              texture: makeBandedPlanetTexture(['#dcc192', '#c8a06e', '#eed8ae', '#b8905c']), rimColor: 0xffe0ac, ring: true },
            { size: 0.5, orbit: 20, speed: 0.002, tilt: 0.22, spin: 0.009,
              texture: makeRockyPlanetTexture('#2a6a52', '#63e0ae'), rimColor: 0x74f0c4 },
            { size: 0.22, orbit: 23, speed: 0.0016, tilt: -0.12, spin: 0.016,
              texture: makeRockyPlanetTexture('#7d7d7d', '#c2c2c2'), rimColor: 0xd6d6d6 }
        ];

        const planets = [];
        planetsConfig.forEach((cfg) => {
            const mat = new THREE.MeshStandardMaterial({ map: cfg.texture, roughness: 0.9, metalness: 0.04 });
            const mesh = new THREE.Mesh(new THREE.SphereGeometry(cfg.size, 32, 32), mat);
            scene.add(mesh);

            const planetRim = new THREE.Mesh(
                new THREE.SphereGeometry(cfg.size * 1.16, 24, 24),
                new THREE.MeshBasicMaterial({
                    color: cfg.rimColor, transparent: true, opacity: 0.28,
                    side: THREE.BackSide, blending: THREE.AdditiveBlending, depthWrite: false
                })
            );
            mesh.add(planetRim);

            if (cfg.ring) {
                const ringMat = new THREE.ShaderMaterial({
                    uniforms: {
                        uColor: { value: new THREE.Color(cfg.rimColor) },
                        uInner: { value: cfg.size * 1.4 },
                        uOuter: { value: cfg.size * 2.3 }
                    },
                    vertexShader: diskVertex,
                    fragmentShader: ringFragment,
                    transparent: true,
                    side: THREE.DoubleSide,
                    depthWrite: false
                });
                const ring = new THREE.Mesh(new THREE.RingGeometry(cfg.size * 1.4, cfg.size * 2.3, 96, 4), ringMat);
                ring.rotation.x = Math.PI / 2.3;
                mesh.add(ring);
            }

            planets.push({
                mesh: mesh,
                orbit: cfg.orbit,
                speed: cfg.speed,
                angle: Math.random() * Math.PI * 2,
                tilt: cfg.tilt,
                spin: cfg.spin
            });
        });

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

            planets.forEach((p) => {
                p.angle += p.speed;
                const x = p.orbit * Math.cos(p.angle);
                const z = p.orbit * Math.sin(p.angle);
                const y = Math.sin(p.angle * 0.5) * p.orbit * Math.sin(p.tilt);
                p.mesh.position.set(x, y, z);
                p.mesh.rotation.y += p.spin;
            });

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
