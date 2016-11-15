'''Grass placing module.
Places randomly grass from hidden layer to ground near active camera.
It launches certain amount of times per second.
(by default - from "Logic_Cube" object)


For work needed:
	-object with "ground" property (better with not False value, but not necessary).
	 This object must have UV map.
	-mask of grass to this object (black and white image, white - grass is present, 
	 black - absent.
	-add names of objects, on which to place grass, and their mask's names to dict
	 "grass_masks".
	-add names of grass objects and possiblity of their appearance to "list grass_objects".

How to work with it:
	-launch main function of this script every certain amount of time (maybe per second).


Way of working:
	Totally there are 9 squares for placing grass, player is always above the central one,
	when he'll go into another square (non-central),
	than those square becomes new central square.
	Extra squares are removed, new ones are added for scheme to be such:
		
	0 0 0
	0 1 0
	0 0 0 (1 - place, where the player is).
	
	, or such:
	tl tm tr
	ml mm mr
	bl bm br
	
	, but in code they are marked so:
	1 2 3
	4 5 6
	7 8 9
	
	Grass objects are removed from removed squares.
	
	Points, where to place grass, are received by ray down from place,
	guaranteed above the higest point of ground object.
	
	Точки, где рисовать траву получаются пусканием лучей вниз от камеры. Эти лучи также получают u и v координаты точки, куда он упал, на текстуре. Если в этой точке на запеченной текстуре будет зеленый цвет, тогда мы можем расположить там траву. Если нет - то не можем.

Коротко о технической реализации:
	-получаем изображение: a = bpy.data.images['image1.png']
	-получаем все его пиксели в одну строку: p = a.pixels()
	(пикселей в 4 раза больше: r,g,b,a; и т.д., и все в строку.
	Нужно будет сопоставлять с шириной и высотой картинки)	

Author: Vladislav Naumov. naumovvladislav@list.ru; https://github.com/vlad1777d; https://vk.com/naumovvladislav
License: CC-BY. To use this under other license contact author.

What to do:
	-make corrections from vk.com

Revision: 12
'''




import bge
import random  # for receive_random_uv_coordinates()
import bpy  # for check_pixel() and grass_masks
from humanity import *  # for receive_point() for random.choise()
import array  # for converting masks with transform_grass_masks_to_arrays()
from mathutils import Euler, Vector  # for vectors for normal_to_xyz_rot()
import math  # for calculating rotation in normal_to_xyz_rot()




scene = bge.logic.getCurrentScene()
owner = bge.logic.getCurrentController().owner  # for receive_uv() for .rayCast()




square_size = 25  # размер квадрата для помещения травы. Всего их 9 штук, камера всегда находится над центральным.
hysteresis = 0.4  # размер, на который нужно пройти больше расстояние за границу квадрата, чтобы поменять квадраты. Нужен для того чтобы не было рывков и постоянных подгрузок, если персонаж стоит на краю и ходит туда-сюда.
distance_to_change = (square_size / 2) + hysteresis  # расстояние, на которое должен ГГ пройти чтобы поменялись квадраты
#distance_to_change = square_size
height_for_ray = 10  # height, from which ray is casted towards ground for placing grass. camera position height is added to this value
grass_amount = 40  # amount of grass objects in one square


squares = {}  # dict with square objects


# Список объектов состоит из кортежей: (имя_объекта_травы, коефициент). Коефициент отображает вероятность появления
grass_objects = [('grass_main_armature.002', 100), ('grass_1_armature', 5), ('grass_2_armature', 1), ('grass_3_4_armature', 5), ('grass_4_armature', 10), ('grass_6_armature', 10), ('grass_dry', 10), ('grass_liana', 5), ('grass_violent', 5)]

grass_with_accounted_probabilities = tuple((x for x, y in grass_objects for i in range(y)))  # calculated automatically. Format: ['o1', 'o1', 'o1', 'o2', 'o2']. Amount of objects equals on possiblity of their appearance. Than object is chosen automatically with random int from 0 to amount of objects.

