# Импортируем модули.
from math import sin, cos, radians


class Camera:
    """
    Класс виртуальной камеры в трехмерном пространстве.
    Поддерживается только горизонтальное вращение камеры!

    Камера имеет четрыре опорные точки, которые вместе с точкой координат камеры описывают пирамиду,
    основание которой является поверхностью экрана камеры.

    Так как камера имеет только горизонтальное вращение, то для того, чтобы задать координаты этих четырех точек,
    будет достаточно рассчитать по два значения на каждую ось (x, y, z). После чего, для построения изображения,
    нам будет достаточно знать положение левой верхней точки, а также на сколько меняются координаты точки, при
    прохождении по основанию пирамиды, на каждой из осей.

    Атрибуты
    --------
    coordinates : iterable
        Координаты камеры в трехмерном пространстве.
    horizontal_viewing_angle : float
        Угол обзора камеры по горизонтали. Указывается в градусах.
    vertical_viewing_angle : float
        Угол обзора камеры по вертикали. Указывается в градусах.
    horizontal_rotation : float
        Угол, на который повернута камера по горизонтали. Указывается в градусах.
    left_x : float
        Значение координаты левых точек по оси X.
    right_x : float
        Значение координаты правых точек по оси X.
    upper_y : float
        Значение координаты верхних точек по оси Y.
    lower_y : float
        Значение координаты нижних точек по оси Y.
    left_z : float
        Значение координаты левых точек по оси Z.
    right_z : float
        Значение координаты правых точек по оси Z.

    Методы
    ------
    __calculate_edge_points
        pass
    """

    def __init__(self, coordinates, horizontal_viewing_angle, vertical_viewing_angle, horizontal_rotation):
        self.__coordinates = coordinates
        self.__horizontal_viewing_angle = horizontal_viewing_angle
        self.__vertical_viewing_angle = vertical_viewing_angle
        self.__horizontal_rotation = horizontal_rotation
        self.__calculate_edge_points()

    def __calculate_edge_points(self):
        """
        Рассчитывает значения координат на каждой из осей.
        """
        horizontal_angle_1 = radians(90 - self.__horizontal_rotation + self.__horizontal_viewing_angle / 2)
        horizontal_angle_2 = radians(90 - self.__horizontal_rotation - self.__horizontal_viewing_angle / 2)

        self.__left_x = sin(horizontal_angle_1)
        self.__right_x = sin(horizontal_angle_2)

        self.__upper_y = sin(radians(self.__vertical_viewing_angle / 2))
        self.__lower_y = sin(radians(-self.__vertical_viewing_angle / 2))

        self.__left_z = cos(horizontal_angle_1)
        self.__right_z = cos(horizontal_angle_2)

    def get_delta(self):
        """
        Рассчитывает и возвращает разницу между крайними точками основания пирамиды.
        """
        return self.__right_x - self.__left_x, self.__lower_y - self.__upper_y, self.__right_z - self.__left_z

    def get_start_coordinates(self):
        """
        Возвращает координаты левый верхней точки основания пирамиды.
        """
        return self.__left_x, self.__upper_y, self.__left_z

    def get_coordinates(self):
        return self.__coordinates

    def set_horizontal_rotation(self, horizontal_rotation):
        """
        Позволяет вращать камеру.
        """
        self.__horizontal_rotation = horizontal_rotation
        self.__calculate_edge_points()
