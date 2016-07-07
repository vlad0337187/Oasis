'''Модуль гравитации. Для "гравитационной пушки".
Запускается выполнением функции gravity() при нажатии клавиш мыши
(колесико вверх, вниз; левая, правая средняя кнопки мыши).

В сцене должны присутствовать объекты:
    -crosshair_gravity (прицел грав. пушки) (плоскость посредине экрана);
    -родитель объекта прицела - камера;
    -point_for_transporting (указатель места перемещения предмета)(на скрытом слое);
    -transport_effect (на скрытом слое).
    
Объекты, с которыми должна работать гравитационная пушка, должны иметь свойство с именем "gravity".

Версия: 24
'''



#print('module runned')
import bge
from keys_reductions import *



scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()



target = None
pulled = False
globalDict = bge.logic.globalDict
globalDict['pulled'] = False # для модуля анимации (может и других)
globalDict['target'] = None  # для модуля анимации (может и других)
DEFAULT_DISTANCE_FOR_TRANSPORTING = 50  # для сброса. А то была ошибка в функц. gravity
distance_for_transporting = 50  # регулируется колесиком мыши. Потом станет текущим значением.
max_distance_for_transporting = 100
pulling_distance = 6
gun_power = 60  # равен силе броска; сила притягивания и толчка в 2 раза меньше.
throwing_power = gun_power
magneting_power = gun_power / 2
crosshair = scene.objects['crosshair_gravity']  # для более быстрого доступа
crosshairs_parent = crosshair.parent  # для разницы в координатах нужно




def gravity():
    '''Основная функция, вызывается при нажатии левой кнопки мыши.
    Остальные вызываются из нее.
    
    Вызывает действия при нажатии на заданные клавиши. (v2)
    '''
    global pulled, target, globalDict
    global distance_for_transporting  # меняем колесиком мыши
    
    # Нажата левая кнопка мыши:
    if mouse.events[LEFT_MOUSE] == activated:
        if pulled == False:
            find_target()
            if target != None:
                if crosshair.getDistanceTo(target) <= pulling_distance:  # расстояние, на котором можно "схватить" объект
                    pull()
        elif pulled == True:
            if not check_is_bareer_for_throwing_present():
                throw()
                delete_point_for_transporting()
            
    # Нажата правая кнопка мыши:
    elif mouse.events[RIGHT_MOUSE] == activated:
        if pulled == False:
            find_target()
            if target != None:
                if crosshair.getDistanceTo(target) <= pulling_distance:  # расстояние, на котором можно "схватить" объект
                    pull()
                    create_point_for_transporting()
        elif pulled == True:
            create_point_for_transporting()  # чтобы потом удалить если нет и не было ошибки
            if not check_is_bareer_for_transporting_present():
                transport()
                delete_point_for_transporting()
                transport_effect()
            
    # Колесико мыши вниз:
    elif mouse.events[WHEELDOWN_MOUSE] == activated:
        if pulled:
            distance_for_transporting -= 5
            if distance_for_transporting <= 0:
                distance_for_transporting += 5
            print('distance_for_transporting:', distance_for_transporting)
            create_point_for_transporting()
        else:
            find_target()
            if target != None:
              magnet()
        
    # Колесико мыши вверх:
    elif mouse.events[WHEELUP_MOUSE] == activated:
        if pulled:
            distance_for_transporting += 5
            if distance_for_transporting > max_distance_for_transporting:
                distance_for_transporting -= 5
            print('distance_for_transporting:', distance_for_transporting)
            create_point_for_transporting()
        else:
            find_target()
            if target != None:
              unmagnet()
            
    # Колесико мыши щелчок:
    elif mouse.events[MIDDLE_MOUSE] == activated:
        if pulled:
            if distance_for_transporting == DEFAULT_DISTANCE_FOR_TRANSPORTING:
                '''if state_of_point_for_transporting == True:
                    delete_point_for_transporting()'''
                if scene.objects.get('point_for_transporting'):
                    delete_point_for_transporting()
                else:
                    create_point_for_transporting()
            else:
                distance_for_transporting = DEFAULT_DISTANCE_FOR_TRANSPORTING
                create_point_for_transporting()  # для обновления
        else:
            find_target()
            if target != None:
              stop_object()


def find_target():
    '''Пишет в глобальную переменную target имя объекта, на который направлена пушка. (v2)
    '''
    global target, globalDict
    
    crosshair_world_position = crosshair.worldPosition.copy()
    crosshair.localPosition[0] += 100
    crosshair_world_posion_changed = crosshair.worldPosition.copy()  # получили коорд. смещения в лок. области объекта
    crosshair.worldPosition = crosshair_world_position  
    
    target = crosshair.rayCastTo(crosshair_world_posion_changed, 100, 'gravity')
    globalDict['target'] = target  # для модуля анимации (может и других)


def pull():
    '''"Притягивает" объект к прицелу пушки. (v2)
    '''
    global target, pulled, globalDict
    
    if target == None:
        return
    
    target.setParent(crosshair, False, True)
    target.worldPosition = crosshair.worldPosition
    local_position = target.localPosition.copy()
    local_position[0] += 2; local_position[1] -= 1; local_position[2] -= 0
    target.localPosition = local_position
    
    #target.collisionMask = 65533  # чтобы отражать можно было удары
    #target.collisionGroup = 2
    #print('collision group:', target.collisionGroup)
    #print('collision mask:', target.collisionMask)
        
    pulled = True
    globalDict['pulled'] = True  # для модуля анимации (может и других)
        
    
