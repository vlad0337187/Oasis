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

Revision: 8
'''


from decimal import Decimal  # for humdrange








def change_indexes_0_to_1(key):
	'''('RU') Функция используется в drange в __getitem__().
	a[1] > a[0]
	Она смещает в последовательностях номер первого элемента с [0] на [1].
	если при a[arg] передается один аргумент, он int и пишется в keys
	если пытаешься брать срез, keys присваивается объект среза вида: slice(1, None, None)
	rev. 5
	'''
	if type(key) == int:	
		
		if key >= 0:
			key += 1
	
	elif type(key) == slice:
	
		if key.step and (key.step < 0): # reverse order  
			if key.start and (key.start >= 0):
				start = key.start + 1
			else:
				start = key.start
			
			if key.stop != None:
			
				if key.stop >= 0:
					stop = key.stop + 2
				else:
					stop = key.stop
			else:
				stop = None
			
			key = slice(start, stop, key.step)
	
		else:  # straight order, key.step > 0 and None
			if key.start >= 0:
				start = key.start + 1
			
			key = slice(start, key.stop, key.step)		
	
	return key




def change_indexes_1_to_0(key):
	'''('RU') Функция используется в: __getitem__, __setitem__, __delitem__.
	a[1] > a[0]
	Она смещает в последовательностях номер первого элемента с [1] на [0].
	если в функц. передается один аргумент, он int и пишется в keys
	если пытаешься брать срез, keys присваивается объект среза вида: slice(1, None, None)	
	rev. 6
	'''
	if type(key) == int:
		
		if key > 0:
			key -= 1
	
	elif type(key) == slice:
		
		if key.step and (key.step < 0):  # reverse order
			if key.start and (key.start > 0):
				start = key.start - 1
			else:  # key.start == None, or == 0, or < 0.
				start = key.start
			
			if key.stop != None:
				if key.stop >= 2:
					stop = key.stop - 2
				elif 0 <= key.stop  <= 1:
					stop = None
			else:
				stop = key.stop
			
			key = slice(start, stop, key.step)
		
		else:  #  straight order  # key.step > 0 and None
			if key.start and (key.start > 0):
				start = key.start - 1			
				key = slice(key.start - 1, key.stop, key.step)
	
	return key




"""def check_indexes_0_to_1():  # 
	'''Check indexes for logic and type errors.
	hack for drange because if reverse order and a is lesser than b - 
	it gives another error -  Stop key index (9) out of range - 
	it needs check for this earlier than for
	
	rev. 1
	'''
	if index_type == int:
		pass
	
	elif index_type == slice:
		if key.step and (key.step < 0):  # reverse order
			if key.start < key.
		
		else: # straight order (step > 0 or None)
	
	else:
		raise TypeError('Indexes must be int or slice type, now it is {0}'.format(type(index_type)))"""








# __init__ and __new__ methods
for name in ('list', 'tuple', 'str'):
	if name == 'list':
		method = '__init__'
		retn = ''
	else:  # tuple, str
		method = '__new__'
		retn = 'return '
	exec(
	"""def hum{name}{method}(self, *something):
		'''('EN') humlist(1,2) > [1, 2]; humlist([1,2]) > [1, 2]; humlist((1,2), (2,3)) > [(1, 2), (2, 3)] 
		('RU') Подобные есть и в humtuple и в humstr, только называется __new__.
		'''	
		
		classname = 'hum{name}'  # потому что у неизменяемых объектов до создания экземпляра еще нету self.__class__
		length = len(something)
		
		if length > 1:
			if classname == 'humstr':
				result = ''
				for some in something:
					result += str(some)
				{retn}{name}.{method}(self, result)  # retn иногда возвращает, иногда - нет
			else:
				{retn}{name}.{method}(self, something)
		
		elif length == 1:
			if something[0].__class__ == tuple:
				{retn}{name}.{method}(self, something[0])  # tuple
			else:
				if classname == 'humstr':
					{retn}{name}.{method}(self, something[0])  # one element
				else:
					{retn}{name}.{method}(self, something)  # tuple with one element
		
		else:  # length == 0
			{retn}{name}.{method}(self, something)""".format(name=name, method=method, retn=retn))
else:
	del method, retn, name




def sequence__getitem__(self, keys):
	keys = change_indexes_1_to_0(keys)
	return self.__class__.__base__.__getitem__(self, keys)

def sequence__setitem__(self, keys, value):
	'''('EN') Set self[key] to value. If A = [1,2,3], than A[1] = 5 will change A to: [5,2,3]
	'''
	keys = change_indexes_1_to_0(keys)
	self.__class__.__base__.__setitem__(self, keys, value) # keys - итерируемый объект: (slice(1,2,1), ) или (1, )

def sequence__delitem__(self, keys):
	'''('EN') Delete self[key]. If A = [1,2,3], than A[1] = 5 will change A so: [5,2,3]''' 
	keys = change_indexes_1_to_0(keys)
	self.__class__.__base__.__delitem__(self, keys)




def sequence_get(self, keys):
	'''Get method for sequences.
	Returns value of element on position (keys). If such element is absent - returns None.
	Used in: humlist, humtuple, humstr.
	rev. 1
	'''
	try:
		value = self.__getitem__(keys)
	except (IndexError, KeyError):
		value = None
	return value


def sequence_index(self, value, *positions):
	'''Index method for sequences.
	Returns index of element with specified value (optional in positions).
	rev. 1
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
	rev. 2
	'''

	# Технические методы:
	
	__init__ = humlist__init__
	
	__getitem__ = sequence__getitem__
	__setitem__ = sequence__setitem__
	__delitem__ = sequence__delitem__
	
	
	# Нетехнические методы:
	
	index = sequence_index
	get = sequence_get
	
	def insert(self, position, value):
		position = changeIndexes(position)
		list.insert(self, position, value)








class humtuple(tuple):
	'''Class, that is the same to tuple type, but with normal indexes.
	rev. 2
	'''
	
	# Технические методы:
	
	__new__ = humtuple__new__  # у неизменяемых типов только __new__() метод
	
	
	__getitem__ = sequence__getitem__
	__setitem__ = sequence__setitem__
	__delitem__ = sequence__delitem__
	
	
	# Нетехнические методы:
		
	index = sequence_index
	get = sequence_get








class humstr(str):
	'''Class, that is the same to string type, but with normal indexes.
	rev. 2
	'''
	
	# Технические методы:	
	
	__new__ = humstr__new__
	
	__getitem__ = sequence__getitem__
	__setitem__ = sequence__setitem__
	__delitem__ = sequence__delitem__
	
	
	# Нетехнические методы:
	
	index = sequence_index
	get = sequence_get
	
	def find(self, value):
		return str.find(self, value) + 1
	# (rfind и так возвращает правильное значение)
	
	
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








class humdict(dict):
	'''Same as dict, but with .get() method.
	'''
	
	get = sequence_get  # it's appropriate








def humrange(*n):
	'''Function, that is the same to range() function, but with normal indexes.
	list(humrange(3)) == [1,2,3]; list(humrange(2, 3)) == [2,3]; list(humrange(10, 8, -1)) == [10, 9, 8]
	rev. 2
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








