'''Данный модуль позволяет запускать различные действия после нажания клавиш пользователем.

Он позволяет контроллировать очередность запускаемых функций и тем самым избежать ошибок.
В данный момент с его помощью работают модули gun_gravity и gun_animations (хотя они могут работать и отдельно (сами анализируют нажатия клавиш) (нужно просто к нип подключить сенсоры всех требуемых клавиш).
Структура:
    keys_input():
        gun_gravity;
        gun_animations.

Требует:
	наличие модулей:
		gun_gravity;
		gun_animations;
		keys_reductions.

Версия: 4
'''

import bge
import gun_gravity as gravity
import gun_animations as animations
from keys_reductions import *



def pressed():
    ''' Обрабатывает любые клавиши, вызывает нужную реакцию на них.
    '''
    '''print('pressed activated')
    print('wkey reduced: ', keyb.events[W])
    #print('thr. point', eval('bge.logic.keyboard.events[bge.events.WKEY]'))
    #print(bge.logic.keyboard.events[W])
    print('activated: ', activated)
    print(keyb.events[W] == activated)
    #pr_keys()'''
    if keyb.events[W] == activated or keyb.events[W] == deactivated:
        animations.animate()
    elif keyb.events[A] == activated or keyb.events[A] == deactivated:
        animations.animate()
    elif keyb.events[D] == activated or keyb.events[D] == deactivated:
        animations.animate()
    elif keyb.events[S] == activated or keyb.events[S] == deactivated:
        animations.animate()
      
    if mouse.events[LEFT_MOUSE]:
        gravity.gravity()
        animations.animate()
    elif mouse.events[RIGHT_MOUSE]:
        gravity.gravity()
        animations.animate()
    elif mouse.events[MIDDLE_MOUSE]:
        gravity.gravity()
        animations.animate()
    elif mouse.events[WHEELDOWN_MOUSE]:
        gravity.gravity()
        animations.animate()
    elif mouse.events[WHEELUP_MOUSE]:
        gravity.gravity()
        animations.animate()
        
        

animations.stand_straight()  # при первом запуске