def throw():
    '''Отбрасывает притянутый объект от пушки. (v1)
    '''
    global target, pulled, globalDict
    
    dx, dy, dz = difference_in_coordinates(crosshair, crosshairs_parent)
    
    target.removeParent()
    direction = [dx * gun_power, dy * gun_power, dz * gun_power]  # сила броска
    target.setLinearVelocity(direction, False)
    
    pulled = False
    target = None
    globalDict['pulled'] = False  # для модуля анимации (может и других)
    globalDict['target'] = False  # для модуля анимации (может и других)


def transport():
    '''Тоже самое, что и бросок, только перемещение на заданное расстояние.
    (v3)
    '''
    global target, pulled, globalDict
    
    target.removeParent()
    target.worldPosition = scene.objects['point_for_transporting'].worldPosition  #раньше просто предмет перемещали, сейчас будем прямо на место указателя
    
    pulled = False
    target = None
    globalDict['pulled'] = False  # для модуля анимации (может и других)
    globalDict['target'] = False  # для модуля анимации (может и других)
    
    
def transport_effect():
    '''Отображает на время эффект перемещения (объект с названием "teleport").
    Вызывается из transport(). (v1)
    '''
    scene.addObject('transport_effect', crosshair, 15)
    
    transport_effect_obj = scene.objects['transport_effect']
    transport_effect_obj.setParent(crosshair, False, True)
    #print('transport effect world position: ', transport_effect_obj.worldPosition)
    #print('transport effect local position: ', transport_effect_obj.localPosition)
    
    transport_effect_obj.worldPosition = crosshair.worldPosition.copy()
    transport_effect_obj.localPosition.y -= 0.75
    transport_effect_obj.localPosition.x += 2
    transport_effect_obj.localPosition.z -= 0.1
    
    transport_effect_obj.localOrientation = crosshair.localOrientation.copy()
    #transport_effect_obj.removeParent()
    
    
def create_point_for_transporting():
    '''Создает\обновляет (перемещает) указатель места телепортации объекта. (v2)
    '''
    #global state_of_point_for_transporting  # отображает состояние вкл\выкл
    
    if scene.objects.get('point_for_transporting', None) == None:  # вдруг уже есть
        scene.addObject('point_for_transporting')
    point_for_transporting = scene.objects['point_for_transporting']
    
    point_for_transporting.worldPosition = crosshair.worldPosition.copy()
    point_for_transporting.setParent(crosshair, False, False)
    
    dx, dy, dz = difference_in_coordinates(crosshair, crosshairs_parent)
    direction = [dx * distance_for_transporting, dy * distance_for_transporting, dz * distance_for_transporting] # для перемещения, чем меньше dx, т.д. - тем точнее
    point_for_transporting.worldPosition.x += direction[0]
    point_for_transporting.worldPosition.y += direction[1]
    point_for_transporting.worldPosition.z += direction[2]


def check_is_bareer_for_transporting_present():
    '''Проверяет наличие барьера между прицелом и местом (указателем) куда перемещать предмет.
    Возвращает None или имя объекта барьера.
    Вызывается из gravity().
    Барьер - предмет со свойством "terrain". (v4)
    '''

    point_for_transporting = scene.objects['point_for_transporting']  # должна присутствовать
    barrier = crosshair.rayCast(point_for_transporting, crosshair, 0, 'terrain', 0, 1, 0, 65535)  # 65535 - числ. предст. групп - см. краткий конспект Blender
    #print(barrier)
    return barrier[0]


def check_is_bareer_for_throwing_present():
    '''Проверяет наличие барьера для перемещения (луч от прицела прямо по оси).
    Возвращает None или имя объекта барьера.
    Барьер - предмет со свойством "terrain". (v4)
    '''
    global target
    
    crosshairs_world_position = crosshair.worldPosition.copy()  # бэкап
    crosshair.localPosition[0] += 2
    crosshairs_world_position_changed = crosshair.worldPosition.copy()
    crosshair.worldPosition = crosshairs_world_position  # вернули на место
    
    barrier = crosshair.rayCastTo((crosshairs_world_position_changed), 0.0, 'terrain')
    #print(barrier)
    return barrier


def difference_in_coordinates(object1, object2):
    '''Отнимает от мировых координат объекта 1 мировые координаты объекта 2.
    Пример: координаты камеры в сравнии с координатами прицела = направление взгляда. (v1)
    '''
    object1_position = object1.worldPosition.copy()
    object2_position = object2.worldPosition.copy()
    delta_x = object1_position[0] - object2_position[0]
    delta_y = object1_position[1] - object2_position[1]
    delta_z = object1_position[2] - object2_position[2]
    return [delta_x, delta_y, delta_z]


def delete_point_for_transporting():
    '''Убирает с экрана указатель для перемещения объектов. (v1)
    '''
    #global state_of_point_for_transporting
    
    if scene.objects.get('point_for_transporting'):
        scene.objects['point_for_transporting'].endObject()
        #state_of_point_for_transporting = False
    

def magnet():
    '''Примагничивает объект.
    Т.е. применяет к объекту скорость в направлении прицела. (v2)
    '''
    global target
    
    dx, dy, dz = difference_in_coordinates(crosshairs_parent, crosshair)
    
    direction = [dx * magneting_power, dy * magneting_power, dz * magneting_power]  # сила притягивания
    target.setLinearVelocity(direction, False)


def unmagnet():
    '''Отмагничивает объект.
    Т.е. применяет к объекту скорость в противоположном от прицела направлении.
    
    То же, что и в magnet(), только направление противоположное задается. (v2)
    '''
    global target
    
    dx, dy, dz = difference_in_coordinates(crosshair, crosshairs_parent)
    
    direction = [dx * magneting_power, dy * magneting_power, dz * magneting_power]  # сила отталкивания
    target.setLinearVelocity(direction, False)
    
    
def stop_object():
    '''Останавливает любое движение объекта. (v2)
    '''
    global target
    
    target.setLinearVelocity([0, 0, 0], False)

