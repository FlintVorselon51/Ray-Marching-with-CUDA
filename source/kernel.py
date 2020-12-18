kernel = """
    __global__ void f(int *result,  int *int_data, float *data, float *objects)
    {
        int blockId = blockIdx.x + blockIdx.y * gridDim.x;
        int threadId = blockId * (blockDim.x * blockDim.y) + (threadIdx.y * blockDim.x) + threadIdx.x;
        
        int screen_width = int_data[0];
        int screen_height = int_data[1];
        int max_grid = int_data[2];
        int max_block = int_data[3];
        int number_of_objects = int_data[5];
        
        int x = max_grid * blockIdx.y + blockIdx.x;
        int y = max_block * threadIdx.y + threadIdx.x; 
        
        float end_point_x = data[0] + data[3] * x;
        float end_point_y = data[1] + data[4] * y;
        float end_point_z = data[2] + data[5] * x;
        
        float to_camera_x = end_point_x;
        float to_camera_y = end_point_y;
        float to_camera_z = end_point_z;
        
        float camera_x = data[6];
        float camera_y = data[7];
        float camera_z = data[8];
        
        float min_distance = data[9];
        
        for (int i = 0; i < 50; i++) {
            float length = sqrtf(
                powf(end_point_x - camera_x, 2) +
                powf(end_point_y - camera_y, 2) +
                powf(end_point_z - camera_z, 2)); 
            float coff = min_distance / length; // Коэфицент удлиннения

            camera_x = camera_x + (end_point_x - camera_x) * coff;  
            camera_y = camera_y + (end_point_y - camera_y) * coff;
            camera_z = camera_z + (end_point_z - camera_z) * coff;
            //if (x == 237 && y == 0) { 
            //   printf("ATTENTION! %d (%f, %f, %f) min_distance %f ATTENTION!", i, camera_x, camera_y, camera_z, min_distance);
            //}
            // Находим минимальное расстояние до объекта
            
            min_distance = 0.0; // Минимальное расстояние до объекта
            int idx = 0;  // Индекс объекта с минимальным расстоянием
            for (int j = 0; j < number_of_objects; j++) {    
                float distance = sqrtf(
                    powf(objects[j*7] - camera_x, 2) +
                    powf(objects[j*7+1] - camera_y, 2) +
                    powf(objects[j*7+2] - camera_z, 2)); // - радиус круга
                distance -= objects[j*7+3];
                
                if (distance < min_distance || j == 0) {
                    min_distance = distance;
                    idx = j;
                }
                if (min_distance < 0.001) {
                    if (x < screen_width && y < screen_height) {
                        result[(x*screen_height+y)*3] = objects[idx*7+4];
                        result[(x*screen_height+y)*3+1] = objects[idx*7+5]; 
                        result[(x*screen_height+y)*3+2] = objects[idx*7+6]; 
                    }
                }
                if (min_distance > 30) {
                    if (x < screen_width && y < screen_height) {
                        result[(x*screen_height+y)*3] = 0;
                        result[(x*screen_height+y)*3+1] = 0; 
                        result[(x*screen_height+y)*3+2] = 0; 
                    }
                }
            }
            end_point_x = camera_x + to_camera_x;
            end_point_y = camera_y + to_camera_y;
            end_point_z = camera_z + to_camera_z;
        }
    }
"""
