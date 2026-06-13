"""Dominant Three.js MetroGrid Sector 7 gameplay scene."""

from __future__ import annotations

import html
import json
import uuid

from .game_data import EVIDENCE_NAME_BY_ID, GAME_OBJECTS
from .game_state import GameState

THREEJS_GAME_BOOTSTRAP = r"""
() => {
  "use strict";
  const executeSceneScripts = () => {
    document.querySelectorAll(".sector7-game + script:not([data-neon-executed])").forEach((source) => {
      source.dataset.kernel95Executed = "true";
      const runtime = document.createElement("script");
      runtime.dataset.kernel95Runtime = "true";
      runtime.textContent = source.textContent;
      document.body.appendChild(runtime);
      runtime.remove();
    });
  };
  executeSceneScripts();
  if (window.Kernel95ThreeBootstrap && window.Kernel95ThreeBootstrap.observer) {
    window.Kernel95ThreeBootstrap.observer.disconnect();
  }
  const observer = new MutationObserver(executeSceneScripts);
  observer.observe(document.body, { childList: true, subtree: true });
  window.Kernel95ThreeBootstrap = { observer, executeSceneScripts };
}
"""


def _minimal_state(state: GameState, selected_object: str) -> dict[str, object]:
    return {
        "trust": state.trust,
        "corruption": state.corruption,
        "discovered_clues": state.discovered_clues,
        "contradictions": [item.get("id") for item in state.known_contradictions],
        "analyzed_evidence": [
            next(
                (
                    evidence_id
                    for evidence_id, name in EVIDENCE_NAME_BY_ID.items()
                    if name == evidence_name
                ),
                evidence_name,
            )
            for evidence_name in state.analyzed_evidence
        ],
        "selected_object": selected_object,
        "suspect_stress": state.suspect_stress,
        "secret_unlocked": state.secret_unlocked,
        "memory_vault_unlocked": state.memory_vault_unlocked,
        "mirror_memory_audit_unlocked": state.mirror_memory_audit_unlocked,
        "duplicate_j17": "duplicate_token" in state.discovered_clues,
    }


