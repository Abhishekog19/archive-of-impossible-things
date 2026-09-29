export const distanceToArea = (z, area) => Math.max(area.minZ - z, z - area.maxZ, 0)

export function desiredAreas(z, areas, active, bootstrap = false) {
  return areas.filter(area => distanceToArea(z, area) <= (bootstrap ? 6 : active.includes(area.id) ? area.keep : area.load))
    .map(area => area.id)
}

export function requiredAreas(z, areas) {
  const required = areas.filter(area => distanceToArea(z, area) <= 6)
  return required.length ? required : [areas.reduce((best, area) => distanceToArea(z, area) < distanceToArea(z, best) ? area : best)]
}
