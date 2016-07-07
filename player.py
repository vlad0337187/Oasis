'''Обеспечивает действия персонажа, такие как замедление при входе в воду и т.д.
Требует:
	-объект персонажа с именем player.
	-актуаторы движения, подключенные к контроллеру, на котором запускается скрипт:
		-с именем forward
		-с именем left
		-с именем right
		-с именем back
		-вращения объекта по оси y (вертикально) с именем vertical_rot
		-с именем custom
	-должен запускаться при нажатии клавиш: W, A, S, D, LShift, Space.

Версия: 5
'''
'''Что сделать:
	-возможно не нужен custom_actuator
'''


import bge
from keys_reductions import *
from mathutils import Matrix, Euler



scene = bge.logic.getCurrentScene()
player = scene.objects["player"]
#controller = bge.logic.getCurrentController()  # активирует какой-то другой контроллер
controller = player.controllers['Python']
player_camera_empty = scene.objects["player_camera_empty"]


actuators = player.actuators

forward_actuator = actuators['forward']
left_actuator = actuators['left']
right_actuator = actuators['right']
back_actuator = actuators['back']
custom_actuator = actuators['custom']  # для нестандартных движений, движется по локальной оси Х даже вверх

vertical_rotation_actuator = actuators['vertical_rot']
camera_rotation_actuator = player_camera_empty.actuators['rotation']


common_speed = 0.2
common_speed_backup = common_speed  # для функций on_ и off_slow_down()
mass = player.mass
underwater = 0  # для функций



def play():
	general_moving()  # будут и другие


def general_moving():
	if keyb.events[W] == activated:
		forward(True)
	elif keyb.events[W] == deactivated:
		forward(False)
	if keyb.events[A] == activated:
		left(True)
	if keyb.events[A] == deactivated:
		left(False)
	elif keyb.events[D] == activated:
		right(True)
	elif keyb.events[D] == deactivated:
		right(False)
	if keyb.events[S] == activated:
		back(True)
	elif keyb.events[S] == deactivated:
		back(False)
	if keyb.events[LSHIFT] == activated:
		shift_speed_up(True)
	elif keyb.events[LSHIFT] == deactivated:
		shift_speed_up(False)
		
        

def no_dynamics():
    player.suspendDynamics(False)
    print(player.isSuspendDynamics)
    
    
def dynamics():
    player.restoreDynamics()
    print(player.isSuspendDynamics)


def forward(state):
	if state == True:
		controller.activate(forward_actuator)
	if state == False:
		controller.deactivate(forward_actuator)
    

def left(state):
	if state == True:
		controller.activate(left_actuator)
	if state == False:
		controller.deactivate(left_actuator)


def right(state):
	if state == True:
		controller.activate(right_actuator)
	if state == False:
		controller.deactivate(right_actuator)


def back(state):
	if state == True:
		controller.activate(back_actuator)
	if state == False:
		controller.deactivate(back_actuator)
		
		
def shift_speed_up(state):
	'''Ускоряет персонажа при нажатии шифта.
	Вызывается из player(). (v1)
	'''
	if state == True:
		forward_actuator.dLoc = (common_speed * 2, 0, 0)
		left_actuator.dLoc = (0, common_speed * 2, 0)
		right_actuator.dLoc = (0, - common_speed * 2, 0)
		back_actuator.dLoc = (-common_speed * 2, 0, 0)
	elif state == False:
		forward_actuator.dLoc = (common_speed, 0, 0)
		left_actuator.dLoc = (0, common_speed, 0)
		right_actuator.dLoc = (0, - common_speed, 0)
		back_actuator.dLoc = (- common_speed, 0, 0)
		
		
def on_slow_down():
	'''Замедляет движение игрока
	'''
	global common_speed
	common_speed = common_speed_backup / 4
	
	forward_actuator.dLoc = (common_speed, 0, 0)
	left_actuator.dLoc = (0, common_speed, 0)
	right_actuator.dLoc = (0, - common_speed, 0)
	back_actuator.dLoc = (- common_speed, 0, 0)	


def off_slow_down():
	
	global common_speed
	common_speed = common_speed_backup
	
	forward_actuator.dLoc = (common_speed, 0, 0)
	left_actuator.dLoc = (0, common_speed, 0)
	right_actuator.dLoc = (0, - common_speed, 0)
	back_actuator.dLoc = (- common_speed, 0, 0)	


