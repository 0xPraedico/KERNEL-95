"""Self-contained Three.js MIRROR Core with a CSS-only fallback."""

from __future__ import annotations

import html
import uuid


def render_mirror_core_html(
    trust: int,
    corruption: int,
    status: str = "UNRELIABLE",
    secret_unlocked: bool = False,
) -> str:
    """Return a responsive, optional WebGL visual that never blocks gameplay."""
    trust = max(0, min(100, int(trust)))
    corruption = max(0, min(100, int(corruption)))
    visual_id = f"mirror-core-{uuid.uuid4().hex}"
    if trust >= 70:
        primary, secondary = "#55f5ff", "#ff2da6"
    elif trust < 35:
        primary, secondary = "#ff3b6b", "#ff2da6"
    else:
        primary, secondary = "#ff2da6", "#55f5ff"
    secret_label = (
        '<div class="mirror-core-alert">SUPPRESSED MEMORY DETECTED</div>'
        if secret_unlocked
        else ""
    )
    safe_status = html.escape(status.upper())

    return f"""
<div id="{visual_id}" class="mirror-core-shell"
     data-trust="{trust}" data-corruption="{corruption}"
     style="--core-primary:{primary};--core-secondary:{secondary}">
  <div class="mirror-core-fallback" aria-hidden="true">
    <div class="fallback-ring fallback-ring-a"></div>
    <div class="fallback-ring fallback-ring-b"></div>
    <div class="fallback-orb"></div>
    <div class="fallback-fragments"></div>
  </div>
  <canvas class="mirror-core-canvas" aria-label="Animated MIRROR AI core"></canvas>
  <div class="mirror-core-scanlines"></div>
  <div class="mirror-core-hud">
    <span>MIRROR CORE // {safe_status}</span>
    <span>TRUST {trust:02d} // CORRUPTION {corruption:02d}</span>
  </div>
  {secret_label}
</div>
<script>
(() => {{
  "use strict";
  const rootId = "{visual_id}";
  const CDN = "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js";
  window.NeonTraceMirror = window.NeonTraceMirror || {{
    loading: null,
    instances: new Map()
  }};
  const ns = window.NeonTraceMirror;

  function loadThree() {{
    if (window.THREE) return Promise.resolve(window.THREE);
    if (ns.loading) return ns.loading;
    ns.loading = new Promise((resolve, reject) => {{
      const script = document.createElement("script");
      script.src = CDN;
      script.async = true;
      script.onload = () => window.THREE ? resolve(window.THREE) : reject(new Error("THREE missing"));
      script.onerror = () => reject(new Error("Three.js CDN unavailable"));
      document.head.appendChild(script);
    }});
    return ns.loading;
  }}

  function init() {{
    const root = document.getElementById(rootId);
    if (!root || root.dataset.initialized === "true") return;
    root.dataset.initialized = "true";
    loadThree().then((THREE) => {{
      if (!root.isConnected) return;
      const canvas = root.querySelector(".mirror-core-canvas");
      let renderer;
      try {{
        renderer = new THREE.WebGLRenderer({{
          canvas,
          alpha: true,
          antialias: true,
          powerPreference: "low-power"
        }});
      }} catch (_) {{
        root.dataset.webgl = "failed";
        return;
      }}

      const trust = Number(root.dataset.trust || 50);
      const corruption = Number(root.dataset.corruption || 0);
      const primary = new THREE.Color(getComputedStyle(root).getPropertyValue("--core-primary").trim());
      const secondary = new THREE.Color(getComputedStyle(root).getPropertyValue("--core-secondary").trim());
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(46, 1, 0.1, 100);
      camera.position.set(0, 1.1, 7.4);
      camera.lookAt(0, 0.2, 0);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.6));
      renderer.setClearColor(0x000000, 0);

      const core = new THREE.Mesh(
        new THREE.IcosahedronGeometry(1.05, 2),
        new THREE.MeshBasicMaterial({{
          color: primary,
          wireframe: true,
          transparent: true,
          opacity: 0.82
        }})
      );
      scene.add(core);

      const inner = new THREE.Mesh(
        new THREE.IcosahedronGeometry(0.68, 1),
        new THREE.MeshBasicMaterial({{
          color: secondary,
          transparent: true,
          opacity: 0.22,
          blending: THREE.AdditiveBlending,
          depthWrite: false
        }})
      );
      scene.add(inner);

      const rings = [];
      [
        [1.65, 0.018, 0.3, 0.2],
        [2.0, 0.014, 1.2, -0.6],
        [2.38, 0.012, -0.7, 0.8]
      ].forEach((spec, index) => {{
        const ring = new THREE.Mesh(
          new THREE.TorusGeometry(spec[0], spec[1], 8, 100),
          new THREE.MeshBasicMaterial({{
            color: index === 1 ? secondary : primary,
            transparent: true,
            opacity: 0.64,
            blending: THREE.AdditiveBlending
          }})
        );
        ring.rotation.x = spec[2];
        ring.rotation.y = spec[3];
        rings.push(ring);
        scene.add(ring);
      }});

      const count = 110;
      const positions = new Float32Array(count * 3);
      for (let i = 0; i < count; i += 1) {{
        const radius = 2.2 + Math.random() * 2.5;
        const angle = Math.random() * Math.PI * 2;
        positions[i * 3] = Math.cos(angle) * radius;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 4.5;
        positions[i * 3 + 2] = Math.sin(angle) * radius * 0.42;
      }}
      const particleGeometry = new THREE.BufferGeometry();
      particleGeometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
      const particles = new THREE.Points(
        particleGeometry,
        new THREE.PointsMaterial({{
          color: secondary,
          size: 0.035 + corruption * 0.00025,
          transparent: true,
          opacity: 0.62,
          blending: THREE.AdditiveBlending,
          depthWrite: false
        }})
      );
      scene.add(particles);

      const grid = new THREE.GridHelper(11, 22, primary, secondary);
      grid.position.y = -2.15;
      grid.rotation.x = 0.04;
      grid.material.transparent = true;
      grid.material.opacity = 0.14;
      scene.add(grid);

      let frame = 0;
      let stopped = false;
      const clock = new THREE.Clock();
      const glitch = Math.max((45 - trust) / 45, corruption / 100);

      function resize() {{
        if (!root.isConnected) return;
        const width = Math.max(1, root.clientWidth);
        const height = Math.max(1, root.clientHeight);
        renderer.setSize(width, height, false);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
      }}

      function animate() {{
        if (stopped || !root.isConnected) {{
          stopped = true;
          renderer.dispose();
          particleGeometry.dispose();
          ns.instances.delete(rootId);
          return;
        }}
        frame = requestAnimationFrame(animate);
        const t = clock.getElapsedTime();
        core.rotation.x = t * 0.18;
        core.rotation.y = t * 0.25;
        inner.rotation.x = -t * 0.3;
        inner.rotation.z = t * 0.22;
        rings[0].rotation.z = t * 0.22;
        rings[1].rotation.z = -t * 0.16;
        rings[2].rotation.y = t * 0.12;
        particles.rotation.y = t * (0.035 + corruption * 0.00045);
        particles.material.opacity = 0.5 + Math.sin(t * (2 + corruption * 0.035)) * 0.16;
        core.scale.setScalar(1 + Math.sin(t * 1.7) * 0.035);
        if (glitch > 0.45 && Math.sin(t * 13.0) > 0.965) {{
          core.position.x = (Math.random() - 0.5) * glitch * 0.22;
          rings[1].position.y = (Math.random() - 0.5) * glitch * 0.14;
        }} else {{
          core.position.x *= 0.8;
          rings[1].position.y *= 0.8;
        }}
        renderer.render(scene, camera);
      }}

      const observer = new ResizeObserver(resize);
      observer.observe(root);
      resize();
      root.classList.add("webgl-ready");
      animate();
      ns.instances.set(rootId, {{
        stop: () => {{
          stopped = true;
          cancelAnimationFrame(frame);
          observer.disconnect();
          renderer.dispose();
        }}
      }});
    }}).catch(() => {{
      const root = document.getElementById(rootId);
      if (root) root.dataset.webgl = "fallback";
    }});
  }}

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", init, {{ once: true }});
  }} else {{
    requestAnimationFrame(init);
  }}
}})();
</script>
"""
