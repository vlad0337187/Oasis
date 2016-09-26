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

Revision: 5
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
	
	# Keyboard 1
	if activated in keyb.inputs[W].queue:
		animations.animate()
	elif deactivated in keyb.inputs[W].queue:
		animations.animate()
		
	if activated in keyb.inputs[A].queue:
		animations.animate()
	elif deactivated in keyb.inputs[A].queue:
		animations.animate()
		
	if activated in keyb.inputs[D].queue:
		animations.animate()
	elif deactivated in keyb.inputs[D].queue:
		animations.animate()
		
	if activated in keyb.inputs[S].queue:
		animations.animate()
	elif deactivated in keyb.inputs[S].queue:
		animations.animate()

	# Mouse:
	if activated in mouse.inputs[LEFT_MOUSE].queue:
		gravity.gravity()
		animations.animate()
	elif deactivated in mouse.inputs[LEFT_MOUSE].queue:
		gravity.gravity()
		animations.animate()

	if activated in mouse.inputs[RIGHT_MOUSE].queue:
		gravity.gravity()
		animations.animate()
	elif deactivated in mouse.inputs[RIGHT_MOUSE].queue:
		gravity.gravity()
		animations.animate()

	if activated in mouse.inputs[MIDDLE_MOUSE].queue:
		gravity.gravity()
		animations.animate()
	elif deactivated in mouse.inputs[MIDDLE_MOUSE].queue:
		gravity.gravity()
		animations.animate()

	if activated in mouse.inputs[WHEELDOWN_MOUSE].queue:
		gravity.gravity()
		animations.animate()
	elif deactivated in mouse.inputs[WHEELDOWN_MOUSE].queue:
		gravity.gravity()
		animations.animate()
    
	if activated in mouse.inputs[WHEELUP_MOUSE].queue:
		gravity.gravity()
		animations.animate()
	elif deactivated in mouse.inputs[WHEELUP_MOUSE].queue:
		gravity.gravity()
		animations.animate()
        
        


animations.stand_straight()  # при первом запуске