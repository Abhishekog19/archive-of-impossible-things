export const SPRING = { x: -12.5, z: -48, reach: 5.5 }
export const SPRING_KEY = 'archive.spring.v1'
export const ROUTES = ['leaves', 'stones', 'root']
export const EMPTY_SPRING = { route: null, bent: false, lifted: false, complete: false }

export function readSpring(raw) {
  try {
    const value = JSON.parse(raw)
    if (value?.version !== 1) return { ...EMPTY_SPRING }
    const bent = value.bent === true, lifted = value.lifted === true
    return { route: null, bent, lifted, complete: bent && lifted && value.complete === true }
  } catch { return { ...EMPTY_SPRING } }
}

export function directSpring(state, route) {
  if (!ROUTES.includes(route)) return state
  return { route, bent: state.bent || route === 'leaves', lifted: state.lifted || route === 'stones',
    complete: state.complete || (route === 'root' && state.bent && state.lifted) }
}

export function springMessage(state) {
  if (state.route === 'leaves') return 'The leaves bend toward the stream. The water remembers how to curve.'
  if (state.route === 'stones') return 'The stones rise on the water. The spring remembers how to lift.'
  if (state.route === 'root') return state.complete
    ? 'The spring remembers both lessons. Water climbs the root, and a new leaf opens.'
    : 'The stream reaches the root, then falls back. What could the other paths teach it?'
  return state.complete ? 'The root still holds your discovery. You can keep experimenting.'
    : 'Three paths leave this spring. Where should the water go?'
}
