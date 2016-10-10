#! /usr/bin/env python3
''' 
('RU') Данный модуль заменяет стандартные типы данных последовательностей (списки, кортежи, строки) аналогичными типами данных,
в которых индексация идет не с нуля а с единицы. Пример: a = humlist(1,2,3); print(a[2]) выведет 2.

Содержит типы данных: 
	humlist (аналог списков), humtuple (аналог кортежей), humstr (аналог строк)
Содержит функции:
	humrange (аналог range)

Подключение модуля: 
1) Добавим в sys.path расположение каталога (папки) с данным модулем. 
	Пример 1 (простой):
		import sys
		sys.path.append('/home/user/modules')
	Пример 2 (с относительными путями): 
		import os, sys, inspect
		# realpath() will make your script run, even if you symlink it :)
		cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
		if cmd_folder not in sys.path:
		sys.path.insert(0, cmd_folder)
	Пример 3 (с относительными путями):
		# use this if you want to include modules from a subfolder
		cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
		if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
  Можно не добавлять если данный модуль находится в домашнем каталоге (папке). В некоторых ОС домашний каталог это тот, в котором
  расположен файл с выполняемой программой.
2) Импортируем его: from humanity import *
  или: import humanity


('EN') This module replaces the standard sequence data types (lists, tuples, strings) similar types of data,
in which indexation is not from zero but from one. Example: a = humlist(1,2,3); print(a[2]) will print 2.

Contains data types: 
	humlist (similar to lists), humtuple (similar to tuples), humstr (analogue lines)
Contains functions:
	humrange (analogue range)

Importing module: 
1) Add to sys.path to a directory (folder) with this module. 
	Example 1 (simple):
		import sys
		sys.path.append('/home/user/modules')
	Example 2 (with relative paths): 
		import os, sys, inspect
		# realpath() will make your script run, even if you symlink it :)
		cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
		if cmd_folder not in sys.path:
		sys.path.insert(0, cmd_folder)
	Example 3 (with relative paths):
		# use this if you want to include modules from a subfolder
		cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
		if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
		You can not add if the module is in the home directory (folder). In some operating systems the home directory is the one in which
		is a file with the executable program.
2) Import: import from humanity *
or: import humanity

Revision: 3
'''








def changeIndexes(keys):
	'''('RU') Функция используется в: __getitem__, __setitem__, __delitem__.
	Она смещает в последовательностях номер первого элемента с [0] на [1].
	если в функц. передается один аргумент, он int и пишется в keys
	если пытаешься брать срез, keys присваивается объект среза вида: slice(1, None, None)'''
	''' В других методах не используется, так как там нету объектов среза: slice(1, None, None), там можно просто отнять 1 от индекса или добавить
	
	revision: 3
	'''
	if isinstance(keys, slice):
	
		'''if keys.start == 0:  # проверки:
			raise IndexError('There is no element under index 0')'''
		if keys.step == 0:
			raise ValueError('slice step cannot be zero')

		# обычный порядок всегда, кроме когда есть и 1 и 2, 2 больше 1
		if (keys.start and (keys.stop != None)) and (keys.start > keys.stop):  # обратный порядок
		
			if keys.step == None:  # проверки:
				raise IndexError('Step cannot be default (positive) while reverse order.')
			elif keys.step > 0:
				raise IndexError('Step cannot be positive while reverse order.')
				
			if keys.start > 0:
				start = keys.start - 1
				if keys.stop >= 2:
					stop = keys.stop - 2
				elif 0 <= keys.stop  <= 1:
					stop = None
				else:
					stop = keys.stop
				keys = slice(start, stop, keys.step)
			
		else:  # прямой порядок
			if keys.start:
				if keys.start > 0:
					keys = slice(keys.start - 1, keys.stop, keys.step)
		

	elif isinstance(keys, int): #если нет 'slice(', значит целое число
	
		if keys > 0:
			keys = keys - 1
		elif keys == 0:  # проверки:
			raise IndexError('There is no element under index 0')
	
	return keys







for x in ('list', 'tuple', 'str'):  # __init__ and __new__ methods
	if x == 'list':
		method = '__init__'
		retn = ''
	else:
		method = '__new__'
		retn = 'return '
	exec(
	"""def {x}{method}(self, *something):
		'''('EN') humlist(1,2) > [1, 2]; humlist([1,2]) > [1, 2]; humlist((1,2), (2,3)) > [(1, 2), (2, 3)] 
		('RU') Подобные есть и в humtuple и в humstr, только называется __new__.
		'''	
		
		length = len(something)
		if length > 1:
			{retn}{x}.{method}(self, something) # возвращать ничего не нужно (для базового класса так)
		elif length == 1:
			if something[0].__class__ == tuple:
				{retn}{x}.{method}(self, something[0])
			else:
				{retn}{x}.{method}(self, something)
		else:
			{retn}{x}.{method}(self, something)""".format(x=x, method=method, retn=retn))
