"""Shared ownership of the Phase 5 hub boundary replacements (visuals only)."""
def boundary_proxy(name, x, z):
    if name.startswith('Collision'):return False
    if name.startswith('Broken wall'):
        return not (-21<x<-4 and -40<z<-17)  # Phase 3 connector owns these.
    return name.startswith(('Woodland rock ridge','Arrival slope','Right branch','Island understory',
        'Overgrown path mouth','Overgrown branch roots','Overlook parapet',
        'Overlook side pier','Far broken bridge'))
