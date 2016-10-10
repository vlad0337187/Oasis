'''Предоставляет сокращения для нажатых клавиш.

Может использоваться всеми модулями, которые обрабатывают нажатия клавиш.

Author: Vladislav Naumov. naumovvladislav@list.ru; github.com/vlad1777d; vk.com/naumovvladislav
License: CC-BY. To use this under other license contact author.

Revision: 3
'''

import bge


keyb = bge.logic.keyboard  # если сюда добавить events - не будет работать
mouse = bge.logic.mouse

activated = bge.logic.KX_INPUT_JUST_ACTIVATED
deactivated =  bge.logic.KX_INPUT_JUST_RELEASED
active = bge.logic.KX_INPUT_ACTIVE
absent = bge.logic.KX_INPUT_NONE

W = bge.events.WKEY
A = bge.events.AKEY
D = bge.events.DKEY
S = bge.events.SKEY
SPACE = bge.events.SPACEKEY
LSHIFT = bge.events.LEFTSHIFTKEY

LEFT_MOUSE = bge.events.LEFTMOUSE
RIGHT_MOUSE = bge.events.RIGHTMOUSE
MIDDLE_MOUSE = bge.events.MIDDLEMOUSE
WHEELUP_MOUSE = bge.events.WHEELUPMOUSE
WHEELDOWN_MOUSE = bge.events.WHEELDOWNMOUSE