# here are the objects, which will rotate according to the ground's slope
# (it's normal in that point)
grass_objects_align_to_ground_slope = ['grass_main_armature.002']


grass_masks = {'ground': bpy.data.images.get('ground_grass_mask_v2.png')}  # contains keys: "name_of_ground_object", value: mask image object
#grass_masks['ground'] = bpy.data.images.get('ground_grass_mask_v3.png')

masks_sizes = {k:(v.size[0], v.size[1]) for k, v in grass_masks.items()}  # calculated automatically. Key - name of object, value - tuple of it's width and height








# for TESTING only
def print_grass():  # not used now
	print('Current grass:\n',
	'Square 1 objects(total: {0}):'.format(len(squares[1].objects)), squares[1].objects,
	'Square 2 objects(total: {0}):'.format(len(squares[2].objects)), squares[2].objects,
	'Square 3 objects(total: {0}):'.format(len(squares[3].objects)), squares[3].objects,
	'Square 4 objects(total: {0}):'.format(len(squares[4].objects)), squares[4].objects,
	'Square 5 objects(total: {0}):'.format(len(squares[5].objects)), squares[5].objects,
	'Square 6 objects(total: {0}):'.format(len(squares[6].objects)), squares[6].objects,
	'Square 7 objects(total: {0}):'.format(len(squares[7].objects)), squares[7].objects,
	'Square 8 objects(total: {0}):'.format(len(squares[8].objects)), squares[8].objects, 
	'Square 9 objects(total: {0}):'.format(len(squares[9].objects)), squares[9].objects)
	print('TOTAL OBJECTS:', len(squares[1].objects) + len(squares[2].objects) + 
	len(squares[3].objects) + len(squares[4].objects) + len(squares[5].objects) + 
	len(squares[6].objects) + len(squares[7].objects) + len(squares[8].objects) + 
	len(squares[9].objects))




def grass():  # not used now
	'''Main function.
	Please, use change_squares() instead of it.
	'''
	if queue():
		queue('+1')




class cell():
	def __init__(self, *coordinates):
		'''coordinates - x and y coordinates of cell. Z value will be ignored.
		'''
		if coordinates:
			self.x = coordinates[0][0]
			self.y = coordinates[0][1]
		self.objects = []










def create_squares():
	'''Создает переменные для квадратов. Вида [[координаты], [список объектов травы]].
	Координаты - список из трех чисел: x, y, z. Доступ можно получить как по номерам,так и по буквам.
	Объект травы - либо меш, либо объект арматуры, на который прикреплен меш.
	rev1
	'''
	#print('create_squares()')
	global squares
	
	squares[5] = cell(scene.active_camera.worldPosition)  # creates first, as other depend on it
	
	squares[1] = cell((squares[5].x + square_size, squares[5].y + square_size))
	squares[2] = cell((squares[5].x + square_size, squares[5].y))
	squares[3] = cell((squares[5].x + square_size, squares[5].y - square_size))
	squares[4] = cell((squares[5].x, squares[5].y + square_size))
	
	squares[6] = cell((squares[5].x, squares[5].y - square_size))
	squares[7] = cell((squares[5].x - square_size, squares[5].y + square_size))
	squares[8] = cell((squares[5].x - square_size, squares[5].y))
	squares[9] = cell((squares[5].x - square_size, squares[5].y - square_size))
	
	place_objects(1, 2, 3, 4, 5, 6, 7, 8, 9)
	#print('create_squares() finished')