else:
	del method, retn, x




def sequence__getitem__(self, keys):
	keys = changeIndexes(keys)
	return self.__class__.__base__.__getitem__(self, keys)

def sequence__setitem__(self, keys, value):
	'''('EN') Set self[key] to value. If A = [1,2,3], than A[1] = 5 will change A to: [5,2,3]
	'''
	keys = changeIndexes(keys)
	self.__class__.__base__.__setitem__(self, keys, value) # keys - итерируемый объект: (slice(1,2,1), ) или (1, )

def sequence__delitem__(self, keys):
	'''('EN') Delete self[key]. If A = [1,2,3], than A[1] = 5 will change A so: [5,2,3]''' 
	keys = changeIndexes(keys)
	self.__class__.__base__.__delitem__(self, keys)




def sequence_get(self, keys):
	'''Get method for sequences.
	Returns value of element on position (keys). If such element is absent - returns None.
	Used in: humlist, humtuple, humstr.
	version: 1
	'''
	try:
		value = self.__getitem__(keys)
	except IndexError:
		value = None
	return value


def sequence_index(self, value, *positions):
	'''Index method for sequences.
	Returns index of element with specified value (optional in positions).
	version: 1
	'''
	
	length = len(positions)
	
	if length >= 3:
		raise TypeError('index() takes at most 3 arguments ({0} given)'.format(length+1))
	elif length == 2:
		start = positions[0] - 1
		end = positions[1]
		return self.__class__.__base__.index(self, value, start, end) + 1
	elif length == 1:
		start = positions[0] - 1
		return self.__class__.__base__.index(self, value, start) + 1
	else:  # если нет вообще позиций
		return self.__class__.__base__.index(self, value) + 1







class humlist(list):
	'''Class, that is the same to list type, but with normal indexes.
	version: 2
	'''

	# Технические методы:
	
	"""def __init__(self, *something):
		'''('EN') humlist(1,2) > [1, 2]; humlist([1,2]) > [1, 2]; humlist((1,2), (2,3)) > [(1, 2), (2, 3)] 
		('RU') Подобные есть и в humtuple и в humstr, только называется __new__.'''
		length = len(something)
		if length > 1:
			list.__init__(self, something) # возвращать ничего не нужно (для базового класса так)
		elif length == 1:
			if something[0].__class__ == tuple:
				list.__init__(self, something[0])
			else:
				list.__init__(self, something)
		else:
			list.__init__(self, something)"""
	__init__ = list__init__
			
	"""try: something[1]; something[0] # если два и более аргумента - else:
		except IndexError: # если нет двух и более:
			try: something[0] # если только один аргумент - else:
			except IndexError: # если ни одного аргумента
				list.__init__(self, something)
			else: # если только один аргумент
				something = something[0]
				list.__init__(self, something)
		else: # если два и более аргумента
			list.__init__(self, something) # возвращать ничего не нужно (для базового класса так)"""
	
	
	__getitem__ = sequence__getitem__
	__setitem__ = sequence__setitem__
	__delitem__ = sequence__delitem__
	
	
	# Нетехнические методы:
	
	def insert(self, position, value):
		position = changeIndexes(position)
		list.insert(self, position, value)
	
	
	index = sequence_index
	get = sequence_get








class humtuple(tuple):
	'''Class, that is the same to tuple type, but with normal indexes.
	version: 2
	'''
	
	# Технические методы:
	
	#def __init__(self, something):
		#У кортежей нет этого метода. Вместо него - __new__. Если добавить __init__ - будут работать оба.
	
	"""def __new__(self, *something): #только init не канает. Походу он вообще тут не работает.
		'''('EN') Analog to __init__ method in humlist class
		('RU') Но они не одинаковы - у каждого свои нюансы.'''
		try: something[1]; something[0] # если два и более аргумента - else:
		except IndexError: # если нет двух и более:
			try: something[0] # если только один аргумент - else:
			except IndexError: # если ни одного аргумента
				return tuple.__new__(self, something)
			else: # если только один аргумент
				something = something[0]
				return tuple.__new__(self, something)
		else: # если два и более аргумента
			return tuple.__new__(self, something) # возвращать ничего не нужно (для базового класса так)"""
	__new__ = tuple__new__
	
	
	def __getitem__(self, keys):
		'''('EN') Analog to similar method in humlist class'''
		keys = changeIndexes(keys)
		return tuple.__getitem__(self, keys)
	
	
	def __setitem__(self, keys, value):
		'''('EN') Analog to similar method in humlist class'''
		keys = changeIndexes(keys)
		return tuple.__setitem__(self, keys, value)#второй аргумент просит итерируемый объект вида: (slice(1,2,1), ) или (1, )
	
	
	def __delitem__(self, keys):
		'''('EN') Analog to similar method in humlist class'''
		keys = changeIndexes(keys)
		return tuple.__delitem__(self, keys)
		
	# Нетехнические методы:
		
	index = sequence_index
	get = sequence_get








