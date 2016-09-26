'''Вычисляет: на какую точку передней части объектива камеры попадает луч от солнца.
Нужна для правильной работы шейдера (2д фильтра) "filter_light_scattering.glsl".

Требует:
	-наличие объекта солнца с именем "Sun".
	-наличие объекта пустышки камеры (камера - потомок) с именем "player_camera_empty"
	(именно пустышки, ведь у камеры неправильные локальные координаты).
	-наличие объекта активной камеры.
	-podkliuchit aktuatory aktivacii i deaktivacii 2d filtra (sheidera) "filter_light_scattering.glsl" s
	imenami "scattering" i "deactivate_scattering".

better to hang this module to mousemove sensor - it moves camera (than there will not be extra launches).
Also it's needed to add Delay-0 sensor to launch it on startup.

Kogda solnce popadaet v kameru, vkliuchaem sheider, postepenno uvelichivaem ves luchei.
Kogda solnce perestaet popadat v kameru, postepenno umenshiaem ves luchei.
Kogda luchi budut <= 0, vykliuchaem sheider.

Версия: v2
'''

import bge
from math import *  # for translating radians to degrees
#from mathutils import Matrix, Euler



scene = bge.logic.getCurrentScene()
sun = scene.objects['Sun']
camera = scene.active_camera
fov = camera.fov  # degree of view of camera. Dlia nahozhdenia koordinat ekrana
camera_empty = scene.objects['player_camera_empty']
weight_backup = camera_empty['weight'] + 0.01  # нужна для функции
step = 0.006  # step for gradually changing weight value
contr = bge.logic.getCurrentController()




def scattering():
	'''This is the main function, which is called time to time from object.
	It calles all other functions.
	'''
	if scattering_on_off():
		if not scene.filterManager.getFilter(10):
			contr.activate('scattering')
		if camera_empty['weight'] < weight_backup:
			camera_empty['weight'] += step
		change_screen_x_coordinates()
		change_screen_y_coordinates()
	else:
		if camera_empty['weight'] > 0.0:
			camera_empty['weight'] -= step
		elif camera_empty['weight'] <= 0.0:
			if scene.filterManager.getFilter(10):
				contr.activate('remove_scattering')		




def refresh_camera():
	'''Обновляет при изменении камеру.
	'''
	global camera, fov
	camera = scene.active_camera
	fov = camera.fov


def scattering_on_off():
	'''Vozvrachaet True esli solnce ne bolshe chem na 90 gradusov ot camery otvernulos.
	(ranshe bylo: Vozvrachaet True esli solnce popadaet v obiektiv)
	'''
	#global camera_empty
	#if camera.pointInsideFrustum(sun.worldPosition):  # ranshe bylo
	vector = camera_empty.getVectTo(sun)[2]
	#x = fov / 180  # po proporcii
	
	if vector.x > 0:  # togda solnce speredi kamery
		#print('scattering on')
		return True
	else:
		#print('scattering off')
		return False
	#print(weight_backup, camera_empty['weight'])


def change_screen_x_coordinates():
	'''
	1. Puskaem vektor (lokalnyi, tak kak kamera vertitsia) ot camery do solnca.
	2. Poluchaem Y vektora (X displeia kamery).
	3. Tochku centra (O) smeschaem vniz i sootvetstvenno meniaem z. Z i est iskomaia koordinata Y.
	'''
	vect = camera_empty.getVectTo(sun)[2]
	y = - vect[1]
	#print('sun local y = ', y)
	
	x = y
	#x += 0.5  # 0.5 eto celaia vysota (1) delim na 2
	# in UPBGE not needed - we count from edge of screen
	
	camera_empty['x'] = x
	#print('x = ', x)


def change_screen_y_coordinates():
	'''
	1. Puskaem vektor (lokalnyi, tak kak kamera vertitsia) ot camery do solnca.
	2. Poluchaem Z vektora.
	3. Tochku centra (O) smeschaem vniz i sootvetstvenno meniaem z. Z i est iskomaia koordinata Y.
	'''
	vect = camera_empty.getVectTo(sun)[2]
	z = vect[2]
	#print('sun local z = ', z)
	
	y = z
	#y += 0.5  # 0.5 eto celaia vysota (1) delim na 2
	# in UPBGE not needed - we count from edge of screen
	
	camera_empty['y'] = y
	#print('y = ', y)
	
	
	
	
scattering()