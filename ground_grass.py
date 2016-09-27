'''Располагает случайно траву со скытых слоев рядом с активной камерой на земле.
Запускается раз в 120 секунд по-умолчанию с объекта LogicCube.

Для работы требуется:
	-объект со свойством "ground" (на котором будет трава рисоваться);
	-картинка с запеченной текстурой обеъкта или маски с именем "ground_baked" (или сумма всех масок кроме земли, главное знать, на каких областях должна быть трава) (смотрим в каждой маске, начинающейся с ground_alpha, если эта точка нигде не белая - можно рисовать) (в данный момент трава занимает все место на земле, кроме тех, в чиьх масках есть белый цвет).

Алгоритм работы:
	Всего есть 9 квадратов для размещения травы, игрок всегда находится над центральным, как только он переходит на другой квадрат (не центральный), 
	тот сразу становится новым центральным квадратом. Лишние квадраты удаляются, новые рисуются, чтобы схема 
всегда была такой:
	0 0 0
	0 1 0
	0 0 0 (1 - место расположения игрока).
	
	ВЛ ВС ВП
	СЛ СС СП
	НЛ НС НП (подписал буквами чтобы было понятней).
	Squares in English.
	tl tm tr
	ml mm mr
	bl bm br
	1 2 3
	4 5 6
	7 8 9
	С удаляемых квадратов удаляется трава.
	
	Точки, где рисовать траву получаются пусканием лучей вниз от камеры. Эти лучи также получают u и v координаты точки, куда он упал, на текстуре. Если в этой точке на запеченной текстуре будет зеленый цвет, тогда мы можем расположить там траву. Если нет - то не можем.

Коротко о технической реализации:
	-получаем изображение: a = bpy.data.images['image1.png']
	-получаем все его пиксели в одну строку: p = a.pixels()
	(пикселей в 4 раза больше: r,g,b,a; и т.д., и все в строку.
	Нужно будет сопоставлять с шириной и высотой картинки)	
	
Revision: 2
'''

import bge


scene = bge.logic.getCurrentScene()
current_camera = scene.active_camera
camera_position = scene.active_camera.worldPosition
size = 5  # размер квадрата для помещения травы. Всего их 9 штук, камера всегда находится над центральным.
hysteresis = 0.3  # размер, на который нужно пройти больше расстояние за границу квадрата, чтобы поменять квадраты. Нужен для того чтобы не было рывков и постоянных подгрузок, если персонаж стоит на краю и ходит туда-сюда.
distance_to_change = (square_size / 2) + hysteresis  # расстояние, на которое должен ГГ пройти чтобы поменялись квадраты
squares = {}




class cell():
	def __init__(self, *coordinates):
		'''coordinates - x and y coordinates of cell. Z value will be ignored.
		'''
		if coordinates:
			self.x = coordinates[0][0]
			self.y = coordinates[0][1]
		self.objects = []
		
	def move(self, x, y):
		'''Moves center of cell to need X and Y destance.
		'''
		self.x += x
		self.y += y
		
	def remove_objects(self):
		if self.objects:
			for object in self.objects:
				object.endObject()
		

def grass():
	'''Пока не работает. 
	Возможно в будущем заменим на change_squares().
	'''
	print(scene.objects['ground'].children)
	create_squares()
	pass


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
	v1
	'''
	global squares
	
	squares[1] = cell(camera_position)
	squares[2] = cell(camera_position)
	squares[3] = cell(camera_position)
	
	squares[4] = cell(ccamera_position)
	squares[5] = cell(ccamera_position)
	squares[6] = cell(camera_position)
	
	squares[7] = cell(camera_position)
	squares[8] = cell(camera_position)
	squares[9] = cell(camera_position)
	
	squares[1].x += size; squares[1].y += size; 
	squares[2].x += size;
	squares[3].x += size; squares[3].y -= size;
	
	squares[4].y += size;
	squares[6].y -= size;
	
	squares[7].x -= size; squares[7].y += size;
	squares[8].x -= size;
	squares[9].x -= size; squares[9].y -= size;
	

def change_squares():
	'''Основная функция.
	Если передвинулся в сторону любую больше чем на 5 метров, тогда убираем лишние квадраты и рисуем недостающие.
	v1
	'''
	if where_was_the_step() == 1:  # вверх-влево
		remove_objects(3, 6, 7, 8, 9)  # before new links will created
		
		squares[9] = squares[5]
		squares[5] = squares[1]
		squares[8] = squares[4]
		squares[6] = squares[2];  # old things reuse
		
		squares[1] = cell((squares[5].x + size, squares[5].y + size))
		squares[2] = cell((squares[5].x + size, squares[5].y))
		squares[3] = cell((squares[5].x + size, squares[5].y - size))
		squares[4] = cell((squares[5].x, squares[5].y + size))
		squares[7] = cell((squares[5].x - size, squares[5].y + size))
		
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


def where_was_the_step():
	'''Calculates, was character moved to another square, or not.
	If yes - returns the direction.
	'''
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


def step_forward_left():
	'''Переднюю левую клетку делает центральной. Ненужные удаляем, нужные добавляем.
	Вызывается из change_squares().
	v1
	'''
	pass	


def place_objects():
	pass


def delete_grass_in_squares(*squares):
	'''Вызывает метод завершения у объектов травы в данном квадрате вида: 
	[[координаты], [список объектов травы]].
	Вызывается из step_forward_left(), которая вызывается из change_squares().
	'''
	if not squares: return

	for square in squares:
		try: x[1]
		except IndexError: continue  # если травы в квадрате нету
		for grass_object in square[1]:  # по объектам травы
			if grass_object.children:
				grass_object.children[0].endObject()
			grass_object.endObject()


create_squares()  # при первом запуске модуля
print('Module "ground_grass" loaded.')
