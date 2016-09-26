'''Вычисляет: на какую точку передней части объектива камеры попадает луч от солнца.
Нужна для правильной работы шейдера (2д фильтра) "filter_light_scattering.glsl".

Требует:
	-наличие объекта солнца с именем "Sun".
	-наличие объекта пустышки камеры (камера - потомок) с именем "player_camera_empty"
	(именно пустышки, ведь у камеры неправильные локальные координаты).
	-наличие объекта активной камеры.
	-podkliuchit dva aktuatora aktivacii i deaktivacii 2d filtra (sheidera) "filter_light_scattering.glsl" s
	imenami "scattering" i "deactivate_scattering", "scattering_2" i "deactivate_scattering_2".

better to hang this module to mousemove sensor - it moves camera (than there will not be extra launches).
Also it's needed to add Delay-0 sensor to launch it on startup.

Kogda solnce popadaet v kameru, vkliuchaem sheider, postepenno uvelichivaem ves luchei.
Kogda solnce perestaet popadat v kameru, postepenno umenshiaem ves luchei.
Kogda luchi budut <= 0, vykliuchaem sheider.

Revision: v3
'''

''' Ne udalos zastavit rabotat tak kak eto 2D filtr, ne 3d. Solnce ne mozhet byt za kameroi - 
ne smozhwt renderit luchi szadi.

SDELAT ZHELTYI CVET V SOLNECHNYH LUCHAH
'''

import bge
from math import *  # for translating radians to degrees
#from mathutils import Matrix, Euler



scene = bge.logic.getCurrentScene()
sun = scene.objects['Sun']
camera = scene.active_camera
fov = camera.fov  # degree of view of camera
camera_empty = scene.objects['player_camera_empty']
weight_backup = camera_empty['weight']  # нужна для функции
weight_2_backup = camera_empty['weight_2']  # нужна для функции
step = 0.006  # step for gradually changing weight value
contr = bge.logic.getCurrentController()




def scattering():
	'''This is the main function, which is called time to time from object.
	It calles all other functions.
	'''
	if scattering_on_off():
		contr.activate('scattering')
		if camera_empty['weight'] < weight_backup:
			camera_empty['weight'] += step
			
		if camera_empty['weight_2'] >= weight_2_backup:
			camera_empty['weight_2'] -= step	
		if camera_empty['weight_2'] <= 0.0:
			contr.activate('remove_scattering_2')
	else:
		if camera_empty['weight'] > 0.0:
			camera_empty['weight'] -= step
		if camera_empty['weight'] <= 0.0:
			contr.activate('remove_scattering')
			
		contr.activate('scattering_2')
		if camera_empty['weight_2'] < weight_2_backup:
			camera_empty['weight_2'] += step
			
	change_screen_x_coordinates()
	change_screen_y_coordinates()
		
			
		


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
	global camera_empty
	#if camera.pointInsideFrustum(sun.worldPosition):  # ranshe bylo
	vector = camera_empty.getVectTo(sun)[2]
	x = fov / 180  # po proporcii
	
	if vector.x >= 0:  # togda solnce szadi kamery
		#print('true')
		return True
	else:
		return False
	#print(weight_backup, camera_empty['weight'])


def scattering_2_on_off():
	global camera_empty
	#if camera.pointInsideFrustum(sun.worldPosition):  # ranshe bylo
	vector = camera_empty.getVectTo(sun)[2]
	x = fov / 180  # po proporcii
	
	if vector.x >= 0:  # togda solnce szadi kamery
		#print('true')
		return True
	else:
		return False
	#print(weight_backup, camera_empty['weight'])


def change_screen_x_coordinates():
	'''
	1. Puskaem vektor (lokalnyi, tak kak kamera vertitsia) ot camery do solnca.
	2. Poluchaem Y vektora (X displeia kamery).
	3. X >= 0 (solnce speredi ili sboku), togda punkt 4, esli X < 0 (solnce szadi) - 5.
	4. Tochku centra (O) smeschaem vniz i sootvetstvenno meniaem z. Z i est iskomaia koordinata X.
	5. -Z iz punkta 4 budet iskomoy koordinatoi X.
	'''
	vect = camera_empty.getVectTo(sun)[2]
	x = vect[0]  # na sluchai punkta 3 (razvorota kamery)
	y = - vect[1]  # Y 3d prostranstva i est X displeia, "-" tak kak uvelichenie na ekrane idet v druguiu storonu
	#print('sun local y = ', y)
	
	if x >= 0:  # esli solnce speredi
		x = (y*fov) / fov
		x += 0.5  # 0.5 eto celaia vysota (1) delim na 2
	
		camera_empty['x'] = x
	else:  # solnce szadi
		x = (y*fov) / fov
		x += 0.5  # 0.5 eto celaia vysota (1) delim na 2
	
		camera_empty['x'] = 1 - x
	
	#print('x = ', x)


def change_screen_y_coordinates():
	'''
	1. Puskaem vektor (lokalnyi, tak kak kamera vertitsia) ot camery do solnca.
	2. Poluchaem Z vektora.
	3. Esli ugol mezhdu X i luchem k solncu <= 90 gradusov, togda punkt 4, esli bolshe - 5.
	3. Tochku centra (O) smeschaem vniz i sootvetstvenno meniaem z. Z i est iskomaia koordinata Y.
	'''
	vect = camera_empty.getVectTo(sun)[2]
	x = vect[0]  # na sluchai punkta 3 (razvorota kamery)
	z = vect[2]  # Z 3d prostranstva i est Y displeia
	#print('sun local z = ', z)
	
	if x >= 0:  # esli solnce popadaet v kameru
		y = (z*fov) / fov
		y += 0.5  # 0.5 eto celaia vysota (1) delim na 2
	
		camera_empty['y'] = y
	else:  # solnce szadi
		y = (z*fov) / fov
		y += 0.5  # 0.5 eto celaia vysota (1) delim na 2
	
		camera_empty['y'] = 1 - y
	#print('y = ', y)
	
	
def check_contact_with_sun():
	'''Iz treh tochek puskaet luchi k solncu. Esli vse vstrechiaiut pregradu - plavno
	vykliuchaem sheider (umenshaiem parametr "weight").
	'''
	'''camera.rayCast(sun, camera, 0, '', 0, 0, 0, 0)'''
	return True
	pass
	
	
scattering()