def on_underwater():
	'''Позволяет персонажу двигаться в направлени куда смотрит.
	Отключает вращение вверх-вниз пустышки камеры, включает для самого игрока.
	Вызывается с того места, которое анализирует: под водой ли игрок. 
	Обычно комбинируется с функциями замедления, так как сама не замедляет игрока.
	(v1)
	'''
	global underwater
	if underwater == 1: return
	
	camera_local_euler_copy = player_camera_empty.localOrientation.to_euler().copy()  # чтобы знать предыдущее
	
	vertical_rotation_actuator.sensitivity = [0, -2.0]  # самого игрока
	camera_rotation_actuator.sensitivity = [0, 0]  # камеры
	camera_rotation_actuator.reset()  # если не сбросить сразу - будут проблемы
	vertical_rotation_actuator.reset()
	
	player_local_euler = player.localOrientation.to_euler()  # потому что локальная - хуйня.
	camera_local_euler = player_camera_empty.localOrientation.to_euler()
	
	player_local_euler.y = camera_local_euler_copy.y
	player.localOrientation = player_local_euler  # чтобы не было рывка камеры
	
	camera_local_euler = player_camera_empty.localOrientation.to_euler()  # еще раз получили - ведь значение поменялось
	camera_local_euler.y = 0
	player_camera_empty.localOrientation = camera_local_euler  # выровняли камеру вертикально
	
	custom_actuator.linV = (-0.01, 0, 0)  # позволяет не падать в воду
	player.localLinearVelocity = (0, 0, 0)  # чтобы не улетал
	
	underwater = 1
	print('on_underwater()')	
	

def off_underwater():
	'''Возвращает обычное движение игроку при возвращении на сушу.
	Вращение вверх-вниз для игрока становится 0, теперь вверх-вниз вращается только камера.
	Вызывается с того места, которое анализирует: под водой ли игрок. (v1)
	'''
	global underwater
	if underwater == 0: return

	player_local_euler_copy = player.localOrientation.to_euler().copy()

	camera_rotation_actuator.sensitivity = [0, -2.0]
	vertical_rotation_actuator.sensitivity = [0, 0]
	vertical_rotation_actuator.reset()  # если не сбросить - будут проблемы
	camera_rotation_actuator.reset()
	
	camera_local_euler = player_camera_empty.localOrientation.to_euler()
	player_local_euler = player.localOrientation.to_euler()
	
	camera_local_euler.y = player_local_euler_copy.y  # присваиваем сейчас, потому что позже его поменяем.
	player_camera_empty.localOrientation = camera_local_euler  # чтобы не было рывка камеры.
	
	player_local_euler_copy.y = 0
	player.localOrientation = player_local_euler_copy  # выровняли вертикально игрока

	custom_actuator.linV = (0, 0, 0)  # позволяло не падать в воду
	player.localLinearVelocity = (0, 0, 0)  # чтобы не улетал
	
	underwater = 0
	print('off_underwater()')
	
	
def null_actuators():
	'''Обнуляет значения всех актуаторов движения, включает флаги работы в локальных координатах. 
	Сначала актуаторы движения, затем вращения. (v1)
	'''
	for act in (forward_actuator, left_actuator, right_actuator, back_actuator, custom_actuator):
		act.force = (0, 0, 0)
		act.torque = (0, 0, 0)
		act.dLoc = (0, 0, 0)
		act.dRot = (0, 0, 0)
		act.linV = (0, 0, 0)
		act.angV = (0, 0, 0)
		act.damping = 0
		
		act.useLocalForce = True
		act.useLocalTorque = True
		act.useLocalDLoc = True
		act.useLocalDRot = True
		act.useLocalLinV = True
		act.useLocalAngV = True
		
	for act in(vertical_rotation_actuator, camera_rotation_actuator):
		
		

def default_values_actuators():
	'''Присваивает всем актуаторам движения нужные значения по-умолчанию.
	Сначала актуаторам движения, затем вращения.
	Вызывается после null_actuators(). (v1)
	'''
	forward_actuator.dLoc = (common_speed, 0, 0)
	left_actuator.dLoc = (0, common_speed, 0)
	right_actuator.dLoc = (0, - common_speed, 0)
	back_actuator.dLoc = (- common_speed, 0, 0)	
		
		

null_actuators()  # при первом запуске
default_values_actuators()
