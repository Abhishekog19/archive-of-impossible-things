// Serialize GPU preparation so neighbouring packages do not upload all of their
// atlases in the same frame. The scene owner retains resources until this settles.
const queues = new WeakMap()

export function nextPreparationFrame(signal) {
  return new Promise((resolve, reject) => {
    signal.throwIfAborted()
    const abort = () => { cancelAnimationFrame(frame); reject(signal.reason) }
    const frame = requestAnimationFrame(() => {
      signal.removeEventListener('abort', abort)
      resolve()
    })
    signal.addEventListener('abort', abort, { once: true })
  })
}

export function prepareScene(renderer, object, camera, scene, signal, onStage = () => {}, extraTextures = [], yieldFrame = nextPreparationFrame) {
  const previous = queues.get(renderer) || Promise.resolve()
  const task = previous.catch(() => {}).then(async () => {
    signal.throwIfAborted()
    const textures = new Set(extraTextures)
    object.traverse(node => {
      for (const material of Array.isArray(node.material) ? node.material : [node.material]) {
        if (!material) continue
        for (const value of Object.values(material)) if (value?.isTexture) textures.add(value)
      }
    })
    onStage('textures')
    for (const texture of textures) {
      await yieldFrame(signal)
      signal.throwIfAborted()
      renderer.initTexture(texture)
    }
    onStage('shaders')
    await yieldFrame(signal)
    signal.throwIfAborted()
    // Use the real scene's fog/lights so the prepared variant matches play.
    await renderer.compileAsync(object, camera, scene)
    signal.throwIfAborted()
  })
  queues.set(renderer, task)
  return task
}