class humstr(str):
	'''Class, that is the same to string type, but with normal indexes.
	version: 2
	'''
	
	# Технические методы:
	
	#def __init__(self, something):
		#У кортежей нет этого метода. Вместо него - __new__. Если добавить __init__ - будут работать оба.
	
	
	def __new__(self, *something): #только init не канает. Походу он вообще тут не работает.
		'''('EN') Analog to __init__ method in humlist class
		('RU') Но они не одинаковы - у каждого свои нюансы.'''
		try: something[1]; something[0] # если два и более аргумента - else:
		except IndexError: # если нет двух и более:
			try: something[0] # если только один аргумент - else:
			except IndexError: # если ни одного аргумента
				return str.__new__(self)
			else: # если только один аргумент
				something = something[0]
				return str.__new__(self, something)
		else: # если два и более аргумента
			return str.__new__(self, something) # возвращать ничего не нужно (для базового класса так)
	
	
	def __getitem__(self, keys):
		'''('EN') Analog to similar method in humlist class'''
		keys = changeIndexes(keys)
		return str.__getitem__(self, keys)
	
	
	def __setitem__(self, keys, value):
		'''('EN') Analog to similar method in humlist class'''
		keys = changeIndexes(keys)
		return str.__setitem__(self, keys, value)#второй аргумент просит итерируемый объект вида: (slice(1,2,1), ) или (1, )
	
	
	def __delitem__(self, keys):
		'''('EN') Analog to similar method in humlist class'''
		keys = changeIndexes(keys)
		return str.__delitem__(self, keys)
	
	
	# Нетехнические методы:
	
	def find(self, value):
		return str.find(self, value) + 1
	# rfind и так возвращает правильное значение
	
	
	def rindex(self, value, *positions):
		length = len(positions)
	
		if length >= 3:
			raise TypeError('index() takes at most 3 arguments ({0} given)'.format(length+1))
		elif length == 2:
			start = positions[0] - 1
			end = positions[1]
			return self.__class__.__base__.rindex(self, value, start, end) + 1
		elif length == 1:
			start = positions[0] - 1
			return self.__class__.__base__.index(self, value, start) + 1
		else:  # если нет вообще позиций
			return self.__class__.__base__.index(self, value) + 1
	
	
	def format(self, *args, **kwargs):
		if args:
			return str.format(self, '', *args, **kwargs)
		else:
			return str.format(self, **kwargs)
		
	index = sequence_index
	get = sequence_get








class humdict(dict):
	def get(self, key):
		'''Returns value of element on name (key). If such element is absent - returns None.
		Used in: dict. (variant for sequences is named sequence_get)
		'''
		try:
			value = self.__getitem__(key)
		except KeyError:
			value = None
		return value








def humrange(*n):
	'''Function, that is the same to range() function, but with normal indexes.
	list(humrange(3)) == [1,2,3]; list(humrange(2, 3)) == [2,3]; list(humrange(10, 8, -1)) == [10, 9, 8]
	revision: 2
	'''
	if len(n) >= 4:  # 4 and more arguments
		return range(*n)  # will raise error
		
	elif len(n) == 3:
	
		if n[0] < n[1]:  # straight order
			if n[2] <= 0:
				raise ValueError("Step can't be lesser or equal to zero while straight order.")
			return range(n[0], n[1] + 1, n[2])  # + и - дают включительность
			
		elif n[0] > n[1]:  # reverse order
			if n[2] >= 0:
				raise ValueError("Step can't be larger or equal to zero while reverse order.")
			return range(n[0], n[1] - 1, n[2])
			
		else:  # equal
			if n[2] <= 0:
				raise ValueError("Step can't be lesser or equal to zero while straight order.")
			return range(n[0], n[1] + 1, n[2])
		
	elif len(n) == 2:  # if [0] will be larger than [1] >> [], because range(4,4) and range(4,3) >> []
		if n[0] > n[1]:
			raise ValueError("Start value can't be larger than second while straight order (default step == 1).")
		return range(n[0], n[1] + 1)
		
	elif len(n) == 1:
		if n[0] <= 0:
			raise ValueError("Range from 1 to {0} with step == 1 doesn't exist (default step == 1).".format(n))
		return range(1, n[0] + 1)  # если один аргумент





def humfrange(a, b, step):
	'''Same as humrange, but including float numbers.
	'''
	if a < b:  # straight order
		if step <= 0:
			raise ValueError("Step can't be lesser or equal to zero while straight order.")
		while a <= b:
			yield a
			a += step
		return
	
	elif a > b:  # reverse order
		if step >= 0:  # can't be
			raise ValueError("Step can't be larger or equal to zero while reverse order.")
		while a >= b:
			yield a
			a += step
		return
	
	else:  # a == b
		if step <= 0:
			raise ValueError("Step can't be lesser or equal to zero while straight order.")
		while True:
			yield a
			break
		return
