"""Split the proven kit into independent ruin/forest packages; no source edits."""
import bpy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads((ROOT/'src/config/asset-kit.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/source/archive-kit.blend'))
groups={
    'ruins':[a['name'] for a in manifest['assets'] if a['family']=='Stone'],
    'forest':[a['name'] for a in manifest['assets'] if a['family']=='Wood']+manifest['extras'],
}
output=ROOT/'public/models/zones'
output.mkdir(parents=True,exist_ok=True)
report={'source':'art/source/archive-kit.blend','packages':{}}
for name,names in groups.items():
    bpy.ops.object.select_all(action='DESELECT')
    selected=[]
    for asset in names:
        for key in (asset,'Collider_'+asset):
            obj=bpy.data.objects.get(key)
            if obj is None:
                if key==asset: raise RuntimeError('Missing runtime asset '+asset)
                continue
            obj.hide_set(False);obj.select_set(True);selected.append(key)
    path=output/(name+'.glb')
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,
                              export_image_format='JPEG',export_image_quality=90)
    report['packages'][name]={'url':'/models/zones/'+name+'.glb',
                              'bytes':path.stat().st_size,'nodes':selected}
(ROOT/'src/config/zone-packages.json').write_text(json.dumps(report,indent=2)+'\n')
print('ZONE_PACKAGES '+json.dumps(report),flush=True)
