'''
This module imports code of all other modules (text files), specified in dictionary "what_to_import"
and places it into appropriate text files inside of .blend file.

Needed when code of similar modules was updated on hard disk.
Revision: 1.1
'''



what_to_import = {'humanity.py':'/home/vlad/Programs/My_projects/humanity/'}  # key - name of module, value - it's path on hard disk


import bpy  # to get text blocks inside of .blend file


print('\nStarting importing code.')

for key, value in what_to_import.items():
	with open(value + key, 'tr') as text_file:
		bpy.data.texts[key].from_string(text_file.read())
	print(key, 'imported.')


print('Finished importing code.')