---
name: archive-world-builder
description: Build and visually iterate the Archive of Impossible Things hub environment, Blender assets, GLB integration, and third-person roaming. Use for environment production and visual review, not Archive gameplay.
---

# Archive world builder

Read `plans/CURRENT_PLAN.md` from the repository root for the active step. Consult
`environment-september-plan.md` for scope and dates, `look-target.md` for visual
targets, and `art-pipeline.md` for export conventions only as needed. Do not
duplicate those documents. Blender MCP is already configured; leave setup alone.

Follow this production order:

reference → blockout → camera match → terrain/ruins → vegetation → materials → lighting/fog → detail → optimization → GLB → R3F → collision → browser comparison.

- Use `concept/REF4.png` as the primary hub reference. Keep a reference camera
  separate from the third-person gameplay camera; match framing and aspect ratio.
- Establish plaza, path, landmark, and canopy silhouettes before surface detail.
- In each comparison, identify and fix the biggest 3–5 visual mismatches first
  (or all remaining mismatches if fewer). Do not polish tiny details early.
- Prove one representative asset's export and browser appearance before producing
  the full kit. Bake or recreate Blender effects that GLB cannot carry.
- Keep decorative geometry separate from simple walkable colliders. Reuse the
  existing Rapier/ecctrl integration; check stairs, slopes, grounding, and camera collision.
- Use available browser/Playwright tools for screenshots and traversal checks.
  Compare the reference camera and gameplay views after each visual iteration;
  record actual performance and remaining mismatches in the current plan.
- Optimize visible triangles, draw calls, textures, and foliage overdraw for Iris Xe
  and mobile. Real-phone verification stays pending until tested on a real device.
