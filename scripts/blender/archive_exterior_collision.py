"""Derive a simple collider for the attached archive tree/root silhouette."""
import bpy, os, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))

def export_with_collision():
    objects=[o for o in bpy.context.selected_objects if o.type in ('MESH','EMPTY') and o.name!='ArchiveExterior_Collision']
    previous=bpy.data.objects.get('ArchiveExterior_Collision')
    if previous:bpy.data.objects.remove(previous,do_unlink=True)
    wood=bpy.data.objects['ArchiveExterior_Wood']
    collider=wood.copy();collider.data=wood.data.copy();bpy.context.collection.objects.link(collider)
    collider.name='ArchiveExterior_Collision';collider.data.materials.clear()
    bpy.context.view_layer.objects.active=collider
    dec=collider.modifiers.new('Root collision budget','DECIMATE');dec.ratio=.14
    bpy.ops.object.modifier_apply(modifier=dec.name)
    collider.hide_render=True
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects+[collider]:obj.select_set(True)
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/source/archive-exterior.blend'),compress=True)
    target=ROOT/'public/models/archive-exterior.glb';temporary=target.with_name('archive-exterior.next.glb')
    bpy.ops.export_scene.gltf(filepath=str(temporary),export_format='GLB',
        use_selection=True,export_image_format='JPEG',export_image_quality=92)
    os.replace(temporary,target)

if __name__=='__main__':
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/source/archive-exterior.blend'))
    export_with_collision()
    from world_art_context import export_context
    export_context()