def change_squares():
	'''Основная функция.
	Если передвинулся в сторону любую больше чем на 5 метров, тогда убираем лишние квадраты и рисуем недостающие.
	rev1
	'''
	global squares
	#print('change_squares()')
	step = where_was_the_step()
	#print('step was to {0}'.format(step))
	
	if step == 1:  # вверх-влево
		remove_objects(3, 6, 7, 8, 9)  # before new links will created
		
		squares[9] = squares[5]
		squares[5] = squares[1]
		squares[8] = squares[4]
		squares[6] = squares[2];  # old things reuse
		
		squares[1] = cell((squares[5].x + square_size, squares[5].y + square_size))
		squares[2] = cell((squares[5].x + square_size, squares[5].y))
		squares[3] = cell((squares[5].x + square_size, squares[5].y - square_size))
		squares[4] = cell((squares[5].x, squares[5].y + square_size))
		squares[7] = cell((squares[5].x - square_size, squares[5].y + square_size))
		
		place_objects(1, 2, 3, 4, 7)
		
	elif step == 2:  # вверх-посредине
		remove_objects(7, 8, 9)
		
		squares[7] = squares[4]
		squares[8] = squares[5]
		squares[9] = squares[6]
		squares[4] = squares[1]
		squares[5] = squares[2]
		squares[6] = squares[3]
		
		squares[1] = cell((squares[5].x + square_size, squares[5].y + square_size))
		squares[2] = cell((squares[5].x + square_size, squares[5].y))
		squares[3] = cell((squares[5].x + square_size, squares[5].y - square_size))
		
		place_objects(1, 2, 3)
		
	elif step == 3:  # вверх-вправо
		remove_objects(1, 4, 7, 8, 9)
		
		squares[7] = squares[5]
		squares[8] = squares[6]
		squares[4] = squares[2]
		squares[5] = squares[3]
		
		squares[1] = cell((squares[5].x + square_size, squares[5].y + square_size))
		squares[2] = cell((squares[5].x + square_size, squares[5].y))
		squares[3] = cell((squares[5].x + square_size, squares[5].y - square_size))
		squares[6] = cell((squares[5].x, squares[5].y - square_size))
		squares[9] = cell((squares[5].x - square_size, squares[5].y - square_size))
		
		place_objects(1, 2, 3, 6, 9)
		
	elif step == 4:  # посредине-влево
		remove_objects(3, 6, 9)
		
		squares[9] = squares[8]
		squares[6] = squares[5]
		squares[3] = squares[2]
		squares[8] = squares[7]
		squares[5] = squares[4]
		squares[2] = squares[1]
		
		squares[1] = cell((squares[5].x + square_size, squares[5].y + square_size))
		squares[4] = cell((squares[5].x, squares[5].y + square_size))
		squares[7] = cell((squares[5].x - square_size, squares[5].y + square_size))
		
		place_objects(1, 4, 7)
		
	elif step == 5:  # посредине-посредине (didn't move)
		pass
	elif step == 6:  # посредине-вправо
		remove_objects(1, 4, 7)
		
		squares[7] = squares[8]
		squares[4] = squares[5]
		squares[1] = squares[2]
		squares[8] = squares[9]
		squares[5] = squares[6]
		squares[2] = squares[3]
		
		squares[3] = cell((squares[5].x + square_size, squares[5].y - square_size))
		squares[6] = cell((squares[5].x, squares[5].y - square_size))
		squares[9] = cell((squares[5].x - square_size, squares[5].y - square_size))
		
		place_objects(3, 6, 9)
		
	elif step == 7:  # вниз-влево
		remove_objects(1, 2, 3, 6, 9)
		
		squares[3] = squares[5]
		squares[6] = squares[8]
		squares[2] = squares[4]
		squares[5] = squares[7]
		
		squares[1] = cell((squares[5].x + square_size, squares[5].y + square_size))
		squares[4] = cell((squares[5].x, squares[5].y + square_size))
		squares[7] = cell((squares[5].x - square_size, squares[5].y + square_size))
		squares[8] = cell((squares[5].x - square_size, squares[5].y))
		squares[9] = cell((squares[5].x - square_size, squares[5].y - square_size))
		
		place_objects(1, 4, 7, 8, 9)
		
	elif step == 8:  # вниз-посредине
		remove_objects(1, 2, 3)
		
		squares[1] = squares[4]
		squares[2] = squares[5]
		squares[3] = squares[6]
		squares[4] = squares[7]
		squares[5] = squares[8]
		squares[6] = squares[9]
		
		squares[7] = cell((squares[5].x - square_size, squares[5].y + square_size))
		squares[8] = cell((squares[5].x - square_size, squares[5].y))
		squares[9] = cell((squares[5].x - square_size, squares[5].y - square_size))
		
		place_objects(7, 8, 9)
		
	elif step == 9:  # вниз-вправо
		remove_objects(1, 2, 3, 4, 7)
		
		squares[1] = squares[5]
		squares[2] = squares[6]
		squares[4] = squares[8]
		squares[5] = squares[9]
		
		squares[3] = cell((squares[5].x + square_size, squares[5].y - square_size))
		squares[6] = cell((squares[5].x, squares[5].y - square_size))
		squares[7] = cell((squares[5].x - square_size, squares[5].y + square_size))
		squares[8] = cell((squares[5].x - square_size, squares[5].y))
		squares[9] = cell((squares[5].x - square_size, squares[5].y - square_size))
		
		place_objects(3, 6, 7, 8, 9)
	
	elif step == 10:  # step was too large
		remove_objects(1, 2, 3, 4, 5, 6, 7, 8, 9)
		create_squares()
	
	#print('change_squares() finished')




