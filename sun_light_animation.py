import bge

obj = bge.logic.getCurrentController().owner

obj.playAction('sun_blinking(default_anim)', 1, 300, layer=0, priority=0, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=0.3, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)

#print('ANIMATION STARTED')