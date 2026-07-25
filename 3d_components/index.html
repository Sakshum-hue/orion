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

# --- Living, Interactive Black Hole Universe ---
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
            cursor: grab;
        }
        #bh-canvas.hoverable { cursor: pointer; }
        #bh-canvas:active { cursor: grabbing; }

        .glass-panel {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(8.5px);
            -webkit-backdrop-filter: blur(8.5px);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        .header-wrap {
            position: fixed;
            top: 4vh;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            z-index: 2;
            pointer-events: none;
            animation: floatY 6s ease-in-out infinite;
        }
        @keyframes floatY {
            0%, 100% { transform: translateX(-50%) translateY(0px); }
            50% { transform: translateX(-50%) translateY(-6px); }
        }

        .orion-text-main {
            color: rgba(255, 255, 255, 0.94);
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-weight: 800;
            font-size: 4.2rem;
            letter-spacing: -2px;
            margin: 0;
            animation: glowPulse 4s ease-in-out infinite;
        }
        @keyframes glowPulse {
            0%, 100% { text-shadow: 0 0 22px rgba(90, 160, 255, 0.45), 0 0 4px rgba(255,255,255,0.3); }
            50% { text-shadow: 0 0 40px rgba(120, 190, 255, 0.85), 0 0 10px rgba(255,255,255,0.5); }
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
            color: rgba(255,255,255,0.4);
            font-family: -apple-system, sans-serif;
            font-size: 0.8rem;
            letter-spacing: 1px;
            pointer-events: none;
            text-align: center;
            transition: opacity 0.4s ease;
        }

        .info-panel {
            position: fixed;
            left: 4vw;
            bottom: 6vh;
            max-width: 340px;
            padding: 18px 22px;
            z-index: 3;
            opacity: 0;
            transform: translateY(14px);
            transition: opacity 0.5s ease, transform 0.5s ease;
            pointer-events: none;
        }
        .info-panel.visible { opacity: 1; transform: translateY(0px); }
        .info-name {
            color: #eaf4ff;
            font-family: 'SF Pro Display', -apple-system, sans-serif;
            font-weight: 700;
            font-size: 1.3rem;
            letter-spacing: 1px;
            margin: 0 0 6px 0;
        }
        .info-desc {
            color: rgba(210, 228, 255, 0.8);
            font-family: -apple-system, sans-serif;
            font-weight: 400;
            font-size: 0.92rem;
            line-height: 1.4;
            margin: 0 0 10px 0;
        }
        .info-stats {
            display: flex;
            gap: 16px;
            margin-top: 4px;
        }
        .info-stat {
            display: flex;
            flex-direction: column;
        }
        .info-stat-label {
            color: rgba(170, 200, 255, 0.55);
            font-family: -apple-system, sans-serif;
            font-size: 0.62rem;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }
        .info-stat-value {
            color: #eaf4ff;
            font-family: -apple-system, sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .info-close {
            position: absolute;
            top: 10px;
            right: 14px;
            color: rgba(255,255,255,0.45);
            font-family: -apple-system, sans-serif;
            font-size: 0.75rem;
            cursor: pointer;
            pointer-events: auto;
            letter-spacing: 1px;
        }
        .info-close:hover { color: rgba(255,255,255,0.85); }

        /* Floating hover tooltip that follows the cursor */
        .hover-tip {
            position: fixed;
            z-index: 4;
            padding: 6px 12px;
            font-family: 'SF Pro Display', -apple-system, sans-serif;
            font-weight: 600;
            font-size: 0.82rem;
            letter-spacing: 0.5px;
            color: #eaf4ff;
            background: rgba(10, 18, 36, 0.55);
            border: 1px solid rgba(140, 190, 255, 0.35);
            border-radius: 8px;
            backdrop-filter: blur(6px);
            pointer-events: none;
            opacity: 0;
            transform: translate(-50%, -140%) scale(0.92);
            transition: opacity 0.15s ease, transform 0.15s ease;
            white-space: nowrap;
        }
        .hover-tip.visible { opacity: 1; transform: translate(-50%, -160%) scale(1); }

        /* Small legend of clickable worlds, bottom-right */
        .legend {
            position: fixed;
            right: 3vw;
            bottom: 6vh;
            z-index: 2;
            display: flex;
            flex-direction: column;
            gap: 8px;
            font-family: -apple-system, sans-serif;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 5px 10px;
            border-radius: 20px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            color: rgba(220, 232, 255, 0.65);
            font-size: 0.72rem;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: background 0.2s ease, color 0.2s ease, transform 0.2s ease;
        }
        .legend-item:hover, .legend-item.active {
            background: rgba(120, 175, 255, 0.16);
            color: #ffffff;
            transform: translateX(-3px);
        }
        .legend-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            box-shadow: 0 0 8px currentColor;
        }
    </style>

    <canvas id="bh-canvas"></canvas>

    <div class="header-wrap">
        <h1 class="orion-text-main">ORION AI</h1>
        <div class="orion-text-sub">Event Horizon Interface</div>
    </div>

    <div class="hint" id="hint">drag to orbit &nbsp;•&nbsp; scroll to zoom &nbsp;•&nbsp; hover or click a world to explore</div>

    <div class="glass-panel info-panel" id="info-panel">
        <div class="info-close" id="info-close">CLOSE ✕</div>
        <p class="info-name" id="info-name">—</p>
        <p class="info-desc" id="info-desc">—</p>
        <div class="info-stats">
            <div class="info-stat">
                <span class="info-stat-label">Orbit</span>
                <span class="info-stat-value" id="info-orbit">—</span>
            </div>
            <div class="info-stat">
                <span class="info-stat-label">Relative Size</span>
                <span class="info-stat-value" id="info-size">—</span>
            </div>
            <div class="info-stat">
                <span class="info-stat-label">Class</span>
                <span class="info-stat-value" id="info-class">—</span>
            </div>
        </div>
    </div>

    <div class="hover-tip" id="hover-tip">—</div>

    <div class="legend" id="legend"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    (function () {
        const canvas = document.getElementById('bh-canvas');
        const hintEl = document.getElementById('hint');
        const infoPanel = document.getElementById('info-panel');
        const infoName = document.getElementById('info-name');
        const infoDesc = document.getElementById('info-desc');
        const infoOrbit = document.getElementById('info-orbit');
        const infoSize = document.getElementById('info-size');
        const infoClass = document.getElementById('info-class');
        const infoClose = document.getElementById('info-close');
        const hoverTip = document.getElementById('hover-tip');
        const legendEl = document.getElementById('legend');

        const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false });
        const pixelRatio = Math.min(window.devicePixelRatio, 2);
        renderer.setPixelRatio(pixelRatio);
        renderer.autoClear = true;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);

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

        // ================= CAMERA: orbit + focus-follow + cursor parallax =================
        let radius = 13, theta = Math.PI / 2.25, phi = Math.PI / 2.05;
        let targetTheta = theta, targetPhi = phi, targetRadius = radius;
        let isDragging = false, dragMoved = false, lastX = 0, lastY = 0, downX = 0, downY = 0, downTime = 0;
        let autoRotate = true;

        const orbitCenter = new THREE.Vector3(0, 0, 0);
        const targetCenter = new THREE.Vector3(0, 0, 0);
        let focusedPlanet = null;
        let hoveredEntry = null;
        let lastPointerX = 0, lastPointerY = 0;

        let parallaxX = 0, parallaxY = 0, parallaxTargetX = 0, parallaxTargetY = 0;

        function updateCamera() {
            theta += (targetTheta - theta) * 0.07;
            phi += (targetPhi - phi) * 0.07;
            radius += (targetRadius - radius) * 0.07;
            parallaxX += (parallaxTargetX - parallaxX) * 0.04;
            parallaxY += (parallaxTargetY - parallaxY) * 0.04;

            if (focusedPlanet) {
                targetCenter.copy(focusedPlanet.mesh.position);
            } else {
                targetCenter.set(0, 0, 0);
            }
            orbitCenter.lerp(targetCenter, 0.08);

            const useTheta = theta + parallaxX;
            const usePhi = Math.max(0.35, Math.min(Math.PI - 0.35, phi + parallaxY));

            const x = orbitCenter.x + radius * Math.sin(usePhi) * Math.cos(useTheta);
            const y = orbitCenter.y + radius * Math.cos(usePhi);
            const z = orbitCenter.z + radius * Math.sin(usePhi) * Math.sin(useTheta);
            camera.position.set(x, y, z);
            camera.lookAt(orbitCenter);
        }

        canvas.addEventListener('pointerdown', (e) => {
            isDragging = true; dragMoved = false; autoRotate = false;
            lastX = downX = e.clientX; lastY = downY = e.clientY;
            downTime = performance.now();
        });
        window.addEventListener('pointerup', (e) => {
            isDragging = false;
            const dx = e.clientX - downX, dy = e.clientY - downY;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const elapsed = performance.now() - downTime;
            if (dist < 6 && elapsed < 400) handleClick(e);
        });
        window.addEventListener('pointermove', (e) => {
            const nx = (e.clientX / window.innerWidth) * 2 - 1;
            const ny = (e.clientY / window.innerHeight) * 2 - 1;
            parallaxTargetX = nx * 0.18;
            parallaxTargetY = ny * 0.1;
            lastPointerX = e.clientX;
            lastPointerY = e.clientY;

            if (!isDragging) {
                updateHover(e.clientX, e.clientY);
            }

            if (!isDragging) return;
            dragMoved = true;
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
            targetRadius = Math.max(2.5, Math.min(30, targetRadius));
        }, { passive: false });

        // ================= RAYCAST: hover + click, focus planets, pulse the hole =================
        const raycaster = new THREE.Raycaster();
        const ndc = new THREE.Vector2();
        const meshToPlanet = new Map();

        let pulseStart = -999;
        function triggerPulse() { pulseStart = clock.getElapsedTime(); }

        function updateHover(clientX, clientY) {
            const rect = canvas.getBoundingClientRect();
            ndc.x = ((clientX - rect.left) / rect.width) * 2 - 1;
            ndc.y = -((clientY - rect.top) / rect.height) * 2 + 1;
            raycaster.setFromCamera(ndc, camera);

            const planetMeshes = planets.map((p) => p.mesh);
            const hits = raycaster.intersectObjects(planetMeshes, true);

            let entry = null;
            if (hits.length > 0) {
                let obj = hits[0].object;
                while (obj && !meshToPlanet.has(obj)) obj = obj.parent;
                if (obj) entry = meshToPlanet.get(obj);
            }

            if (entry !== hoveredEntry) {
                hoveredEntry = entry;
                canvas.classList.toggle('hoverable', !!entry);
                if (entry) {
                    hoverTip.textContent = entry.cfg.name;
                    hoverTip.classList.add('visible');
                    setActiveLegend(entry.cfg.name);
                } else {
                    hoverTip.classList.remove('visible');
                    setActiveLegend(focusedPlanet ? focusedPlanet.cfgName : null);
                }
            }
            if (entry) {
                hoverTip.style.left = clientX + 'px';
                hoverTip.style.top = clientY + 'px';
            }
        }

        function focusPlanet(planet, cfg) {
            focusedPlanet = planet;
            focusedPlanet.cfgName = cfg.name;
            targetRadius = Math.max(2.2, cfg.size * 7.5);
            infoName.textContent = cfg.name;
            infoDesc.textContent = cfg.desc;
            infoOrbit.textContent = cfg.orbit.toFixed(1) + ' AU';
            infoSize.textContent = cfg.size.toFixed(2) + 'x';
            infoClass.textContent = cfg.klass;
            infoPanel.classList.add('visible');
            hintEl.style.opacity = '0';
            setActiveLegend(cfg.name);
            spawnPing(planet.mesh.position, cfg.rimColor);
        }

        function defocus() {
            focusedPlanet = null;
            targetRadius = 13;
            infoPanel.classList.remove('visible');
            hintEl.style.opacity = '1';
            setActiveLegend(null);
        }
        infoClose.addEventListener('click', defocus);

        function handleClick(e) {
            const rect = canvas.getBoundingClientRect();
            ndc.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
            ndc.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
            raycaster.setFromCamera(ndc, camera);

            const planetMeshes = planets.map((p) => p.mesh);
            const hits = raycaster.intersectObjects(planetMeshes, true);
            if (hits.length > 0) {
                let obj = hits[0].object;
                while (obj && !meshToPlanet.has(obj)) obj = obj.parent;
                if (obj) {
                    const entry = meshToPlanet.get(obj);
                    focusPlanet(entry.planet, entry.cfg);
                    triggerPulse();
                    return;
                }
            }

            const horizonHit = raycaster.intersectObject(horizon, false);
            triggerPulse();
            if (horizonHit.length > 0) {
                defocus();
                return;
            }
            defocus();
        }

        // ================= SKYBOX: procedural high-res deep-space nebula =================
        function makeSpaceSkyboxTexture() {
            const w = 4096, h = 2048;
            const c = document.createElement('canvas');
            c.width = w; c.height = h;
            const ctx = c.getContext('2d');

            const base = ctx.createLinearGradient(0, 0, 0, h);
            base.addColorStop(0, '#02030a');
            base.addColorStop(0.5, '#04050f');
            base.addColorStop(1, '#020208');
            ctx.fillStyle = base;
            ctx.fillRect(0, 0, w, h);

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

            ctx.globalAlpha = 0.05;
            for (let i = 0; i < 6; i++) {
                ctx.strokeStyle = 'rgba(150,180,255,0.5)';
                ctx.lineWidth = 40 + Math.random() * 80;
                ctx.beginPath();
                const sy = Math.random() * h;
                ctx.moveTo(0, sy);
                ctx.bezierCurveTo(w * 0.3, sy + (Math.random() - 0.5) * 300, w * 0.7, sy + (Math.random() - 0.5) * 300, w, sy + (Math.random() - 0.5) * 200);
                ctx.stroke();
            }
            ctx.globalAlpha = 1.0;

            for (let i = 0; i < 9000; i++) {
                const x = Math.random() * w;
                const y = Math.random() * h;
                const b = Math.random();
                const size = b < 0.85 ? 0.7 : (b < 0.97 ? 1.3 : 2.0);
                const alpha = 0.25 + Math.random() * 0.55;
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

        // ================= GLOW HALO SPRITE =================
        function makeGlowTexture() {
            const size = 256;
            const c = document.createElement('canvas');
            c.width = c.height = size;
            const ctx = c.getContext('2d');
            const g = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
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

        // ================= EVENT HORIZON + PHOTON RING =================
        const horizonRadius = 1.5;
        const horizon = new THREE.Mesh(
            new THREE.SphereGeometry(horizonRadius, 96, 96),
            new THREE.MeshBasicMaterial({ color: 0x000000 })
        );
        scene.add(horizon);

        const rim = new THREE.Mesh(
            new THREE.SphereGeometry(horizonRadius * 1.06, 64, 64),
            new THREE.MeshBasicMaterial({
                color: 0x5f9fff, transparent: true, opacity: 0.4,
                side: THREE.BackSide, blending: THREE.AdditiveBlending, depthWrite: false
            })
        );
        scene.add(rim);

        const photonRing = new THREE.Mesh(
            new THREE.TorusGeometry(horizonRadius * 1.12, 0.015, 16, 128),
            new THREE.MeshBasicMaterial({
                color: 0xf0f8ff, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending, depthWrite: false
            })
        );
        scene.add(photonRing);

        // ================= ACCRETION DISK: turbulence, Doppler beaming, palette breathing, pulse =================
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
            uniform float uPulse;
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

                vec3 hotA = vec3(1.0, 0.98, 0.94);
                vec3 midA = vec3(0.78, 0.9, 1.0);
                vec3 blueA = vec3(0.22, 0.52, 1.0);
                vec3 deepA = vec3(0.02, 0.07, 0.28);

                vec3 hotB = vec3(1.0, 0.95, 0.99);
                vec3 midB = vec3(0.72, 0.78, 1.0);
                vec3 blueB = vec3(0.42, 0.32, 1.0);
                vec3 deepB = vec3(0.08, 0.03, 0.32);

                float pal = 0.5 + 0.5 * sin(uTime * 0.045);
                vec3 hot = mix(hotA, hotB, pal * 0.45);
                vec3 mid = mix(midA, midB, pal * 0.45);
                vec3 blue = mix(blueA, blueB, pal * 0.45);
                vec3 deep = mix(deepA, deepB, pal * 0.45);

                vec3 color = mix(hot, mid, smoothstep(0.0, 0.16, t));
                color = mix(color, blue, smoothstep(0.16, 0.52, t));
                color = mix(color, deep, smoothstep(0.52, 1.0, t));

                float beam = 0.5 + 0.5 * cos(angle - uTime * 0.5);
                color *= mix(0.55, 1.5, beam);
                color += uPulse * vec3(0.5, 0.7, 1.0) * (1.0 - t) * 0.8;

                float density = 0.35 + 0.65 * turb;
                float alpha = (1.0 - t) * density * uOpacity;
                alpha *= smoothstep(0.0, 0.06, t);
                alpha *= 1.0 - smoothstep(0.8, 1.0, t);

                gl_FragColor = vec4(color, alpha);
            }
        `;

        function makeDiskMaterial(inner, outer, baseOpacity) {
            const mat = new THREE.ShaderMaterial({
                uniforms: {
                    uTime: { value: 0 },
                    uInner: { value: inner },
                    uOuter: { value: outer },
                    uOpacity: { value: baseOpacity },
                    uPulse: { value: 0 }
                },
                vertexShader: diskVertex,
                fragmentShader: diskFragment,
                transparent: true,
                side: THREE.DoubleSide,
                blending: THREE.AdditiveBlending,
                depthWrite: false
            });
            mat.userData.baseOpacity = baseOpacity;
            return mat;
        }

        const innerR = horizonRadius * 1.28;
        const outerR = horizonRadius * 5.4;

        const diskMat = makeDiskMaterial(innerR, outerR, 1.0);
        const disk = new THREE.Mesh(new THREE.RingGeometry(innerR, outerR, 160, 10), diskMat);
        disk.rotation.x = Math.PI / 2.55;
        scene.add(disk);

        const haloMat = makeDiskMaterial(innerR * 0.92, outerR * 0.62, 0.55);
        const halo = new THREE.Mesh(new THREE.RingGeometry(innerR * 0.92, outerR * 0.62, 160, 8), haloMat);
        halo.rotation.x = Math.PI / 2 - 0.28;
        halo.rotation.z = Math.PI / 2;
        scene.add(halo);

        // ================= LIGHTING FOR PLANETS =================
        scene.add(new THREE.AmbientLight(0x1a2a4a, 0.55));
        const diskLight = new THREE.PointLight(0xbfe0ff, 2.4, 90, 2);
        diskLight.position.set(0, 0, 0);
        scene.add(diskLight);

        // ================= ORBIT PATH RINGS (faint guide trails) =================
        function makeOrbitRing(orbitRadius, color) {
            const points = [];
            const segments = 128;
            for (let i = 0; i <= segments; i++) {
                const a = (i / segments) * Math.PI * 2;
                points.push(new THREE.Vector3(orbitRadius * Math.cos(a), 0, orbitRadius * Math.sin(a)));
            }
            const geo = new THREE.BufferGeometry().setFromPoints(points);
            const mat = new THREE.LineBasicMaterial({
                color: color, transparent: true, opacity: 0.14
            });
            return new THREE.LineLoop(geo, mat);
        }

        // ================= REALISTIC PLANET TEXTURE GENERATORS =================
        // Terrain world: oceans, continents, polar caps, and a soft cloud layer.
        function makeTerrainPlanet(oceanColor, landColor, mountainColor, iceColor) {
            const w = 1024, h = 512;
            const mapC = document.createElement('canvas'); mapC.width = w; mapC.height = h;
            const bumpC = document.createElement('canvas'); bumpC.width = w; bumpC.height = h;
            const mctx = mapC.getContext('2d');
            const bctx = bumpC.getContext('2d');

            mctx.fillStyle = oceanColor; mctx.fillRect(0, 0, w, h);
            bctx.fillStyle = '#808080'; bctx.fillRect(0, 0, w, h);

            const continents = 7 + Math.floor(Math.random() * 4);
            for (let i = 0; i < continents; i++) {
                const cx = Math.random() * w;
                const cy = h * 0.18 + Math.random() * h * 0.64;
                const blobs = 16 + Math.floor(Math.random() * 12);
                mctx.fillStyle = landColor;
                bctx.fillStyle = '#b4b4b4';
                for (let j = 0; j < blobs; j++) {
                    const ang = Math.random() * Math.PI * 2;
                    const dist = Math.random() * 75;
                    const bx = cx + Math.cos(ang) * dist;
                    const by = cy + Math.sin(ang) * dist * 0.6;
                    const r = 16 + Math.random() * 36;
                    mctx.beginPath(); mctx.arc(bx, by, r, 0, Math.PI * 2); mctx.fill();
                    bctx.beginPath(); bctx.arc(bx, by, r, 0, Math.PI * 2); bctx.fill();
                }
            }

            for (let i = 0; i < 550; i++) {
                const x = Math.random() * w, y = Math.random() * h;
                const r = 1 + Math.random() * 4;
                mctx.globalAlpha = 0.06 + Math.random() * 0.12;
                mctx.fillStyle = mountainColor;
                mctx.beginPath(); mctx.arc(x, y, r, 0, Math.PI * 2); mctx.fill();
                bctx.globalAlpha = 0.15 + Math.random() * 0.2;
                bctx.fillStyle = Math.random() < 0.5 ? '#e2e2e2' : '#3c3c3c';
                bctx.beginPath(); bctx.arc(x, y, r * 1.6, 0, Math.PI * 2); bctx.fill();
            }
            mctx.globalAlpha = 1; bctx.globalAlpha = 1;

            const capTop = mctx.createLinearGradient(0, 0, 0, h * 0.12);
            capTop.addColorStop(0, iceColor); capTop.addColorStop(1, 'rgba(255,255,255,0)');
            mctx.fillStyle = capTop; mctx.fillRect(0, 0, w, h * 0.12);
            const capBot = mctx.createLinearGradient(0, h, 0, h * 0.88);
            capBot.addColorStop(0, iceColor); capBot.addColorStop(1, 'rgba(255,255,255,0)');
            mctx.fillStyle = capBot; mctx.fillRect(0, h * 0.88, w, h * 0.12);

            const cloudC = document.createElement('canvas'); cloudC.width = w; cloudC.height = h;
            const cctx = cloudC.getContext('2d');
            for (let i = 0; i < 45; i++) {
                const x = Math.random() * w, y = Math.random() * h;
                const r = 35 + Math.random() * 85;
                const g = cctx.createRadialGradient(x, y, 0, x, y, r);
                g.addColorStop(0, 'rgba(255,255,255,0.55)');
                g.addColorStop(1, 'rgba(255,255,255,0)');
                cctx.fillStyle = g;
                cctx.beginPath();
                cctx.ellipse(x, y, r, r * 0.5, Math.random() * Math.PI, 0, Math.PI * 2);
                cctx.fill();
            }

            const mapTex = new THREE.CanvasTexture(mapC);
            const bumpTex = new THREE.CanvasTexture(bumpC);
            const cloudTex = new THREE.CanvasTexture(cloudC);
            mapTex.anisotropy = 4; mapTex.needsUpdate = true;
            bumpTex.needsUpdate = true; cloudTex.needsUpdate = true;
            return { map: mapTex, bump: bumpTex, clouds: cloudTex };
        }

        // Cratered world: rocky/icy body pocked with impact craters.
        function makeCraterPlanet(baseColor, accentColor, craterCount) {
            const w = 1024, h = 512;
            const mapC = document.createElement('canvas'); mapC.width = w; mapC.height = h;
            const bumpC = document.createElement('canvas'); bumpC.width = w; bumpC.height = h;
            const mctx = mapC.getContext('2d');
            const bctx = bumpC.getContext('2d');

            mctx.fillStyle = baseColor; mctx.fillRect(0, 0, w, h);
            bctx.fillStyle = '#808080'; bctx.fillRect(0, 0, w, h);

            for (let i = 0; i < 650; i++) {
                const x = Math.random() * w, y = Math.random() * h;
                mctx.globalAlpha = 0.05 + Math.random() * 0.14;
                mctx.fillStyle = accentColor;
                const r = 2 + Math.random() * 10;
                mctx.beginPath(); mctx.arc(x, y, r, 0, Math.PI * 2); mctx.fill();
            }
            mctx.globalAlpha = 1;

            for (let i = 0; i < craterCount; i++) {
                const x = Math.random() * w, y = Math.random() * h;
                const r = 4 + Math.random() * 24;

                const mg = mctx.createRadialGradient(x, y, 0, x, y, r);
                mg.addColorStop(0, 'rgba(0,0,0,0.28)');
                mg.addColorStop(0.75, 'rgba(0,0,0,0.12)');
                mg.addColorStop(0.85, 'rgba(255,255,255,0.16)');
                mg.addColorStop(1, 'rgba(0,0,0,0)');
                mctx.fillStyle = mg;
                mctx.beginPath(); mctx.arc(x, y, r, 0, Math.PI * 2); mctx.fill();

                const bg = bctx.createRadialGradient(x, y, 0, x, y, r);
                bg.addColorStop(0, 'rgba(55,55,55,1)');
                bg.addColorStop(0.7, 'rgba(95,95,95,1)');
                bg.addColorStop(0.85, 'rgba(225,225,225,1)');
                bg.addColorStop(1, 'rgba(128,128,128,0)');
                bctx.fillStyle = bg;
                bctx.beginPath(); bctx.arc(x, y, r, 0, Math.PI * 2); bctx.fill();
            }

            const mapTex = new THREE.CanvasTexture(mapC);
            const bumpTex = new THREE.CanvasTexture(bumpC);
            mapTex.anisotropy = 4; mapTex.needsUpdate = true; bumpTex.needsUpdate = true;
            return { map: mapTex, bump: bumpTex, clouds: null };
        }

        // Gas giant: banded atmosphere with a great storm.
        function makeGasGiantPlanet(colors, stormColor) {
            const w = 1024, h = 512;
            const mapC = document.createElement('canvas'); mapC.width = w; mapC.height = h;
            const bumpC = document.createElement('canvas'); bumpC.width = w; bumpC.height = h;
            const mctx = mapC.getContext('2d');
            const bctx = bumpC.getContext('2d');

            const bands = 14;
            for (let i = 0; i < bands; i++) {
                mctx.fillStyle = colors[i % colors.length];
                const y0 = (h / bands) * i;
                mctx.fillRect(0, y0, w, h / bands + 2);
            }
            bctx.fillStyle = '#808080'; bctx.fillRect(0, 0, w, h);

            mctx.globalAlpha = 0.16;
            for (let i = 0; i < 75; i++) {
                mctx.strokeStyle = '#ffffff';
                mctx.lineWidth = 1 + Math.random() * 2;
                mctx.beginPath();
                const y = Math.random() * h;
                mctx.moveTo(0, y);
                mctx.bezierCurveTo(w * 0.3, y + (Math.random() - 0.5) * 22, w * 0.7, y + (Math.random() - 0.5) * 22, w, y + (Math.random() - 0.5) * 12);
                mctx.stroke();
            }
            mctx.globalAlpha = 1;

            const sx = w * (0.25 + Math.random() * 0.5), sy = h * (0.35 + Math.random() * 0.3);
            const sw = 75 + Math.random() * 40, sh = sw * 0.6;
            const sg = mctx.createRadialGradient(sx, sy, 0, sx, sy, sw);
            sg.addColorStop(0, stormColor);
            sg.addColorStop(1, 'rgba(0,0,0,0)');
            mctx.fillStyle = sg;
            mctx.beginPath(); mctx.ellipse(sx, sy, sw, sh, 0, 0, Math.PI * 2); mctx.fill();

            for (let i = 0; i < 320; i++) {
                const x = Math.random() * w, y = Math.random() * h;
                bctx.globalAlpha = 0.08 + Math.random() * 0.1;
                bctx.fillStyle = Math.random() < 0.5 ? '#a2a2a2' : '#5c5c5c';
                bctx.beginPath(); bctx.arc(x, y, 3 + Math.random() * 6, 0, Math.PI * 2); bctx.fill();
            }
            bctx.globalAlpha = 1;

            const mapTex = new THREE.CanvasTexture(mapC);
            const bumpTex = new THREE.CanvasTexture(bumpC);
            mapTex.anisotropy = 4; mapTex.needsUpdate = true; bumpTex.needsUpdate = true;
            return { map: mapTex, bump: bumpTex, clouds: null };
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

        // Each world now carries a `klass` label, its own texture recipe, an
        // optional cloud layer, optional rings, and an optional moon.
        const planetsConfig = [
            { name: 'Ember', desc: 'A scorched wanderer, forever circling too close to the light.',
              klass: 'Molten Rock', size: 0.55, orbit: 10.5, speed: 0.0055, tilt: 0.16, spin: 0.012,
              kind: 'crater', textureArgs: ['#8a4a3a', '#e0a06a', 420], rimColor: 0xff9a66 },
            { name: 'Azure', desc: 'Frozen oceans beneath a frostbitten, silent sky.',
              klass: 'Ocean World', size: 0.42, orbit: 12.8, speed: 0.0042, tilt: -0.1, spin: 0.014,
              kind: 'terrain', textureArgs: ['#2a5a8a', '#bcd9ff', '#dceeff', 'rgba(255,255,255,0.92)'], rimColor: 0x7fd0ff, moon: true },
            { name: 'Helios', desc: 'A giant crowned in stardust rings, drifting on ancient winds.',
              klass: 'Gas Giant', size: 1.0, orbit: 16.5, speed: 0.0026, tilt: 0.06, spin: 0.02,
              kind: 'gas', textureArgs: [['#dcc192', '#c8a06e', '#eed8ae', '#b8905c'], 'rgba(255,207,138,0.8)'], rimColor: 0xffe0ac, ring: true },
            { name: 'Verdant', desc: 'A world humming with borrowed light, teeming with quiet color.',
              klass: 'Living World', size: 0.5, orbit: 20, speed: 0.002, tilt: 0.22, spin: 0.009,
              kind: 'terrain', textureArgs: ['#1c4f63', '#4fae7c', '#8fe0a8', 'rgba(255,255,255,0.85)'], rimColor: 0x74f0c4 },
            { name: 'Luna', desc: 'The quiet one, drifting at the edge of the dark.',
              klass: 'Dead Moon', size: 0.22, orbit: 23, speed: 0.0016, tilt: -0.12, spin: 0.016,
              kind: 'crater', textureArgs: ['#7d7d7d', '#c2c2c2', 520], rimColor: 0xd6d6d6 }
        ];

        const planets = [];
        planetsConfig.forEach((cfg) => {
            let tex;
            if (cfg.kind === 'terrain') tex = makeTerrainPlanet(...cfg.textureArgs);
            else if (cfg.kind === 'gas') tex = makeGasGiantPlanet(...cfg.textureArgs);
            else tex = makeCraterPlanet(...cfg.textureArgs);

            const mat = new THREE.MeshStandardMaterial({
                map: tex.map,
                bumpMap: tex.bump,
                bumpScale: 0.035,
                roughness: cfg.kind === 'gas' ? 0.55 : 0.92,
                metalness: 0.04,
                emissive: new THREE.Color(cfg.rimColor),
                emissiveIntensity: 0.0
            });
            const mesh = new THREE.Mesh(new THREE.SphereGeometry(cfg.size, 48, 48), mat);
            mesh.rotation.z = cfg.tilt;
            scene.add(mesh);

            // soft drifting cloud layer for terrain worlds
            if (tex.clouds) {
                const cloudMat = new THREE.MeshBasicMaterial({
                    map: tex.clouds, transparent: true, opacity: 0.85, depthWrite: false
                });
                const cloudMesh = new THREE.Mesh(new THREE.SphereGeometry(cfg.size * 1.015, 48, 48), cloudMat);
                mesh.add(cloudMesh);
                mesh.userData.cloudMesh = cloudMesh;
            }

            const planetRim = new THREE.Mesh(
                new THREE.SphereGeometry(cfg.size * 1.16, 24, 24),
                new THREE.MeshBasicMaterial({
                    color: cfg.rimColor, transparent: true, opacity: 0.28,
                    side: THREE.BackSide, blending: THREE.AdditiveBlending, depthWrite: false
                })
            );
            mesh.add(planetRim);
            mesh.userData.rimMesh = planetRim;

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
                const ringMesh = new THREE.Mesh(new THREE.RingGeometry(cfg.size * 1.4, cfg.size * 2.3, 96, 4), ringMat);
                ringMesh.rotation.x = Math.PI / 2.3;
                mesh.add(ringMesh);
            }

            // a small companion moon for extra visual interest / interactivity
            let moonMesh = null, moonAngle = 0;
            if (cfg.moon) {
                const moonTex = makeCraterPlanet('#9a9a9a', '#d5d5d5', 180);
                const moonMat = new THREE.MeshStandardMaterial({
                    map: moonTex.map, bumpMap: moonTex.bump, bumpScale: 0.02, roughness: 0.95
                });
                moonMesh = new THREE.Mesh(new THREE.SphereGeometry(cfg.size * 0.28, 24, 24), moonMat);
                mesh.add(moonMesh);
            }

            // faint guide ring showing this planet's orbital path
            const orbitLine = makeOrbitRing(cfg.orbit, cfg.rimColor);
            scene.add(orbitLine);

            const planetEntry = {
                mesh: mesh,
                orbit: cfg.orbit,
                speed: cfg.speed,
                angle: Math.random() * Math.PI * 2,
                tilt: cfg.tilt,
                spin: cfg.spin,
                baseScale: 1,
                moonMesh: moonMesh,
                moonAngle: Math.random() * Math.PI * 2
            };
            planets.push(planetEntry);
            meshToPlanet.set(mesh, { planet: planetEntry, cfg: cfg });

            // legend entry so users can also jump to a world without hunting for it
            const item = document.createElement('div');
            item.className = 'legend-item';
            item.dataset.name = cfg.name;
            item.innerHTML = '<span class="legend-dot" style="color:#' + cfg.rimColor.toString(16).padStart(6, '0') + '"></span>' + cfg.name;
            item.addEventListener('click', () => {
                focusPlanet(planetEntry, cfg);
                triggerPulse();
            });
            item.addEventListener('mouseenter', () => setActiveLegend(cfg.name));
            item.addEventListener('mouseleave', () => setActiveLegend(focusedPlanet ? focusedPlanet.cfgName : null));
            legendEl.appendChild(item);
        });

        function setActiveLegend(name) {
            const items = legendEl.querySelectorAll('.legend-item');
            items.forEach((it) => it.classList.toggle('active', it.dataset.name === name));
        }

        // ================= "PING" - a quick expanding ring shown on interaction =================
        const pings = [];
        function spawnPing(position, color) {
            const geo = new THREE.RingGeometry(0.01, 0.05, 48);
            const mat = new THREE.MeshBasicMaterial({
                color: color, transparent: true, opacity: 0.9,
                side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false
            });
            const mesh = new THREE.Mesh(geo, mat);
            mesh.position.copy(position);
            mesh.lookAt(camera.position);
            scene.add(mesh);
            pings.push({ mesh: mesh, birth: clock.getElapsedTime() });
        }

        // ================= ORBITING SPARKLE PARTICLES WITHIN THE DISK =================
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

        // ================= INFALLING MATTER: streaks spiraling into the horizon =================
        const infallCount = 260;
        const infallGeo = new THREE.BufferGeometry();
        const infallPos = new Float32Array(infallCount * 3);
        const infallData = [];
        function resetInfall(d) {
            d.r = outerR * (0.8 + Math.random() * 0.9);
            d.a = Math.random() * Math.PI * 2;
            d.fallSpeed = 0.01 + Math.random() * 0.02;
            d.spinSpeed = 0.01 + Math.random() * 0.02;
            d.y = (Math.random() - 0.5) * 0.3;
        }
        for (let i = 0; i < infallCount; i++) {
            const d = {};
            resetInfall(d);
            infallData.push(d);
            infallPos[i * 3] = d.r * Math.cos(d.a);
            infallPos[i * 3 + 1] = d.y;
            infallPos[i * 3 + 2] = d.r * Math.sin(d.a);
        }
        infallGeo.setAttribute('position', new THREE.BufferAttribute(infallPos, 3));
        const infallMat = new THREE.PointsMaterial({
            color: 0xaad4ff, size: 0.06, transparent: true, opacity: 0.85,
            blending: THREE.AdditiveBlending, depthWrite: false
        });
        const infall = new THREE.Points(infallGeo, infallMat);
        infall.rotation.x = Math.PI / 2.55;
        scene.add(infall);

        // ================= POST-PROCESS: gravitational lensing + bloom =================
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

        // ================= ANIMATE =================
        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);
            const t = clock.getElapsedTime();

            const pulseAge = t - pulseStart;
            const pulse = pulseAge >= 0 ? Math.exp(-pulseAge * 3.0) : 0;

            diskMat.uniforms.uTime.value = t;
            diskMat.uniforms.uPulse.value = pulse;
            diskMat.uniforms.uOpacity.value = diskMat.userData.baseOpacity * (0.9 + 0.1 * Math.sin(t * 0.7)) + pulse * 0.3;

            haloMat.uniforms.uTime.value = t * 0.8;
            haloMat.uniforms.uPulse.value = pulse * 0.7;
            haloMat.uniforms.uOpacity.value = haloMat.userData.baseOpacity * (0.9 + 0.1 * Math.sin(t * 0.7 + 1.0)) + pulse * 0.2;

            disk.rotation.z += 0.0015;
            halo.rotation.y += 0.0009;

            rim.material.opacity = 0.4 + pulse * 0.5;
            photonRing.material.opacity = 0.95 * (0.85 + 0.15 * Math.sin(t * 1.4)) + pulse * 0.1;

            const posAttr = particleGeo.attributes.position;
            for (let i = 0; i < particleCount; i++) {
                const d = particleData[i];
                d.a += d.speed * 0.02;
                posAttr.array[i * 3] = d.r * Math.cos(d.a);
                posAttr.array[i * 3 + 2] = d.r * Math.sin(d.a);
            }
            posAttr.needsUpdate = true;

            const infallAttr = infallGeo.attributes.position;
            for (let i = 0; i < infallCount; i++) {
                const d = infallData[i];
                d.r -= d.fallSpeed;
                d.a += d.spinSpeed * (outerR / Math.max(d.r, 0.5)) * 0.03;
                if (d.r < innerR * 1.05) resetInfall(d);
                infallAttr.array[i * 3] = d.r * Math.cos(d.a);
                infallAttr.array[i * 3 + 1] = d.y * (d.r / outerR);
                infallAttr.array[i * 3 + 2] = d.r * Math.sin(d.a);
            }
            infallAttr.needsUpdate = true;

            glowSprite.scale.setScalar(10 + Math.sin(t * 0.6) * 0.35 + pulse * 1.2);

            planets.forEach((p) => {
                p.angle += p.speed;
                const x = p.orbit * Math.cos(p.angle);
                const z = p.orbit * Math.sin(p.angle);
                const y = Math.sin(p.angle * 0.5) * p.orbit * Math.sin(p.tilt);
                p.mesh.position.set(x, y, z);
                p.mesh.rotation.y += p.spin;

                if (p.mesh.userData.cloudMesh) {
                    p.mesh.userData.cloudMesh.rotation.y += p.spin * 0.4;
                }

                // gentle interactive feedback: glow + slight scale-up on hover/focus
                const entry = meshToPlanet.get(p.mesh);
                const isHovered = hoveredEntry && hoveredEntry.planet === p;
                const isFocused = focusedPlanet === p;
                const targetEmissive = (isHovered || isFocused) ? (isFocused ? 0.55 : 0.32) : 0.0;
                const targetScale = (isHovered || isFocused) ? 1.12 : 1.0;
                p.mesh.material.emissiveIntensity += (targetEmissive - p.mesh.material.emissiveIntensity) * 0.12;
                p.baseScale += (targetScale - p.baseScale) * 0.12;
                p.mesh.scale.setScalar(p.baseScale);
                if (p.mesh.userData.rimMesh) {
                    p.mesh.userData.rimMesh.material.opacity = 0.28 + (isHovered || isFocused ? 0.35 : 0) * (0.7 + 0.3 * Math.sin(t * 3));
                }

                if (p.moonMesh) {
                    p.moonAngle += p.speed * 6.0;
                    const moonOrbitR = p.mesh.geometry.parameters.radius * 2.6;
                    p.moonMesh.position.set(
                        moonOrbitR * Math.cos(p.moonAngle),
                        Math.sin(p.moonAngle * 1.7) * 0.15,
                        moonOrbitR * Math.sin(p.moonAngle)
                    );
                    p.moonMesh.rotation.y += 0.01;
                }
            });

            for (let i = pings.length - 1; i >= 0; i--) {
                const ping = pings[i];
                const age = t - ping.birth;
                if (age > 1.2) {
                    scene.remove(ping.mesh);
                    pings.splice(i, 1);
                    continue;
                }
                const scale = 0.3 + age * 3.5;
                ping.mesh.scale.setScalar(scale);
                ping.mesh.material.opacity = 0.9 * (1.0 - age / 1.2);
                ping.mesh.lookAt(camera.position);
            }

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