def where_was_the_step():
	'''Calculates, was character moved to another square, or not.
	If yes - returns the direction.
	Calculates moving according to "distance_to_change", which includes
	hysteresis.
	'''
	#print('where_was_the_step()')
	camera_position = scene.active_camera.worldPosition
	
	# if too large distance:
	values_x = abs(squares[5].x), abs(camera_position.x)
	values_y = abs(squares[5].y), abs(camera_position.y)
	if max(values_x) - min(values_x) > distance_to_change * 2:
		return 10  # 10 means that step was too far
	elif max(values_y) - min(values_y) > distance_to_change * 2:
		return 10
	
	# general steps:
	if camera_position.x - squares[5].x > distance_to_change:  # to top
		if camera_position.y - squares[5].y > distance_to_change:  # to top-left
			return 1
		elif squares[5].y - camera_position.y > distance_to_change:  # to top-right
			return 3
		else:  # to top-middle
			return 2
	elif squares[5].x - camera_position.x > distance_to_change:  # to bottom
		if camera_position.y - squares[5].y > distance_to_change:  # to bottom-left
			return 7
		elif squares[5].y - camera_position.y > distance_to_change:  # to bottom-right
			return 9
		else:  # to bottom-middle
			return 8
	else:  # to middle
		if camera_position.y - squares[5].y > distance_to_change:  # to middle-left
			return 4
		elif squares[5].y - camera_position.y > distance_to_change:  # to middle-right
			return 6
		else:  # to middle-middle
			return 5








def place_objects(*_squares):
	'''Places randomly chosen grass objects into randomly chosen places
	in given squares.
	rev. 3
	'''	
	#print('place_objects() started')
	for square_number in _squares:
		
		for count in range(grass_amount):
			ground_obj, U, V, point, normal  = receive_point(square_number)
			#point = (-21.23577, 23.35219, 32.67959)
			#U = 0.5; V = 0.5; ground = scene.objects['ground']
			#print('hitnormal =', normal)
			
			if ground_obj:
				#print('ground')
				pixel_number = receive_pixel_number(U, V, ground_obj)
				#color = check_pixel(pixel_number, ground)
				if check_pixel(pixel_number, ground_obj):
					#print('True')
					grass = what_to_place()
					added = scene.addObject(grass)
					added.worldPosition = point
					if str(grass) in grass_objects_align_to_ground_slope:
						added.worldOrientation = normal_to_xyz_rot(normal)
					
					random_rot_value = random.choice((0.7, 0.8, 0.9, 1.0, 1.1, 1.2))
					random_scale_value = random.choice((0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3))
					added.worldOrientation.rotate(Euler((0, 0 ,0.1 * random_rot_value)))
					added.worldScale = Vector((1 * random_scale_value, 1 * random_scale_value, 1 * random_scale_value))
					squares[square_number].objects.append(added)
					#queue('store', (grass, point, square_number))
					#print('added something')
			
	#print('place_objects() finished')




