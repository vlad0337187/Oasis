'''Модуль анимации гравитационного ружья. 
Запускается выполнением функции animate() при нажатии клавиш мыши и WASD
(колесико вверх, вниз; левая, правая средняя кнопки мыши).

Требует:
    - наличие арматуры ружья с именем gun_armature;
    - наличие указанных в функциях анимаций.
    
Версия: 12
'''



import bge
from keys_reductions import *



scene = bge.logic.getCurrentScene()
gun_armature = scene.objects['gun_armature']
cont = bge.logic.getCurrentController()
globalDict = bge.logic.globalDict



def animate():
    '''Главная функция анимации.
    Запускает все остальные анимации. (v2)
    '''
    #print('animate()')

    if keyb.events[W] == activated:
        walk_forward()
        steps(True)
    elif keyb.events[W] == deactivated:
        stop_walking()
        steps(False)
        
    elif keyb.events[A] == activated:
        if keyb.events[W] == active:
            pass
        else:
            steps(True)
    elif keyb.events[A] == deactivated:
        if keyb.events[W] == active:
            pass
        else:
            steps(False)
            stand_straight()
            
    elif keyb.events[D] == activated:
        if keyb.events[W] == active:
            pass
        else:
            steps(True)
    elif keyb.events[D] == deactivated:
        if keyb.events[W] == active:
            pass
        else:
            steps(False)
            stand_straight()
            
    elif keyb.events[S] == activated:
        if keyb.events[W] == active:
            pass
        else:
            steps(True)
    elif keyb.events[S] == deactivated:
        if keyb.events[W] == active:
            pass
        else:
            steps(False)
            stand_straight()
            
        
    if mouse.events[LEFT_MOUSE] == activated:
        try_pulling()
        if globalDict['pulled'] == True:
            item_pulled()
        elif globalDict['pulled'] == False:
            stop_item_pulled()
    elif mouse.events[RIGHT_MOUSE] == activated:
        try_pulling()
        if globalDict['pulled'] == True:
            item_pulled()
        elif globalDict['pulled'] == False:
            stop_item_pulled()
    elif mouse.events[WHEELDOWN_MOUSE] == activated:
        #print('wheel down mouse')
        if globalDict['target'] != None:
            try_pulling()
    elif mouse.events[WHEELUP_MOUSE] == activated:
        #print('wheel up mouse')
        if globalDict['target'] != None:
            try_pulling()
    elif mouse.events[MIDDLE_MOUSE] == activated:
        if globalDict['target'] != None:
            try_pulling()




def walk_forward():
    '''Активирует актуатор анимации ходьбы.
    '''
    #global cont
    #standing(False)  # не используется
    #cont.activate('walk')
    gun_armature.playAction('gun_walk_start_stop_v3', 0, 10, layer=1, priority=1, blendin=3, play_mode=bge.logic.KX_ACTION_MODE_PLAY, layer_weight=0.0, ipo_flags=0, speed=1.0, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def stop_walking():
    '''Деактивирует актуатор анимации ходьбы.
    '''
    #global cont
    #cont.activate('stop')
    #standing(True)  # не используется
    gun_armature.playAction('gun_walk_start_stop_v3', 10, 0, layer=1, priority=1, blendin=3, play_mode=bge.logic.KX_ACTION_MODE_PLAY, layer_weight=0.0, ipo_flags=0, speed=1.0, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def steps(status):
    '''Активирует или деактивирует актуатор анимации шагов.
    '''
    global cont
    if status == True:
        gun_armature.playAction('gun_steps', 10, 35, layer=2, priority=2, blendin=3, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1.0, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    elif status == False:
        gun_armature.stopAction(2)
        
        
def try_pulling():
    '''Активирует актуатор анимации попытки притянуть предмет.
    '''
    #global cont
    #cont.activate('try_pulling')
    #gun_armature.playAction('gun_try_pulling', 0, 12, layer=1, priority=2, blendin=3, play_mode=bge.logic.KX_ACTION_MODE_PLAY, layer_weight=0.0, ipo_flags=0, speed=1.0, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    gun_armature.stopAction(1)
    gun_armature.playAction('gun_try_pulling_v2', 0, 100, layer=1, priority=2, blendin=3, play_mode=bge.logic.KX_ACTION_MODE_PLAY, layer_weight=0.0, ipo_flags=0, speed=1.0, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    
    
def item_pulled():
    '''Активирует актуатор анимации с притянутым предметом.
    '''
    #global cont
    #cont.activate('item_pulled')
    #gun_armature.playAction('gun_item_pulled', 0, 20, layer=4, priority=4, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1.0, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
    gun_armature.playAction('gun_pulled', 0, 82, layer=4, priority=4, blendin=0, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1.0, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)


def stop_item_pulled():
    '''Деактивирует актуатор анимации с притянутым предметом.
    '''
    #global cont
    #cont.deactivate('item_pulled')
    gun_armature.stopAction(4)

    
def stand_straight():
    '''Позволяет выровняться после шагов без смещения пушки. 
    Если активирован только актуатор шагов - пушка поворачивается и прячется за камеру.
    Это нужно чтобы вернуть ее на место - сама не возвращается.
    '''
    gun_armature.playAction('gun_stand_straight', 0, 5, layer=1, priority=2, blendin=5, play_mode=bge.logic.KX_ACTION_MODE_LOOP, layer_weight=0.0, ipo_flags=0, speed=1.0, blend_mode=bge.logic.KX_ACTION_BLEND_BLEND)
