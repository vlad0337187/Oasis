'''This script copies all text files into specified folder.
Revision: 1
'''
folder_to_copy = '../../../code-upbge'


import bpy
import os  # to get abs. path




filepath = bpy.data.filepath
filepath = filepath[:filepath.rfind('/') + 1]

path_to_text = os.path.abspath(filepath + folder_to_copy)

print('Starting writting files to {0}'.format(path_to_text))
for key in bpy.data.texts.keys():
	obj = bpy.data.texts[key]
	with open( path_to_text + '/{name}'.format(name=key), 'tw' ) as file_to_write:
		file_to_write.write( obj.as_string() )
	print('File {name} was successfully written.'.format(name=key))

print('All files were successfully written.')