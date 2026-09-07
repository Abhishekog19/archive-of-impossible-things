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
for (const [key, folder] of Object.entries({
  BLENDER_USER_CONFIG: 'config', BLENDER_USER_SCRIPTS: 'scripts',
  BLENDER_USER_DATAFILES: 'datafiles', BLENDER_USER_EXTENSIONS: 'extensions',
})) {
  env[key] = path.join(output, folder)
  fs.mkdirSync(env[key], { recursive: true })
}
const mode = process.argv[2] || 'setup'
if (!['setup', 'version', 'blockout'].includes(mode)) throw new Error('Use setup, version or blockout')
const args = mode === 'version' ? ['--version'] : [
  '--background', '--factory-startup', '--python-exit-code', '1',
  '--python', path.join(__dirname, mode === 'blockout' ? 'hub_blockout.py' : 'setup.py'), '--', '--output', output,
]
console.log(`Blender: ${executable}`)
const result = spawnSync(executable, args, { cwd: root, env, windowsHide: true, stdio: 'inherit' })
if (result.error) console.error(result.error.message)
process.exit(result.status ?? 1)
