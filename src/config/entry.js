// The assembled world is the public entry. Explicit study links stay usable.
export function usesAssembledWorld(params) {
  return params.get('patch') !== '0' && !['greyroom', 'kit', 'zones', 'water', 'cavern', 'hub']
    .includes(params.get('scene'))
}
