import test from 'node:test'
import assert from 'node:assert/strict'
import { BoxGeometry, Group, Mesh, MeshBasicMaterial, Texture } from 'three'
import { prepareScene } from '../src/scenes/prepareScene.js'

test('preparation uploads unique textures on separate turns before compiling with the real scene', async () => {
  const object = new Group(), map = new Texture(), detail = new Texture()
  object.add(new Mesh(new BoxGeometry(), new MeshBasicMaterial({ map })))
  object.add(new Mesh(new BoxGeometry(), new MeshBasicMaterial({ map })))
  const calls = [], camera = {}, scene = {}
  const renderer = {
    initTexture: texture => calls.push(texture),
    compileAsync: async (...args) => { assert.deepEqual(args, [object, camera, scene]); calls.push('compile') },
  }
  await prepareScene(renderer, object, camera, scene, new AbortController().signal,
    stage => calls.push(stage), [detail, detail], async () => calls.push('frame'))
  assert.deepEqual(calls, ['textures', 'frame', detail, 'frame', map, 'shaders', 'frame', 'compile'])
})

test('aborted queued preparation never touches the GPU and does not block the next area', async () => {
  let finishCompile
  const compiled = [], renderer = {
    initTexture() {},
    compileAsync: object => {
      compiled.push(object.name)
      return object.name === 'first' ? new Promise(resolve => { finishCompile = resolve }) : Promise.resolve()
    },
  }
  const group = name => { const value = new Group(); value.name = name; return value }
  const firstController = new AbortController(), queuedController = new AbortController()
  const first = prepareScene(renderer, group('first'), {}, {}, firstController.signal, undefined, [], async () => {})
  // Let the first compile begin and attach rejection handlers before aborting.
  await new Promise(resolve => setImmediate(resolve))
  const queued = prepareScene(renderer, group('cancelled'), {}, {}, queuedController.signal, undefined, [], async () => {})
  const next = prepareScene(renderer, group('next'), {}, {}, new AbortController().signal, undefined, [], async () => {})
  const rejectedFirst = assert.rejects(first, { name: 'AbortError' })
  const rejectedQueued = assert.rejects(queued, { name: 'AbortError' })
  firstController.abort(); queuedController.abort()
  assert.deepEqual(compiled, ['first'])
  finishCompile()
  await Promise.all([rejectedFirst, rejectedQueued, next])
  assert.deepEqual(compiled, ['first', 'next'])
})

test('texture preparation failure is surfaced and later work can still prepare', async () => {
  const object = new Group(), texture = new Texture()
  let fail = true, compiled = 0
  const renderer = {
    initTexture: () => { if (fail) throw new Error('upload failed') },
    compileAsync: async () => { compiled++ },
  }
  const run = () => prepareScene(renderer, object, {}, {}, new AbortController().signal, undefined, [texture], async () => {})
  await assert.rejects(run(), /upload failed/)
  fail = false
  await run()
  assert.equal(compiled, 1)
})