def what_to_place():
	'''Returns object, which will be spawned.
	It chooses object from the list of availible objects,
	depending on it's specified probablibity.
	'''
	number = random.randint(0, len(grass_with_accounted_probabilities) - 1)
	return grass_with_accounted_probabilities[number]


def receive_point(square_number):
	'''Receives random point (coordinates) for grass in specified square.
	Receives them it's UV coordinates (from 0 to 1).
	'''
	coord_x = random.choice(drange(str(squares[square_number].x - square_size / 2), str(squares[square_number].x + square_size / 2), '0.01', 'float'))
	coord_y = random.choice(drange(str(squares[square_number].y - square_size / 2), str(squares[square_number].y + square_size / 2), '0.01', 'float'))
	#coord_x = 0; coord_y = 0
	#print('coord_x =', coord_x, 'coord_y =', coord_y)
	#print('height_for_ray =', height_for_ray)
	
	point_from = (coord_x, coord_y, scene.active_camera.worldPosition.z + height_for_ray)
	point_to = (coord_x, coord_y, 0)
	answer = owner.rayCast(point_from, point_to, 0, 'ground', 1, 1, 2, 0b1111111111111111)  # owner because some object needs to be there
	
	if answer[4]:  # can be None >> error "'NoneType' object is not subscriptable"
		U = answer[4][0]
		V = answer[4][1]
	else:
		U, V = None, None
	ground_obj, point, normal = answer[0], answer[1], answer[2]
	
	return ground_obj, U, V, point, normal


def receive_pixel_number(U, V, ground):
	'''Receives index of appropriate to UV coordinates pixel on mask image.
	Returns int: index of pixel in list of pixels.
	'''
	mask_width, mask_height = masks_sizes[str(ground)][0], masks_sizes[str(ground)][1]
	
	px_horizontal = int(U * mask_width) # we count by proportion
	px_vertical = int(V * mask_height)  # U - width, V - height
	
	px_ordinal_number = (mask_width * (px_vertical - 1)) + px_horizontal  # from 512x512 image
	pixel_number = (px_ordinal_number * 4)  # *4 - RGBA (or ARGB) (x4 of each color);
	#pixel_number = px_ordinal_number  # for arrays in while cycle
	# we don't make -1 because in 0 there is alpha value.
	
	return pixel_number


def check_pixel(pixel_number, ground):
	'''Check appropriate mask pixel: is it white (is there present grass).
	Returns: True or False (0 or 1).
	'''
	mask = grass_masks['{0}'.format(str(ground))]
	#color = mask.pixels[pixel_number]  # for bpy.data.image
	color = mask[pixel_number]  # for arrays
	
	#return color
	if color >= 0.98:
		return True
	else:
		return False


