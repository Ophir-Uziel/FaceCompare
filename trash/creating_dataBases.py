import os
import face_recognition
from scipy.misc import imsave
from matplotlib.pyplot import *



def create_faces_dataBase(main_dir_path):
    tmp_main_path = main_dir_path.split('/')
    new_tmp_main_path = []
    for part in tmp_main_path:
        new_tmp_main_path.append(part + '/')

    main_new_folder_path = "".join(new_tmp_main_path[:len(new_tmp_main_path)-1]) +"new_dataSet"
    if not os.path.exists(main_new_folder_path):
        os.makedirs(main_new_folder_path)

    images = []
    for subdir, dirs, files in os.walk(main_dir_path):
        for dir in dirs:
            pic_dir_path = main_dir_path +"/" + dir
            images_path_list_in_dir = os.listdir(pic_dir_path)

            new_picture_dir = main_new_folder_path + '/' + dir
            if not os.path.exists(new_picture_dir):
                os.makedirs(new_picture_dir)

            for image in images_path_list_in_dir:
                image_path = pic_dir_path +"/" + image
                image_save_path = new_picture_dir + '/' + image
                image_array = face_recognition.load_image_file(image_path)
                try:
                    top, right, bottom, left = face_recognition.face_locations(image_array)[0]
                except IndexError:
                    print("this is the bad picture:", image_path)
                    imshow(image_array)
                    show()
                    print("no faces found in the picture")
                    continue
                face_image = image_array[top:bottom, left:right]
                imsave(image_save_path, face_image)


create_faces_dataBase("/home/ophir/Desktop/dataSets/lfw")