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
	С удаляемых квадратов удаляется трава.
	
	Точки, где рисовать траву получаются пусканием лучей вниз от камеры. Эти лучи также получают u и v координаты точки, куда он упал, на текстуре. Если в этой точке на запеченной текстуре будет зеленый цвет, тогда мы можем расположить там траву. Если нет - то не можем.

Коротко о технической реализации:
	-получаем изображение: a = bpy.data.images['image1.png']
	-получаем все его пиксели в одну строку: p = a.pixels()
	(пикселей в 4 раза больше: r,g,b,a; и т.д., и все в строку.
	Нужно будет сопоставлять с шириной и высотой картинки)	
	
v1
'''

import bge


scene = bge.logic.getCurrentScene()
current_camera = scene.active_camera
camera_position = scene.active_camera.worldPosition
size = 5  # размер квадрата для помещения травы. Всего их 9 штук, камера всегда находится над центральным.
hysteresis = 0.3  # размер, на который нужно пройти больше расстояние за границу квадрата, чтобы поменять квадраты. Нужен для того чтобы не было рывков и постоянных подгрузок, если персонаж стоит на краю и ходит туда-сюда.
distance_to_change = (square_size / 2) + hysteresis  # расстояние, на которое должен ГГ пройти чтобы поменялись квадраты




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
	global vl, vs, vp
	global sl, ss, sp
	global nl, ns, np
	#global squares
	
	vl = cell(camera_position); vs = cell(camera_position); vp = cell(camera_position)
	sl = cell(ccamera_position(; ss = cell(ccamera_position); sp = cell(camera_position)
	nl = cell(camera_position); ns = cell(camera_position); np = cell(camera_position)
	
	vl.x += size; vl.y += size; 
	vs.x += size;
	vp.x += size; vp.y -= size;
	
	sl.y += size;
	sp.y -= size;
	
	nl.x -= size; nl.y += size;
	ns.x -= size;
	np.x -= size; np.y -= size;
	

def change_squares():
	'''Основная функция.
	Если передвинулся в сторону любую больше чем на 5 метров, тогда убираем лишние квадраты и рисуем недостающие.
	v1
	'''
	if camera_position.x - ss.x > distance_to_change:  # вверх
		if camera_position.y - ss.y > distance_to_change:  # вверх-влево
			np = ss; ss = vl; ns = sl; sp = vs;  # old things reuse
			
			vl = cell((ss.x + size, ss.y + size))
			vs = cell((ss.x + size, ss.y))
			vp = cell((ss.x + size, ss.y - size))
			
			sl = cell((ss.x, ss.y + size))
			
			nl = cell((ss.x - size, ss.y + size))
			
			create_objects(vl)
			create_objects(vs)
			create_objects(vp)
			
			create_objects(sl)
			
			create_objects(nl)
			
		if camera_position.y - ss.y < distance_to_change:  # вверх-вправо
			pass
		else:  # вверх-посредине
			nl = sl; ns = ss; np = sl
			sl = vl; ss = vs; sp = vp  # old things reuse
			
			vl = cell((ss.x + step, ss.y + step))
			vs = cell((ss.x + step, ss.y))
			vp = cell((ss.x + step, ss.y - step))
			
			create_objects(vl)
			create_objects(vs)
			create_objects(vp)
	elif camera_position.x < distance_to_change:  # вниз
		if camera_position.y - ss.y > distance_to_change:  # вниз-влево
			pass
		if camera_position.y - ss.y < distance_to_change:  # вниз-вправо
			pass
		else:  # вниз-посредине
			pass
	else:  # посредине
		if camera_position.y - ss.y > distance_to_change:  # посредине-влево
			pass
		if camera_position.y - ss.y < distance_to_change:  # посредине-вправо
			pass
		else:  # посредине-посредине
			pass


def step_forward_left():
	'''Переднюю левую клетку делает центральной. Ненужные удаляем, нужные добавляем.
	Вызывается из change_squares().
	v1
	'''
	pass	


def create_objects():
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