class humdrange():  # not a function because of need .__len__() method
	'''Same as humrange, but including decimal (analog to float) numbers.
	Returns Decimal() numbers.
	rev. 5
	'''
	
	
	def __init__(self, a, b, step, return_type='dec'):
		'''Return type: 'dec' - decimal, 'float' - float, 'str' - string (float, written as string),
		'int' - int.
		rev. 3
		'''
		self.check_type_errors(a, b, step, return_type)
		
		a, b, step = Decimal(a), Decimal(b), Decimal(step)
		
		self.a, self.b, self.step = a, b, step
		self.return_type = return_type
		
		self.check_logic_errors()
		
		self.length = self.__len__()
	
	
	
	
	def check_type_errors(self, a, b, step, return_type):
		'''Is launched from .__init__().
		rev.2
		'''
		# check for float:
		if (a.__class__ == float) or (b.__class__ == float) or (step.__class__ == float):
			raise TypeError('You cannot pass float to humdrange because general float type cannot reproduce all numbers - some of them are changed to other, what causes errors.\nPlease, use Decimal(), int, or float, which is written as string (in quotes).')
		
		# we check a:
		if not ((a.__class__ == int) or (a.__class__ == str) or (a.__class__ == Decimal)):
			raise TypeError('Start value must be int or decimal, written as string, or Decimal.')
		# we check b:
		if not ((b.__class__ == int) or (b.__class__ == str) or (b.__class__ == Decimal)):
			raise TypeError('Start value must be int or float, written as string, or Decimal.')
		# we check step:
		if not ((step.__class__ == int) or (step.__class__ == str) or (step.__class__ == Decimal)):
			raise TypeError('Start value must be int or float, written as string, or Decimal.')
		
		# we check return_type:
		if not (type(return_type) == str):
			raise TypeError('Return type must be specified with appropriate string.')
	
	
	
	
	def check_logic_errors(self):
		'''Checks current instance of humdrange for errors.
		Is launched from .__init__().
		rev. 1
		'''
		# we check step
		if self.step == 0:
			raise ValueError("Step can't be equal to zero.")
		
		# we check a and b depening order
		if self.step < 0:  # reverse order
			if self.a < self.b:
				raise ValueError("Start value ({0}) can't be lesser stop ({1}) while reverse order."\
				.format(self.a, self.b))
		
		else:  # straight order or a == b
			if self.a > self.b:
				raise ValueError("Start value ({0}) can't be larger stop ({1}) while straight order."\
				.format(self.a, self.b))
		
		# we check return type
		if not ((self.return_type == 'dec') or (self.return_type == 'float') or 
				(self.return_type == 'str') or (self.return_type == 'int')):
					raise ValueError("Return type must be one of: 'dec', 'float', 'str', 'int', it was {0}.".format(type(self.return_type)))
	
	
	
	
	def __iter__(self):
		self.first_time = True  # to return a first
		self.current = self.a
		return self
	
	
	def __next__(self):
	
		if self.first_time:  # first value == self.a
			self.first_time = False
			return self.return_depending_type(self.a)
		
		self.current += self.step
		
		if self.a < self.b:  # straight order
			if self.current <= self.b:
				return self.return_depending_type(self.current)
			else:
				raise StopIteration()
		
		elif self.a > self.b:  # reverse order
			if self.current >= self.b:
				return self.return_depending_type(self.current)
			else:
				raise StopIteration()
		
		else:  # a == b
			if self.current == self.a:
				return self.return_depending_type(self.a)
			else:
				raise StopIteration()
	
	
	
	
	def __len__(self):
		try:
			self.length
		except AttributeError:  # if no such attribute
			return int((self.b - self.a) / self.step + 1)
		else:
			return self.length
	
	
	
	
	get = sequence_get
	
		
	def __getitem__(self, key):
		'''Returns one value if there's one key (it's int),
		or new appropriate humdrange instance, if key is slice.
		rev. 3
		'''
		if type(key) == int:
		
			self.check_key_for_errors(key)
			key = self.replace_negative_keys(key)
			
			if self.a == self.b:
				return self.return_depending_type(self.a)
			
			else:  # straight or reverse order resolved mathematically
				return self.return_depending_type(self.a + (self.step * (key - 1)))
		
		elif type(key) == slice:
		
			self.check_slice_for_errors(key)
			key = self.replace_negative_keys(key)
			
			backup = self.return_type  # hack. if it'll be float - it'll pass it (float) to new
			self.return_type = 'dec'  # humdrange's .__init__() method - it'll give errors.
			
			if key.step:
				step = key.step * self.step
			else:
				step = self.step
			
			if step > 0:  # straight order
				if self.step > 0:
					if key.start:
						start = humdrange.__getitem__(self, key.start)  # not self[key] because of error with subclasses
					else:
						start = self.a
			
					if key.stop:
						stop = humdrange.__getitem__(self, key.stop)  # not self[key] because of error with subclasses
					else:
						stop = self.b
				else: # self.step < 0
					if key.start:
						start = humdrange.__getitem__(self, key.start)  # not self[key] because of error with subclasses
					else:
						start = self.b
			
					if key.stop:
						stop = humdrange.__getitem__(self, key.stop)  # not self[key] because of error with subclasses
					else:
						stop = self.a
			
			else:  # step < 0, reverse order
				if self.step > 0: 
					if key.start:
						start = humdrange.__getitem__(self, key.start)  # not self[key] because of error with subclasses
					else:
						start = self.b
			
					if key.stop:
						stop = humdrange.__getitem__(self, key.stop)  # not self[key] because of error with subclasses
					else:
						stop = self.a
				else: # self.step < 0
					if key.start:
						start = humdrange.__getitem__(self, key.start)  # not self[key] because of error with subclasses
					else:
						start = self.a
			
					if key.stop:
						stop = humdrange.__getitem__(self, key.stop)  # not self[key] because of error with subclasses
					else:
						stop = self.b				
			
			self.return_type = backup  # return back from hack
			
			return humdrange(start, stop, step, self.return_type)
		
		else:
			raise TypeError('Key is not of an appropriate type. It must be int or slice.')
	
	
	
	
	def check_key_for_errors(self, key):
		'''Is used in .__getitem__().
		'''		
		# check in diapason
		if not ((1 <= key <= self.__len__()) or (-1 >= key >= -self.__len__()) ):
			raise IndexError("Key index ({now}) out of range (from 1 to {len} or -1 to -{len}).".format(len=self.__len__(), now=key))
	
	
	
	
	def check_slice_for_errors(self, key):
		'''Is used in .__getitem__().
		'''
		# check types of elements (to be int or None)
		if not ( (type(key.start) == int) or (key.start == None) ):
			raise TypeError("Start value must be int or omitted (now it is {0}).".format(key.start))
		if not ( (type(key.stop) == int) or (key.stop == None) ):
			raise TypeError('Stop value must be int or omitted (now it is {0}).'.format(key.start))
		if not ( (type(key.step) == int) or (key.step == None) ):
			raise TypeError('Step value must be int or omitted (now it is {0}).'.format(key.start))	
		
		
		# check start and stop indexes to be in diapason or None	
		if key.start != 0:
			if key.start:  # None cannot be compared to int
				if not ((1 <= key.start <= self.__len__()) or (-1 >= key.start >= -self.__len__())):
					raise IndexError('Start key index ({ind}) out of range (from 1 to {rng} or -1 to -{rng}).'\
					.format(ind=key.start, rng=self.__len__()))
		else:
			raise IndexError('Slice start value cannot be equal zero.')
		if key.stop != 0:
			if key.stop:  # None cannot be compared to int
				if not ((1 <= key.stop <= self.__len__()) or (-1 >= key.stop >= -self.__len__())):
					raise IndexError('Stop key index ({ind}) out of range (from 1 to {rng} or -1 to -{rng}).'\
					.format(ind=key.stop, rng=self.__len__()))
		else:
			raise IndexError('Slice stop value cannot be equal zero.')
		
		
		# check key.step, check start and stop depending on order (step sets order)
		if key.step != 0:  # because if it's None, than will be error while "key.step > 0"
						
			if (key.step == None) or (key.step > 0):  # straight order
				if key.start:
					start = self.replace_negative_keys(key.start)
				else:
					start = 1
				if key.stop:
					stop = self.replace_negative_keys(key.stop)
				else:
					stop = self.__len__()
					
				if start > stop:
					raise ValueError('Slice start value ({start}) cannot be larger stop ({stop}) while straight order.'\
					.format(start=key.start, stop=key.stop))
			
			else:  # key.step < 0, reverse order
				if key.start:
					start = self.replace_negative_keys(key.start)
				else:
					start = self.__len__()
				if key.stop:
					stop = self.replace_negative_keys(key.stop)
				else:
					stop = 1
				
				if start < stop:
					raise ValueError('Slice start value ({start}) cannot be lesser stop ({stop}) while reverse order.'\
					.format(start=key.start, stop=key.stop))
			
		else:  # key.step == 0
			raise ValueError('Slice step cannot be zero.')	
	
	
	
	
	def replace_negative_keys(self, key):
		'''Replaces negative key's values (which mean counting from the end of range)
		with positive ones (which mean counting from start of range).
		It doesn't return anything - it replaces so it is.
		rev. 2
		'''
		if type(key) == int:
			if key < 0:
				key = (self.__len__() + 1) + key  # "-" on "-" gives "+"
			return key
			
		elif type(key) == slice:
			if key.start and (key.start < 0):
				start = (self.__len__() + 1) + key.start  # + -key will give - key
			else:
				start = key.start
			
			if key.stop and (key.stop < 0):
				stop = (self.__len__() + 1) + key.stop
			else:
				stop = key.stop
		
			return slice(start, stop, key.step)
	
	
	
	
	def return_depending_type(self, value):
		'''Returns value, depending on return type, specified in __init__().
		rev. 1
		'''
		if self.return_type == 'dec':
			return value
		elif self.return_type == 'float':
			return float(value)
		elif self.return_type == 'str':
			return str(value)
		else:  # == 'int'
			return int(value)




class drange(humdrange):
	def __getitem__(self, key):
		key = change_indexes_0_to_1(key)
		#сheck_indexes_0_to_1(key)
		return self.__class__.__base__.__getitem__(self, key)








if __name__ == '__main__':  # temporary checks
	pass
