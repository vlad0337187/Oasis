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

Author: Vladislav Naumov. naumovvladislav@list.ru; github.com/vlad1777d; vk.com/naumovvladislav
License: CC-BY. To use this under other license contact author.

Revision: 5
'''
'''
What to do:
	- change module to use scene.active_camera directly and remove active camera's variable and refresh_camera() function.
	- correct randrange
'''



import bge
import random  # for receive_random_uv_coordinates()
import bpy  # for check_pixel() and grass_masks
import humanity  # for receive_point() for random.randrange()




scene = bge.logic.getCurrentScene()
owner = bge.logic.getCurrentController().owner  # for receive_uv() for .rayCast()


current_camera = scene.active_camera
camera_position = scene.active_camera.worldPosition



square_size = 5  # размер квадрата для помещения травы. Всего их 9 штук, камера всегда находится над центральным.
grass_amount = 20  # amount of grass objects in one square
hysteresis = 0.3  # размер, на который нужно пройти больше расстояние за границу квадрата, чтобы поменять квадраты. Нужен для того чтобы не было рывков и постоянных подгрузок, если персонаж стоит на краю и ходит туда-сюда.
distance_to_change = (square_size / 2) + hysteresis  # расстояние, на которое должен ГГ пройти чтобы поменялись квадраты
height_for_ray = 200  # height, from which ray is casted towards ground for placing grass. No ray - no grass. If ray is below ground - no grass.


squares = {}


# Список объектов состоит из кортежей: (имя_объекта_травы, коефициент). Коефициент отображает вероятность появления
grass_objects = [('grass_1_armature', 5), ('grass_2_armature', 1), ('grass_3_armature', 5), ('grass_4_armature', 10), ('grass_6_armature', 100), ('grass_dry', 10), ('grass_liana', 10), ('grass_violent', 20)]

grass_with_accounted_probabilities = tuple((x for x, y in grass_objects for i in range(y)))  # calculated automatically. Format: ['o1', 'o1', 'o1', 'o2', 'o2']. Amount of objects equals on possiblity of their appearance. Than object is chosen automatically with random int from 0 to amount of objects.


grass_masks = {'ground': bpy.data.images.get('ground_grass_mask_v2.png')}  # contains keys: "name_of_ground_object", value: mask image object

masks_sizes = {k:(v.size[0], v.size[1]) for k, v in grass_masks.items()}  # calculated automatically. Key - name of object, value - tuple of it's width and height








def grass():
	'''Main function.
	Please, use change_squares() instead of it.
	'''
	pass




class cell():
	def __init__(self, *coordinates):
		'''coordinates - x and y coordinates of cell. Z value will be ignored.
		'''
		if coordinates:
			self.x = coordinates[0][0]
			self.y = coordinates[0][1]
		self.objects = []




def refresh_camera():
	'''Указывает данному модулю на текущую камеру.
	(нужно если таковая была изменена во время игры) (v1)
	'''
	global current_camera, camera_position
	current_camera = scene.active_camera
	camera_position = current_camera.WorldPosition








def create_squares():
	'''Создает переменные для квадратов. Вида [[координаты], [список объектов травы]].
	Координаты - список из трех чисел: x, y, z. Доступ можно получить как по номерам,так и по буквам.
	Объект травы - либо меш, либо объект арматуры, на который прикреплен меш.
	rev1
	'''
	global squares
	
	squares[5] = cell(camera_position)  # creates first, as other depend on it
	
	squares[1] = cell((squares[5].x + square_size, squares[5].y + square_size))
	squares[2] = cell((squares[5].x + square_size, squares[5].y))
	squares[3] = cell((squares[5].x + square_size, squares[5].y - square_size))
	squares[4] = cell((squares[5].x, squares[5].y + square_size))
	
	squares[6] = cell((squares[5].x, squares[5].y - square_size))
	squares[7] = cell((squares[5].x - square_size, squares[5].y + square_size))
	squares[8] = cell((squares[5].x - square_size, squares[5].y))
	squares[9] = cell((squares[5].x - square_size, squares[5].y - square_size))
	
	place_objects(1, 2, 3, 4, 5, 6, 7, 8, 9)




def change_squares():
	'''Основная функция.
	Если передвинулся в сторону любую больше чем на 5 метров, тогда убираем лишние квадраты и рисуем недостающие.
	rev1
	'''
	print('change_squares()')
	if where_was_the_step() == 1:  # вверх-влево
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
		
	elif where_was_the_step() == 2:  # вверх-посредине
		remove_objects(7, 8, 9)
		
		squares[7] = squares[4]
		squares[8] = squares[5]
		squares[9] = squares[6]
		squares[4] = squares[1]
		squares[5] = squares[2]
		squares[6] = squares[3]
		
		squares[1] = cell((squares[5].x + step, squares[5].y + step))
		squares[2] = cell((squares[5].x + step, squares[5].y))
		squares[3] = cell((squares[5].x + step, squares[5].y - step))
		
		place_objects(1, 2, 3)
		
	elif where_was_the_step() == 3:  # вверх-вправо
		remove_objects(1, 4, 7, 8, 9)
		
		squares[7] = squares[5]
		squares[8] = squares[6]
		squares[4] = squares[2]
		squares[5] = squares[3]
		
		squares[1] = cell((squares[5].x + step, squares[5].y + step))
		squares[2] = cell((squares[5].x + step, squares[5].y))
		squares[3] = cell((squares[5].x + step, squares[5].y - step))
		squares[6] = cell((squares[5].x, squares[5].y - step))
		squares[9] = cell((squares[5].x - step, squares[5].y - step))
		
		place_objects(1, 2, 3, 6, 9)
		
	elif where_was_the_step() == 4:  # посредине-влево
		remove_objects(3, 6, 9)
		
		squares[9] = squares[8]
		squares[6] = squares[5]
		squares[3] = squares[2]
		squares[8] = squares[7]
		squares[5] = squares[4]
		squares[2] = squares[1]
		
		squares[1] = cell((squares[5].x + step, squares[5].y + step))
		squares[4] = cell((squares[5].x, squares[5].y + step))
		squares[7] = cell((squares[5].x - step, squares[5].y + step))
		
		place_objects(1, 4, 7)
		
	elif where_was_the_step() == 5:  # посредине-посредине (didn't move)
		pass
	elif where_was_the_step() == 6:  # посредине-вправо
		remove_objects(1, 4, 7)
		
		squares[7] = squares[8]
		squares[4] = squares[5]
		squares[1] = squares[2]
		squares[8] = squares[9]
		squares[5] = squares[6]
		squares[2] = squares[3]
		
		squares[3] = cell((squares[5].x + step, squares[5].y - step))
		squares[6] = cell((squares[5].x, squares[5].y - step))
		squares[9] = cell((squares[5].x - step, squares[5].y - step))
		
		place_objects(3, 6, 9)
		
	elif where_was_the_step() == 2:  # вниз-влево
		remove_objects(1, 2, 3, 6, 9)
		
		squares[3] = squares[5]
		squares[6] = squares[8]
		squares[2] = squares[4]
		squares[5] = squares[7]
		
		squares[1] = cell((squares[5].x + step, squares[5].y + step))
		squares[4] = cell((squares[5].x, squares[5].y + step))
		squares[7] = cell((squares[5].x - step, squares[5].y + step))
		squares[8] = cell((squares[5].x - step, squares[5].y))
		squares[9] = cell((squares[5].x - step, squares[5].y - step))
		
		place_objects(1, 4, 7, 8, 9)
		
	elif where_was_the_step() == 2:  # вниз-посредине
		remove_objects(1, 2, 3, 6, 9)
		
		squares[1] = squares[4]
		squares[2] = squares[5]
		squares[3] = squares[6]
		squares[4] = squares[7]
		squares[5] = squares[8]
		squares[6] = squares[9]
		
		squares[7] = cell((squares[5].x - step, squares[5].y + step))
		squares[8] = cell((squares[5].x - step, squares[5].y))
		squares[9] = cell((squares[5].x - step, squares[5].y - step))
		
		place_objects(7, 8, 9)
		
	elif where_was_the_step() == 2:  # вниз-вправо
		remove_objects(1, 2, 3, 4, 7)
		
		squares[1] = squares[5]
		squares[2] = squares[6]
		squares[4] = squares[8]
		squares[5] = squares[9]
		
		squares[3] = cell((squares[5].x + step, squares[5].y - step))
		squares[6] = cell((squares[5].x, squares[5].y - step))
		squares[7] = cell((squares[5].x - step, squares[5].y + step))
		squares[8] = cell((squares[5].x - step, squares[5].y))
		squares[9] = cell((squares[5].x - step, squares[5].y - step))
		
		place_objects(3, 6, 7, 8, 9)
	
	print('change_squares() finished')




def where_was_the_step():
	'''Calculates, was character moved to another square, or not.
	If yes - returns the direction.
	Calculates moving according to "distance_to_change", which includes
	hysteresis.
	'''
	print('where_was_the_step()')
	if camera_position.x - squares[5].x > distance_to_change:  # to top
		if camera_position.y - squares[5].y > distance_to_change:  # to top-left
			return 1
		if camera_position.y - squares[5].y < distance_to_change:  # to top-right
			return 3
		else:  # to top-middle
			return 2
	elif camera_position.x < distance_to_change:  # to bottom
		if camera_position.y - squares[5].y > distance_to_change:  # to bottom-left
			return 7
		if camera_position.y - squares[5].y < distance_to_change:  # to bottom-right
			return 9
		else:  # to bottom-middle
			return 8
	else:  # to middle
		if camera_position.y - squares[5].y > distance_to_change:  # to middle-left
			return 4
		if camera_position.y - squares[5].y < distance_to_change:  # to middle-right
			return 6
		else:  # to middle-middle
			return 5
	
	print('where_was_the_step() finished')








def place_objects(*_squares):
	'''Places randomly chosen grass objects into randomly chosen places
	in given squares.
	rev. 1
	'''
	print('place_objects()')
	for square in _squares:
		
		for count in range(grass_amount):
			point, U, V, ground = receive_point(square)
			
			if ground:
				pixel_number = receive_pixel_number(U, V, ground)
				color = check_pixel(pixel_number, ground)
				
				if color >= 0.2:
					grass = what_to_place()
					added = scene.addObject(grass)
					added.worldPosition = point
	print('place_objects()')




def what_to_place():
	'''Returns object, which will be spawned.
	It chooses object from the list of availible objects,
	depending on it's specified probablibity.
	'''
	number = random.randint(0, len(grass_with_accounted_probabilities) - 1)
	return grass_with_accounted_probabilities[number]


def receive_point(square):
	'''Receives random point (coordinates) for grass in specified square.
	Receives them it's UV coordinates (from 0 to 1).
	'''
	coord_x = random.choise(humfrange(squares[square].x + square_size / 2, squares[square].x - square_size / 2, 0.01))
	coord_y = random.choise(humfrange(squares[square].y + square_size / 2, squares[square].y - square_size / 2, 0.01))
	
	point_from = (coord_x, coord_y, height_for_ray)
	point_to = (coord_x, coord_y, 0)
	answer = owner.rayCast(point_from, point_to, 0, 'ground', 0, 1, 2, 0b1111111111111111)  # owner because some object needs to be there
	
	U = answer[4][0]
	V = answer[4][1]
	obj = answer[0]
	point = answer[1]
	
	return point, U, V, obj


def receive_pixel_number(U, V, ground):
	'''Receives index of appropriate to UV coordinates pixel on mask image.
	Returns int: index of pixel in list of pixels.
	'''
	mask_width, mask_height = masks_sizes[str(ground)][0], masks_sizes[str(ground)][1]
	
	px_horizontal = int(U * mask_width) # we count by proportion
	px_vertical = int(V * mask_height)  # U - width, V - height
	
	px_ordinal_number = (mask_width * (px_vertical - 1)) + px_horizontal  # from 512x512 image
	pixel_number = (px_ordinal_number * 4)  # *4 - RGBA (or ARGB) (x4 of each color);
	# we don't make -1 because in 0 there is alpha value.
	
	return pixel_number


def check_pixel(pixel_number, ground):
	'''Check appropriate mask pixel: is it white (is there present grass).
	Returns: True or False.
	'''
	mask = grass_masks['{0}'.format(str(ground))]
	color = mask.pixels[pixel_number]
	
	return color








def remove_objects(*squares):
	'''Вызывает метод завершения у объектов травы в данном квадрате вида: 
	[[координаты], [список объектов травы]].
	Вызывается из step_forward_left(), которая вызывается из change_squares().
	'''
	print('remove_objects()')
	if not squares:
		print('remove_objects(): Squares with grass are absent!')
		return

	for square in squares:
		if not len(square.objects):  # no grass in cell
			print('remove_objects(): Squares with grass are empty!')
			return
		else:  # grass is present
			for obj in square.objects():
				delete_recursive(obj)
	print('remove_objects() finished')


def delete_recursive(obj):
	'''Recursivly deletes objects and all their children.
	rev1
	'''
	print('delete_recursive()')
	if obj.children:
		for child in obj.children:
			delete_recursive(child)
		print('deleting', obj)
		obj.endObject()
	else:
		print('deleting', obj)
		obj.endObject()
	print('delete_recursive() finished')








create_squares()  # при первом запуске модуля
print('Module "grass.py" loaded. Squares created.')