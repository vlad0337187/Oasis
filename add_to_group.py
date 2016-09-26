import bpy

selected_objects = bpy.context.selected_objects.copy()
bpy.ops.group.create(name="power_line-max_lod")

#for obj in selected_objects:
	#bpy.ops.object.group_link({'active_object':obj}, group='power_line-max_lod')
