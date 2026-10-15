# Vercel deployment

The intended host is Vercel Hobby. This repository builds a static Vite site;
the environment, physics and graphics preparation run in the visitor's browser.
No server function, database or paid rendering service is required by this build.

Import `Abhishekog19/archive-of-impossible-things`, select `main`, and use the
repository root. `vercel.json` specifies Vite, `npm ci`, `npm run build` and `dist`.
No environment variables are needed for the current environment milestone.
Current navigation uses query strings on `/`, so no SPA route rewrite is needed.
See [Vercel's Vite deployment documentation](https://vercel.com/docs/frameworks/frontend/vite).

Keep the default cache behavior for the model and texture paths. These assets
currently have stable filenames that are replaced by art builds; a year-long
browser `immutable` policy would risk serving stale scenery. Introduce content
hashes before applying that policy. Vite's generated JavaScript/CSS chunks
already have content hashes. See [Vercel's cache header documentation](https://vercel.com/docs/caching/cache-control-headers).

The loader prepares entry-area textures and shaders, then loads ahead along the
route. It does not pin the entire world in GPU memory. Hosting delivers the files;
draw calls, pixels, geometry and device memory still determine sustained FPS.

Once the deployment URL is available, verify a new visit and a repeat visit,
GLB/texture responses, entry-to-playable transfer, portal/return travel, worker
loading, and actual phone controls/thermals. Local preview results do not prove
deployment performance. The current working target is 50–55 FPS. The October 15
local three-minute check passed at 58.64 FPS; this does not establish deployment
or physical-device performance. Startup transfer and visible-triangle budgets
remain open. See [the final verification](ENVIRONMENT_FINAL_VERIFICATION_2026-10-15.md).
