export const distanceToArea = (z, area) => Math.max(area.minZ - z, z - area.maxZ, 0)

export function desiredAreas(z, areas, active, bootstrap = false) {
  return areas.filter(area => distanceToArea(z, area) <= (bootstrap ? 6 : active.includes(area.id) ? area.keep : area.load))
    .map(area => area.id)
}

export function requiredAreas(z, areas) {
  const required = areas.filter(area => distanceToArea(z, area) <= 6)
  // The archive's aligned doors expose the hall and descent from the courtyard.
  // Wait for both visible destinations before releasing the loading gate; a
  // nearby exterior package alone leaves a bright empty portal on a cold entry.
  if (z >= -144 && z <= -87) {
    for (const id of ['hall', 'cavern']) {
      const area = areas.find(candidate => candidate.id === id)
      if (area && !required.includes(area)) required.push(area)
    }
  }
  return required.length ? required : [areas.reduce((best, area) => distanceToArea(z, area) < distanceToArea(z, best) ? area : best)]
}
