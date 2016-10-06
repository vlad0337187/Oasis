import bge
import bpy


scene = bge.logic.getCurrentScene()
cube_test = scene.objects['Cube_test']
cube_test_position = cube_test.worldPosition


# we get the image
grass_mask = bpy.data.images.get('ground_baked_v2.png')  # 'ground_grass_mask_inverse.png'
mask_width = grass_mask.size[0]
mask_height = grass_mask.size[1]




answer = cube_test.rayCast(cube_test_position, (cube_test_position.x, cube_test_position.y, 0), 0, 'ground', 0, 1, 2, 0b1111111111111111)
U_coord = answer[4][0]
V_coord = answer[4][1]
print('UV:', U_coord, 'x', V_coord)



# Высчитаем соответствующие координаты по пропорции:
# U (ширина):
px_horizontal = int(U_coord * mask_width)
px_vertical = int(V_coord * mask_height)

px_ordinal_number = (mask_width * (px_vertical - 1)) + px_horizontal  # from 512x512 image
px_number_in_pixels = (px_ordinal_number * 4)  # *4 - RGBA (x4 of each color);
# we don't make -1 because in 0 there is alpha value.


print('Is in that pixel data?', grass_mask.pixels[px_number_in_pixels])