def render_threejs_game(state: GameState, selected_object: str | None = None) -> str:
    """Render the interactive 3D crime scene plus an accessible fallback map."""
    selected = selected_object or state.selected_3d_object or "evidence_sector_log"
    if selected not in GAME_OBJECTS:
        selected = "evidence_sector_log"
    render_id = f"kernel95-3d-{uuid.uuid4().hex}"
    scene_state = _minimal_state(state, selected)
    visible_objects = {
        object_id: item
        for object_id, item in GAME_OBJECTS.items()
        if object_id != "evidence_suppressed" or state.secret_unlocked
    }
    objects_json = json.dumps(visible_objects, separators=(",", ":")).replace("</", "<\\/")
    state_json = json.dumps(scene_state, separators=(",", ":")).replace("</", "<\\/")
    selected_label = str(GAME_OBJECTS[selected]["label"])
    fallback_buttons = "".join(
        (
            f'<button type="button" class="fallback-hotspot{" is-selected" if object_id == selected else ""}" '
            f'data-object-id="{html.escape(object_id)}">'
            f'<span>{html.escape(str(item["type"]))}</span>'
            f"<strong>{html.escape(str(item['label']))}</strong></button>"
        )
        for object_id, item in visible_objects.items()
    )

    return f"""
<div id="{render_id}" class="sector7-game" data-selected="{html.escape(selected)}">
  <div class="sector7-canvas-mount"></div>
  <div class="sector7-label-layer" aria-hidden="true"></div>
  <div class="sector7-reticle" aria-hidden="true"><span></span></div>
  <div class="sector7-top-hud">
    <div><strong>METROGRID // SECTOR 7</strong><span>DATA CRIME SCENE</span></div>
    <div class="sector7-signal">LIVE FORENSIC LINK</div>
  </div>
  <div class="sector7-selected-hud">
    <span>SELECTED OBJECT</span>
    <strong>{html.escape(selected_label)}</strong>
    <small>DRAG TO ORBIT // WHEEL TO ZOOM // CLICK TO SELECT</small>
  </div>
  <div class="sector7-token-alert" {"hidden" if not scene_state["duplicate_j17"] else ""}>
    J-17 // SAME TIMESTAMP // TWO LOCATIONS
  </div>
  <div class="sector7-fallback">
    <div class="fallback-warning">3D renderer unavailable. Tactical fallback mode active.</div>
    <div class="fallback-map">{fallback_buttons}</div>
  </div>
</div>
<script>
(() => {{
  "use strict";
  const rootId = "{render_id}";
  const objectsData = {objects_json};
  const gameState = {state_json};
  const CDN = "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js";
  window.Kernel95Three = window.Kernel95Three || {{ currentInstance: null, loading: null }};
  const ns = window.Kernel95Three;

  function findBridge() {{
    const selectors = [
      "#scene_object_bridge textarea",
      "#scene_object_bridge input",
      "textarea#scene_object_bridge",
      "input#scene_object_bridge"
    ];
    for (const selector of selectors) {{
      const direct = document.querySelector(selector);
      if (direct) return direct;
    }}
    const app = document.querySelector("gradio-app");
    const scope = app && app.shadowRoot;
    if (scope) {{
      for (const selector of selectors) {{
        const found = scope.querySelector(selector);
        if (found) return found;
      }}
    }}
    return null;
  }}

  function sendSelection(objectId) {{
    const bridge = findBridge();
    if (!bridge) return false;
    const proto = bridge.tagName === "TEXTAREA"
      ? window.HTMLTextAreaElement.prototype
      : window.HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
    setter.call(bridge, objectId);
    bridge.dispatchEvent(new InputEvent("input", {{
      bubbles: true,
      composed: true,
      inputType: "insertText",
      data: objectId
    }}));
    bridge.dispatchEvent(new Event("change", {{ bubbles: true, composed: true }}));
    return true;
  }}

  function updateLocalHud(objectId) {{
    const data = objectsData[objectId];
    if (!data) return;
    const title = document.querySelector(".hud-selected h3");
    const description = document.querySelector(".hud-selected p");
    const type = document.querySelector(".hud-selected > span");
    if (title) title.textContent = data.label;
    if (description) description.textContent = data.description || "No description recovered.";
    if (type) type.textContent = `SELECTED // ${{String(data.type).toUpperCase()}}`;
  }}

  function loadThree() {{
    if (window.THREE) return Promise.resolve(window.THREE);
    if (ns.loading) return ns.loading;
    ns.loading = new Promise((resolve, reject) => {{
      const script = document.createElement("script");
      script.src = CDN;
      script.async = true;
      script.onload = () => window.THREE ? resolve(window.THREE) : reject(new Error("THREE missing"));
      script.onerror = () => reject(new Error("Three.js unavailable"));
      document.head.appendChild(script);
    }});
    return ns.loading;
  }}

  function boot() {{
    const root = document.getElementById(rootId);
    if (!root || root.dataset.initialized === "true") return;
    root.dataset.initialized = "true";

    root.querySelectorAll(".fallback-hotspot").forEach((button) => {{
      button.addEventListener("click", () => {{
        const objectId = button.dataset.objectId;
        root.dataset.selected = objectId;
        root.querySelectorAll(".fallback-hotspot").forEach((item) => item.classList.remove("is-selected"));
        button.classList.add("is-selected");
        const label = objectsData[objectId] ? objectsData[objectId].label : objectId;
        root.querySelector(".sector7-selected-hud strong").textContent = label;
        updateLocalHud(objectId);
        sendSelection(objectId);
      }});
    }});

    loadThree().then((THREE) => {{
      if (!root.isConnected) return;
      if (ns.currentInstance && ns.currentInstance.stop) ns.currentInstance.stop();

      const mount = root.querySelector(".sector7-canvas-mount");
      const labelLayer = root.querySelector(".sector7-label-layer");
      let renderer;
      try {{
        renderer = new THREE.WebGLRenderer({{
          alpha: true,
          antialias: true,
          powerPreference: "high-performance"
        }});
      }} catch (_) {{
        root.dataset.renderer = "fallback";
        return;
      }}
      mount.appendChild(renderer.domElement);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.65));
      renderer.setClearColor(0x030106, 1);

      const scene = new THREE.Scene();
      scene.fog = new THREE.FogExp2(0x08020d, 0.032);
      const camera = new THREE.PerspectiveCamera(54, 1, 0.1, 100);
      let yaw = 0;
      let pitch = 0.29;
      let distance = 16.5;
      const target = new THREE.Vector3(0, 1.1, -0.8);
      const raycaster = new THREE.Raycaster();
      const pointer = new THREE.Vector2();
      const interactive = [];
      const objectMap = new Map();
      const labels = new Map();
      const magenta = new THREE.Color(0xff2da6);
      const violet = new THREE.Color(0x7c3cff);
      const cyan = new THREE.Color(0x55f5ff);
      const danger = new THREE.Color(0xff3b6b);
      let selectedId = gameState.selected_object;
      let hovered = null;
      let dragging = false;
      let moved = false;
      let lastX = 0;
      let lastY = 0;
      let frame = 0;
      let stopped = false;

      scene.add(new THREE.AmbientLight(0x5f174f, 1.35));
      const cyanLight = new THREE.PointLight(0x55f5ff, 26, 18);
      cyanLight.position.set(-5, 6, 3);
      scene.add(cyanLight);
      const pinkLight = new THREE.PointLight(0xff2da6, 34, 20);
      pinkLight.position.set(5, 5, -4);
      scene.add(pinkLight);

      const floor = new THREE.GridHelper(28, 40, 0xff2da6, 0x431139);
      floor.material.transparent = true;
      floor.material.opacity = 0.44;
      scene.add(floor);
      const lowerGrid = new THREE.GridHelper(28, 14, 0x55f5ff, 0x181126);
      lowerGrid.position.y = 0.012;
      lowerGrid.material.transparent = true;
      lowerGrid.material.opacity = 0.12;
      scene.add(lowerGrid);

      const room = new THREE.Group();
      for (let side = -1; side <= 1; side += 2) {{
        for (let z = -5; z <= 4; z += 2.2) {{
          const rack = new THREE.Mesh(
            new THREE.BoxGeometry(0.7, 3.2, 1.35),
            new THREE.MeshStandardMaterial({{
              color: 0x0b0710,
              emissive: side < 0 ? 0x40103c : 0x082d34,
              emissiveIntensity: 0.5,
              metalness: 0.75,
              roughness: 0.36,
              wireframe: false
            }})
          );
          rack.position.set(side * 7.6, 1.6, z);
          room.add(rack);
        }}
      }}
      scene.add(room);

      const particleCount = 260;
      const particlePositions = new Float32Array(particleCount * 3);
      for (let i = 0; i < particleCount; i += 1) {{
        particlePositions[i * 3] = (Math.random() - 0.5) * 24;
        particlePositions[i * 3 + 1] = Math.random() * 7;
        particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 18;
      }}
      const particleGeometry = new THREE.BufferGeometry();
      particleGeometry.setAttribute("position", new THREE.BufferAttribute(particlePositions, 3));
      const particles = new THREE.Points(
        particleGeometry,
        new THREE.PointsMaterial({{
          color: gameState.corruption > 55 ? danger : magenta,
          size: 0.045 + gameState.corruption * 0.0003,
          transparent: true,
          opacity: 0.55,
          blending: THREE.AdditiveBlending,
          depthWrite: false
        }})
      );
      scene.add(particles);

      function neonMaterial(color, opacity = 0.78, wireframe = true) {{
        return new THREE.MeshStandardMaterial({{
          color,
          emissive: color,
          emissiveIntensity: 1.2,
          transparent: true,
          opacity,
          wireframe,
          metalness: 0.35,
          roughness: 0.22
        }});
      }}

      function makeLabel(objectId, label) {{
        const element = document.createElement("button");
        element.type = "button";
        element.className = "sector7-world-label";
        element.textContent = label;
        element.dataset.objectId = objectId;
        element.addEventListener("click", (event) => {{
          event.stopPropagation();
          selectObject(objectId, true);
        }});
        labelLayer.appendChild(element);
        labels.set(objectId, element);
      }}

      function register(objectId, group) {{
        group.userData.objectId = objectId;
        group.traverse((child) => {{
          if (child.isMesh) {{
            child.userData.objectId = objectId;
            interactive.push(child);
          }}
        }});
        objectMap.set(objectId, group);
        scene.add(group);
        makeLabel(objectId, objectsData[objectId].label);
      }}

      function evidenceNode(objectId, data, analyzed) {{
        const group = new THREE.Group();
        const color = analyzed ? cyan : magenta;
        const shard = new THREE.Mesh(
          new THREE.OctahedronGeometry(0.5, 0),
          neonMaterial(color, analyzed ? 0.92 : 0.55, true)
        );
        const ring = new THREE.Mesh(
          new THREE.TorusGeometry(0.72, 0.025, 6, 48),
          neonMaterial(analyzed ? cyan : violet, 0.72, false)
        );
        ring.rotation.x = Math.PI / 2;
        group.add(shard, ring);
        group.userData.kind = "evidence";
        group.userData.baseY = data.position[1];
        return group;
      }}

      function suspectHologram(objectId, data) {{
        const group = new THREE.Group();
        const stress = Number(gameState.suspect_stress[data.suspect_id] || 0);
        const color = stress > 55 ? danger : violet;
        const torso = new THREE.Mesh(
          new THREE.CylinderGeometry(0.34, 0.56, 1.25, 10, 1, true),
          neonMaterial(color, 0.5, true)
        );
        torso.position.y = 0.65;
        const head = new THREE.Mesh(
          new THREE.IcosahedronGeometry(0.34, 1),
          neonMaterial(stress > 70 ? danger : cyan, 0.65, true)
        );
        head.position.y = 1.55;
        const base = new THREE.Mesh(
          new THREE.CylinderGeometry(0.8, 0.8, 0.05, 36),
          neonMaterial(color, 0.5, false)
        );
        group.add(torso, head, base);
        group.userData.kind = "suspect";
        group.userData.stress = stress;
        group.userData.baseY = data.position[1];
        return group;
      }}

      function mirrorCore(data) {{
        const group = new THREE.Group();
        const trust = Number(gameState.trust);
        const corruption = Number(gameState.corruption);
        const coreColor = trust >= 70 ? cyan : trust < 35 ? danger : magenta;
        const core = new THREE.Mesh(
          new THREE.IcosahedronGeometry(0.86, 2),
          neonMaterial(coreColor, 0.9, true)
        );
        group.add(core);
        for (let i = 0; i < 3; i += 1) {{
          const ring = new THREE.Mesh(
            new THREE.TorusGeometry(1.2 + i * 0.25, 0.022, 6, 80),
            neonMaterial(i === 1 ? cyan : magenta, 0.7, false)
          );
          ring.rotation.x = i * 0.75 + 0.35;
          ring.rotation.y = i * 0.55;
          ring.userData.coreRing = i;
          group.add(ring);
        }}
        group.userData.kind = "core";
        group.userData.corruption = corruption;
        group.userData.baseY = data.position[1];
        return group;
      }}

      function terminalConsole(data) {{
        const group = new THREE.Group();
        const base = new THREE.Mesh(
          new THREE.BoxGeometry(2.0, 0.82, 1.1),
          new THREE.MeshStandardMaterial({{
            color: 0x09050d,
            emissive: 0x063a42,
            emissiveIntensity: 0.8,
            metalness: 0.8,
            roughness: 0.3
          }})
        );
        const screen = new THREE.Mesh(
          new THREE.PlaneGeometry(1.55, 0.58),
          neonMaterial(cyan, 0.72, false)
        );
        screen.position.set(0, 0.35, -0.56);
        screen.rotation.x = -0.18;
        group.add(base, screen);
        group.userData.kind = "terminal";
        group.userData.baseY = data.position[1];
        return group;
      }}

      function memoryVault(data) {{
        const group = new THREE.Group();
        const open = Boolean(gameState.memory_vault_unlocked);
        const color = gameState.secret_unlocked ? danger : open ? cyan : magenta;
        const left = new THREE.Mesh(new THREE.BoxGeometry(1.25, 2.5, 0.5), neonMaterial(color, 0.62, true));
        const right = left.clone();
        left.position.x = open ? -0.95 : -0.62;
        right.position.x = open ? 0.95 : 0.62;
        if (open) {{
          left.rotation.y = -0.4;
          right.rotation.y = 0.4;
        }}
        const seal = new THREE.Mesh(
          new THREE.TorusGeometry(0.42, 0.08, 8, 36),
          neonMaterial(color, 0.9, false)
        );
        seal.position.z = 0.32;
        group.add(left, right, seal);
        group.userData.kind = "vault";
        group.userData.baseY = data.position[1];
        return group;
      }}

      function smileArtifact(data) {{
        const group = new THREE.Group();
        const ring = new THREE.Mesh(
          new THREE.TorusGeometry(0.58, 0.055, 8, 56),
          neonMaterial(danger, 0.85, false)
        );
        const eyeGeometry = new THREE.SphereGeometry(0.07, 10, 10);
        const eyeA = new THREE.Mesh(eyeGeometry, neonMaterial(cyan, 0.9, false));
        const eyeB = eyeA.clone();
        eyeA.position.set(-0.2, 0.14, 0.08);
        eyeB.position.set(0.2, 0.14, 0.08);
        const smile = new THREE.Mesh(
          new THREE.TorusGeometry(0.3, 0.035, 6, 28, Math.PI),
          neonMaterial(magenta, 0.9, false)
        );
        smile.rotation.z = Math.PI;
        smile.position.y = -0.05;
        group.add(ring, eyeA, eyeB, smile);
        group.userData.kind = "artifact";
        group.userData.baseY = data.position[1];
        return group;
      }}

      function gate(data) {{
        const group = new THREE.Group();
        const color = gameState.duplicate_j17 ? danger : violet;
        const geometry = new THREE.BoxGeometry(1.4, 2.7, 0.22);
        const frame = new THREE.Mesh(geometry, neonMaterial(color, 0.5, true));
        const marker = new THREE.Mesh(
          new THREE.TorusGeometry(0.35, 0.04, 6, 32),
          neonMaterial(color, 0.9, false)
        );
        marker.position.z = 0.22;
        group.add(frame, marker);
        group.userData.kind = "gate";
        group.userData.baseY = data.position[1];
        return group;
      }}

      Object.entries(objectsData).forEach(([objectId, data]) => {{
        let group;
        if (data.type === "evidence") {{
          group = evidenceNode(objectId, data, gameState.analyzed_evidence.includes(data.evidence_id));
        }} else if (data.type === "suspect") {{
          group = suspectHologram(objectId, data);
        }} else if (data.type === "ai_core") {{
          group = mirrorCore(data);
        }} else if (data.type === "terminal") {{
          group = terminalConsole(data);
        }} else if (data.type === "vault") {{
          group = memoryVault(data);
        }} else if (data.type === "artifact") {{
          group = smileArtifact(data);
        }} else {{
          group = gate(data);
        }}
        group.position.fromArray(data.position);
        register(objectId, group);
      }});

      let tokenLine = null;
      if (gameState.duplicate_j17) {{
        const start = new THREE.Vector3(...objectsData.sector_7_gate.position);
        const end = new THREE.Vector3(...objectsData.sector_3_gate.position);
        start.y += 0.6;
        end.y += 0.6;
        const points = [];
        for (let i = 0; i <= 40; i += 1) {{
          const point = start.clone().lerp(end, i / 40);
          point.y += Math.sin(i / 40 * Math.PI) * 2.2;
          points.push(point);
        }}
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        tokenLine = new THREE.Line(
          geometry,
          new THREE.LineBasicMaterial({{
            color: danger,
            transparent: true,
            opacity: 0.85,
            blending: THREE.AdditiveBlending
          }})
        );
        scene.add(tokenLine);
      }}

      function updateCamera() {{
        const cp = Math.cos(pitch);
        camera.position.set(
          target.x + Math.sin(yaw) * cp * distance,
          target.y + Math.sin(pitch) * distance,
          target.z + Math.cos(yaw) * cp * distance
        );
        camera.lookAt(target);
      }}

      function selectObject(objectId, notify) {{
        if (!objectMap.has(objectId)) return;
        selectedId = objectId;
        root.dataset.selected = objectId;
        root.querySelector(".sector7-selected-hud strong").textContent = objectsData[objectId].label;
        updateLocalHud(objectId);
        objectMap.forEach((group, id) => {{
          group.userData.selected = id === objectId;
        }});
        labels.forEach((label, id) => label.classList.toggle("is-selected", id === objectId));
        if (notify) sendSelection(objectId);
      }}

      function updatePointer(event) {{
        const rect = renderer.domElement.getBoundingClientRect();
        pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      }}

      renderer.domElement.addEventListener("pointerdown", (event) => {{
        dragging = true;
        moved = false;
        lastX = event.clientX;
        lastY = event.clientY;
        renderer.domElement.setPointerCapture(event.pointerId);
      }});
      renderer.domElement.addEventListener("pointermove", (event) => {{
        updatePointer(event);
        if (dragging) {{
          const dx = event.clientX - lastX;
          const dy = event.clientY - lastY;
          if (Math.abs(dx) + Math.abs(dy) > 3) moved = true;
          yaw -= dx * 0.006;
          pitch = Math.max(-0.08, Math.min(1.05, pitch + dy * 0.004));
          lastX = event.clientX;
          lastY = event.clientY;
          updateCamera();
          return;
        }}
        raycaster.setFromCamera(pointer, camera);
        const hit = raycaster.intersectObjects(interactive, false)[0];
        hovered = hit ? hit.object.userData.objectId : null;
        renderer.domElement.style.cursor = hovered ? "pointer" : "grab";
      }});
      renderer.domElement.addEventListener("pointerup", (event) => {{
        dragging = false;
        if (!moved) {{
          updatePointer(event);
          raycaster.setFromCamera(pointer, camera);
          const hit = raycaster.intersectObjects(interactive, false)[0];
          if (hit && hit.object.userData.objectId) selectObject(hit.object.userData.objectId, true);
        }}
      }});
      renderer.domElement.addEventListener("wheel", (event) => {{
        event.preventDefault();
        distance = Math.max(8, Math.min(27, distance + event.deltaY * 0.012));
        updateCamera();
      }}, {{ passive: false }});
      renderer.domElement.addEventListener("dblclick", () => {{
        yaw = 0;
        pitch = 0.29;
        distance = 16.5;
        updateCamera();
      }});

      function resize() {{
        if (!root.isConnected) return;
        const width = Math.max(1, root.clientWidth);
        const height = Math.max(1, root.clientHeight);
        renderer.setSize(width, height, false);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
      }}

      const resizeObserver = new ResizeObserver(resize);
      resizeObserver.observe(root);
      updateCamera();
      resize();
      selectObject(selectedId, false);
      root.classList.add("renderer-ready");

      const clock = new THREE.Clock();
      function animate() {{
        if (stopped || !root.isConnected) {{
          if (!stopped) stop();
          return;
        }}
        frame = requestAnimationFrame(animate);
        const t = clock.getElapsedTime();
        particles.rotation.y = t * (0.015 + gameState.corruption * 0.00035);
        particles.material.opacity = 0.42 + Math.sin(t * 2.2) * 0.13;
        objectMap.forEach((group, objectId) => {{
          const selectedScale = group.userData.selected ? 1.2 + Math.sin(t * 4) * 0.04 : 1;
          const hoverScale = hovered === objectId ? 1.12 : 1;
          group.scale.lerp(new THREE.Vector3(
            selectedScale * hoverScale,
            selectedScale * hoverScale,
            selectedScale * hoverScale
          ), 0.12);
          if (group.userData.kind === "evidence") {{
            group.rotation.y = t * 0.45;
            group.position.y = group.userData.baseY + Math.sin(t * 1.6 + group.position.x) * 0.13;
          }} else if (group.userData.kind === "suspect") {{
            group.position.y = group.userData.baseY + Math.sin(t * 1.25 + group.position.x) * 0.06;
            if (group.userData.stress > 55 && Math.sin(t * 14) > 0.96) {{
              group.position.x += (Math.random() - 0.5) * 0.05;
            }}
          }} else if (group.userData.kind === "core") {{
            group.rotation.y = t * (0.2 + gameState.corruption * 0.002);
            group.children.forEach((child) => {{
              if (child.userData.coreRing !== undefined) {{
                child.rotation.z = t * (0.18 + child.userData.coreRing * 0.09);
              }}
            }});
            if ((gameState.trust < 35 || gameState.corruption > 60) && Math.sin(t * 15) > 0.97) {{
              group.position.x += (Math.random() - 0.5) * 0.08;
            }}
          }} else if (group.userData.kind === "artifact") {{
            group.rotation.z = Math.sin(t) * 0.16;
          }}
        }});
        if (tokenLine) tokenLine.material.opacity = 0.55 + Math.sin(t * 5) * 0.3;

        labels.forEach((element, objectId) => {{
          const group = objectMap.get(objectId);
          const position = group.position.clone();
          position.y += group.userData.kind === "suspect" ? 2.2 : 1.1;
          position.project(camera);
          const visible = position.z < 1;
          element.style.transform = `translate(-50%, -50%) translate(${{(position.x * 0.5 + 0.5) * root.clientWidth}}px, ${{(-position.y * 0.5 + 0.5) * root.clientHeight}}px)`;
          element.style.opacity = visible ? "1" : "0";
        }});
        renderer.render(scene, camera);
      }}

      function stop() {{
        if (stopped) return;
        stopped = true;
        cancelAnimationFrame(frame);
        resizeObserver.disconnect();
        particleGeometry.dispose();
        scene.traverse((item) => {{
          if (item.geometry) item.geometry.dispose();
          if (item.material) {{
            if (Array.isArray(item.material)) item.material.forEach((mat) => mat.dispose());
            else item.material.dispose();
          }}
        }});
        renderer.dispose();
        labelLayer.replaceChildren();
      }}

      ns.currentInstance = {{ scene, camera, renderer, objects: objectMap, stop }};
      animate();
    }}).catch(() => {{
      const current = document.getElementById(rootId);
      if (current) current.dataset.renderer = "fallback";
    }});
  }}

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", boot, {{ once: true }});
  }} else {{
    requestAnimationFrame(boot);
  }}
}})();
</script>
"""
