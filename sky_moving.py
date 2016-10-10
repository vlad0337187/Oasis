'''Активирует анимацию вращения неба.

Author: Vladislav Naumov. naumovvladislav@list.ru; github.com/vlad1777d; vk.com/naumovvladislav
License: CC-BY. To use this under other license contact author.

Revision: 1
'''


import bge


scene = bge.logic.getCurrentScene()
sky = scene.objects['sky']


sky.playAction('sky_moving', 1, 10, layer=1, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=0.0002, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
