const fs = require('node:fs')
const path = require('node:path')
const { spawnSync } = require('node:child_process')

const root = path.resolve(__dirname, '../..')
const output = path.join(root, '.artifacts', 'blender')
const candidates = [process.env.BLENDER_PATH]
const foundation = 'C:/Program Files/Blender Foundation'
if (fs.existsSync(foundation)) {
  for (const name of fs.readdirSync(foundation).sort().reverse()) {
    candidates.push(path.join(foundation, name, 'blender.exe'))
  }
}
const executable = candidates.find((p) => p && fs.existsSync(p))
if (!executable) {
  console.error('Blender not found. Set BLENDER_PATH to the installed blender.exe.')
  process.exit(1)
}
fs.mkdirSync(output, { recursive: true })
const env = { ...process.env }
// glTF image conversion must use a writable project-local temporary directory.
// Sandboxed Windows sessions can deny Blender's inherited system temp path.
env.TEMP = env.TMP = path.join(output, 'temp')
fs.mkdirSync(env.TEMP, { recursive: true })
for (const [key, folder] of Object.entries({
  BLENDER_USER_CONFIG: 'config', BLENDER_USER_SCRIPTS: 'scripts',
  BLENDER_USER_DATAFILES: 'datafiles', BLENDER_USER_EXTENSIONS: 'extensions',
})) {
  env[key] = path.join(output, folder)
  fs.mkdirSync(env[key], { recursive: true })
}
const mode = process.argv[2] || 'setup'
if (!['setup', 'version', 'blockout', 'corner', 'world', 'kit', 'zones', 'cavern', 'patch', 'hub-art', 'forest-approach', 'forest-canopy', 'archive-exterior', 'archive-hall', 'cavern-structure', 'woodland-backdrop', 'world-finish', 'explorer', 'ruin-runner', 'release-finish', 'ruin-runner-runtime', 'hub-natural-finish', 'hub-boundaries', 'archive-exterior-collision'].includes(mode)) throw new Error('Unknown Blender production mode: '+mode)
const scripts = { setup: 'setup.py', blockout: 'hub_blockout.py', corner: 'hub_corner.py', world: 'world_blockout.py', kit: 'asset_kit.py', zones: 'zone_kit.py', cavern: 'cavern_study.py', patch: 'forest_patch.py', 'hub-art': 'hub_art.py', 'forest-approach': 'forest_approach.py', 'forest-canopy': 'forest_canopy.py' }
const args = mode === 'version' ? ['--version'] : [
  '--background', '--factory-startup', '--python-exit-code', '1',
  '--python', path.join(__dirname, scripts[mode] || mode.replaceAll('-', '_')+'.py'), '--', '--output', output,
  ...process.argv.slice(3),
]
console.log(`Blender: ${executable}`)
const result = spawnSync(executable, args, { cwd: root, env, windowsHide: true, stdio: 'inherit' })
if (result.error) console.error(result.error.message)
process.exit(result.status ?? 1)
