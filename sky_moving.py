'''Активирует анимацию вращения неба.
'''


import bge


scene = bge.logic.getCurrentScene()
sky = scene.objects['sky']


sky.playAction('sky_moving', 1, 10, layer=1, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=0.0002, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
