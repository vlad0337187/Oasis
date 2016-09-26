'''Запускает анимацию на текущем экземпляре объекта со случайной скоростью.

На нужном объекте добавляем сенсор Delay с контроллером Python, тип - модуль.
Далее запускаем нужную функцию.

Версия: 2
'''

import bge
import random



def get_object():
    number = random.choice((-0.3, -0.2, -0.1, 0.0, 0.1, 0.2))
    contr = bge.logic.getCurrentController()
    obj = contr.owner
    return number, obj



def grass_main_armature():
    number, obj = get_object()
    obj.playAction('grass_main_wind', 1, 120, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)


def grass_violent():
    number, obj = get_object()
    obj.playAction('grass_violent_wind', 1, 122, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_PING_PONG, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def grass_liana():
    number, obj = get_object()
    obj.playAction('grass_liana_wind', 1, 146, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_PING_PONG, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def grass_dry():
    number, obj = get_object()
    obj.playAction('grass_dry_wind', 1, 160, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_PING_PONG, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def grass_1_armature():
    number, obj = get_object()
    obj.playAction('grass_1_wind', 1, 159, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def grass_2_armature():
    number, obj = get_object()
    obj.playAction('grass_2_wind', 1, 121, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def grass_3_armature():
    number, obj = get_object()
    obj.playAction('grass_3_wind', 1, 121, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def grass_4_armature():
    number, obj = get_object()
    obj.playAction('grass_4_wind', 1, 121, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
  
    
    
    
def tree_3_armature():
    number, obj = get_object()
    obj.playAction('tree_3_wind', 1, 601, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)


def tree_3_LOD1_armature():
    number, obj = get_object()
    obj.playAction('tree_3_LOD1_wind', 1, 301, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    

def tree_4_armature():
    number, obj = get_object()
    obj.playAction('tree_4_wind', 1, 601, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def tree_4_LOD1_armature():
    number, obj = get_object()
    obj.playAction('tree_4_LOD1_wind', 1, 451, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def tree_5_armature():
    number, obj = get_object()
    obj.playAction('tree_5_wind', 1, 301, layer=0, priority=1, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1 + number, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)