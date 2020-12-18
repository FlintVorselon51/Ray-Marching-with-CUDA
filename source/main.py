# Импортируем модули
# Pycuda
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import pygame
import numpy as np
from kernel import kernel
from Camera import Camera
from time import time
from math import ceil, sqrt, sin, cos, pi
from config import *

import os


def get_distance(objs, point):
    idx = 0
    min_dist = 0
    for i in range(len(objs)):
        now = get_module_of_vector(point, objs[i][0:3]) - objs[i][3]
        if now < min_dist or min_dist == 0:
            min_dist = now
            idx = i
    return idx, min_dist


def get_module_of_vector(point_1, point_2):
    return pow((point_1[0] - point_2[0]) ** 2 +
               (point_1[1] - point_2[1]) ** 2 +
               (point_1[2] - point_2[2]) ** 2, 0.5)


os.environ['PATH'] += ';' + r"C:\Program Files" \
                            r" (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29333\bin\Hostx64\x64"

if __name__ == '__main__':

    # Рассчитываем количество блоков
    block_x = block_y = ceil(sqrt(SCREEN_HEIGHT))
    block_z = 1

    # Рассчитываем количество гридов
    grid_x = grid_y = ceil(sqrt(SCREEN_WIDTH))

    camera = Camera(CAMERA_COORDINATES, HORIZONTAL_VIEWING_ANGLE, VERTICAL_VIEWING_ANGLE, HORIZONTAL_ROTATION)

    # Рассчитываем разницу между краями камеры на каждый пиксель
    camera_delta = camera.get_delta()
    camera_delta = [camera_delta[0] / SCREEN_WIDTH, camera_delta[1] / SCREEN_HEIGHT, camera_delta[2] / SCREEN_WIDTH]

    # Объекты
    # 1 - Шары (x, y, z, радиус, R, G, B)
    objects = np.array(
        [
            [5, 0, 2, 2.4, 0, 0, 255],
            [3, 0, 0, 1.2, 0, 255, 0]
        ], dtype=np.float32)
    len_obj = len(objects)
    # Данные конфигурации и камеры
    index, min_distance = get_distance(objects, camera.get_coordinates())
    int_data = np.array([SCREEN_WIDTH, SCREEN_HEIGHT, grid_x, block_x, index, len_obj], dtype=np.int)
    # data = np.array([*camera.get_start_coordinates(), *camera_delta], dtype=np.float32)
    # Данные
    data = np.array([*camera.get_start_coordinates(), *camera_delta, *camera.get_coordinates(), min_distance],
                    dtype=np.float32)

    result = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT, 3), dtype=np.int)

    # Инициализируем CUDA
    cuda.init()
    dev = cuda.Device(0)
    ctx = dev.make_context()

    kernel = SourceModule(kernel)

    f = kernel.get_function("f")

    f(cuda.Out(result), cuda.In(int_data), cuda.In(data), cuda.In(objects), block=(block_x, block_y, block_z),
      grid=(grid_x, grid_y))

    # pygame
    main_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface = pygame.surfarray.make_surface(result)

    # Timing
    cnt = 0
    unlimited_cnt = 350
    start_frame = time()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ctx.pop()
                exit()

        # result[0:100] = 255

        pygame.surfarray.blit_array(surface, result)
        # pygame.pixelcopy.array_to_surface(surface, result)  Делает тоже самое
        main_surface.blit(surface, (0, 0))

        f(cuda.Out(result), cuda.In(int_data), cuda.In(data), cuda.In(objects), block=(block_x, block_y, block_z),
          grid=(grid_x, grid_y))

        pygame.display.flip()

        # Timing
        cnt += 1
        unlimited_cnt += 1
        if time() - start_frame > 1:
            start_frame = time()
            print(cnt)
            cnt = 0