def normal_to_xyz_rot(normal):
	'''Transforms unit-vector (with length 1) of normal
	into XYZ rotation angles.
	Positive rotation - by clock arrow.
	Normal orientation of projection - when that axis, that is ortogonal for
	user is it's "-" side to user, "+" side away (except the X axis!!! It's blender's feature.
	Example:
        ^ Z                      ^ Z              ^ Y
        |                        |                |
        |                        |                |
        |                        |                |
        |                        |                |
		O----> X         Y <-----O        X <-----O
	(+Y looks away)  (+X looks away)  (+Z looks away)
	rev.4
	'''
	if normal.z > 0:
		if normal.y > 0:
			rot_x = - math.degrees(math.atan(normal.y / normal.z))
			# here ^ must be "+", but there's an issue (look func. description)
		elif normal.y < 0:
			rot_x =  math.degrees(math.atan((- normal.y) / normal.z))
			# here ^ must be "-", but there's an issue (look func. description)
		else:
			rot_x = 0
		
		if normal.x > 0:
			rot_y = math.degrees(math.atan(normal.x / normal.z))
		elif normal.x < 0:
			rot_y = - math.degrees(math.atan((- normal.x) / normal.z))
		else:
			rot_y = 0
		
	elif normal.z < 0:
		if normal.y > 0:
			rot_x = -90 - math.degrees(math.atan(- normal.z / normal.y))
		elif normal.y < 0:
			rot_x = -180 - math.degrees(math.atan(- normal.y / - normal.z))
		else:
			rot_x = 180
		
		if normal.x > 0:
			rot_y = 90 + math.degrees(math.atan(- normal.z / normal.x))
		elif normal.x < 0:
			rot_y = 180 + math.degrees(math.atan(normal.x / normal.z))
		else:
			rot_y = 180
	
	else:
		if normal.y > 0:
			rot_x = -90
		elif normal.y < 0:
			rot_x = 90
		else:
			rot_x = 0
		
		if normal.x > 0:
			rot_y = 90
		elif normal.x < 0:
			rot_y = -90
		else:
			rot_y = 0
	
	rot_x = math.radians(rot_x)
	rot_y = math.radians(rot_y)
	rot_z = 0  # we do not need to rotate z axis
	rot = Euler((rot_x, rot_y, rot_z))
	return rot








def remove_objects(*_squares):
	'''Вызывает метод завершения у объектов травы в данном квадрате вида: 
	[[координаты], [список объектов травы]].
	Вызывается из step_forward_left(), которая вызывается из change_squares().
	'''
	#print('remove_objects()')
	if not squares:
		print('remove_objects(): Squares with grass are absent!')
		return

	for number in _squares:
		if not len(squares[number].objects):  # no grass in cell
			print('remove_objects(): Squares with grass are empty!')
			continue
		else:  # grass is present
			#queue.freeze = True
			for count in range(len(squares[number].objects)):
				delete_recursive(squares[number].objects[count])
				#queue('remove', squares[number].objects[count])
				#print('deleting', count)
			del squares[number].objects[:]
			#queue.freeze = False
				
	#print('remove_objects() finished')


def delete_recursive(obj):
	'''Recursivly deletes objects and all their children.
	rev1
	'''
	#print('delete_recursive()')
	if obj.children:
		for child in obj.children:
			delete_recursive(child)
		#print('deleting', obj)
		obj.endObject()
		return
	else:
		#print('deleting', obj)
		obj.endObject()
	#print('delete_recursive() finished')








class Queue():  # Is not used now.
	'''receives objects for adding to scene.
	'''
	def __init__(self):
		self.adding_queue = []  # list of tuples: (object_name, point_to_place, square_number)
		self.removing_queue = []  # list of objects to remove
		self.freeze = False
		
	def __call__(self, mode='work', obj=None):
		
		if self.freeze:
			del self.adding_queue[:]
			return
		
		if mode == 'work':
			if len(self.adding_queue):
				added = scene.addObject(self.adding_queue[0][0])
				added.worldPosition = self.adding_queue[0][1]
				squares[self.adding_queue[0][2]].objects.append(added)
				self.adding_queue.pop(0)
			if len(self.removing_queue):
				delete_recursive(self.removing_queue[0])
				self.removing_queue.pop(0)
		elif mode == 'store':
			self.adding_queue.append(obj)
		elif mode == 'remove':
			self.removing_queue.append(obj)








def transform_grass_masks_to_arrays():
	'''Transforms grass masks objects to corresponding arrays.
	Because image objects of bpy are very slow.
	'''
	#print('transforming masks to arrays')
	global grass_masks
	grass_masks_copy = grass_masks.copy()
	
	for key in grass_masks_copy:
		pixels = grass_masks[key].pixels
		mask_array = array.array('f')
		mask_array.extend(pixels)
		grass_masks[key] = mask_array
	#print('transformation finished')

		
queue = Queue()










transform_grass_masks_to_arrays()  # при первом запуске модуля
create_squares()  # при первом запуске модуля
print('Module "grass.py" loaded. Squares created.')