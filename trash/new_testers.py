import os
import face_recognition
import time
from new_functions import *
from matplotlib.pyplot import *


DEBUG = False
DATA_SET_FOLDER_PATH = "/home/ophir/Desktop/dataSets/lfw"
BIG_DS = "/media/ophir/SANDISK/general_ds"
SMALL_DS = "/media/ophir/SANDISK/small_ds"
ALGORITHM = 'FR'

# create a folder if not exist
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


# prints if DEBUG == TRUE
def debug_print(message):
    if DEBUG:
        print(message)


# upload data from files
def load_images(main_dir_path):
    # region : Get all the pictures:
    # in format : [image, true if the person has a few images, false if only 1]
    images = []
    for subdir, dirs, files in os.walk(main_dir_path):
        for dir in dirs:

            pic_dir_path = main_dir_path + "/" + dir
            images_path_list_in_dir = os.listdir(pic_dir_path)

            new_person_images = []
            for i in range(len(images_path_list_in_dir)):
                image = images_path_list_in_dir[i]
                image_path = pic_dir_path + "/" + image
                try:
                    new_person_images.append(face_recognition.load_image_file(image_path))
                except:
                    debug_print("image" + str(i) + "is bad form")

            images.append([new_person_images, dir])
    return images
    # end region


# get person from all person, his images and name
def get_person_from_images(images, person_index):
    person = images[person_index]
    person_images = person[0]
    person_name = person[1]
    return person, person_images, person_name


# save 2 images of same person
def save_2_images_same_person(path, person_name, image1, image2, index1, index2):
    current_comparison_results_folder = path + person_name + '||' + str(index1) + str(index2) + '/'
    create_folder(current_comparison_results_folder)
    imsave(current_comparison_results_folder + str(index1), image1)
    imsave(current_comparison_results_folder + str(index2), image2)


# save 2 images of different persons
def save_2_images_different_persons(path, image1, image2, name1, name2):
    current_comparison_results_folder = path + name1 + "||" + name2 + '/'
    create_folder(current_comparison_results_folder)
    imsave(current_comparison_results_folder + name1, image1)
    imsave(current_comparison_results_folder + name2, image2)


# takes person's images and checks if the algorithem says it is the same person
def compare_person_to_himself(person_images, person_name, compared_himself_path, not_exist_path):
    num_of_images = len(person_images)

    debug_print(person_name + str(num_of_images))

    for i in range(num_of_images):

        # check the picture on the same person's pictures
        for j in range(i + 1, num_of_images):
            current_image = person_images[i]
            check_image = person_images[j]


            start_time = time.time()
            result = compare_images(current_image, check_image, ALGORITHM)
            debug_print("comparing time = " + str(time.time() - start_time))

            if result == DIFFERENT:
                debug_print("Ooh, it just said a person isn't the same with himself")
                save_2_images_same_person(compared_himself_path, person_name, current_image, check_image, i, j)

            elif result == SAME:
                debug_print("Great! found the person identical to itself!")

            elif result == FIRST_IMAGE_NO_FACES:
                imsave(not_exist_path + person_name + str(i), current_image)
            else:
                imsave(not_exist_path + person_name + str(j), check_image)


# create all dirs needed for result images
def create_results_dir(results_folder, compared_himself_folder, failed_folder, not_exist_folder):
    failed_path = results_folder + failed_folder
    not_exist_path = results_folder + not_exist_folder
    compared_himself_path = results_folder + compared_himself_folder

    create_folder(results_folder)
    create_folder(compared_himself_path)
    create_folder(failed_path)
    create_folder(not_exist_path)

    return compared_himself_path, failed_path, not_exist_path


def compare_different_persons(person1_images, person1_name, person2_images, person2_name, failed_path):
    for image1 in person1_images:
        for image2 in person2_images:
            start_time = time.time()
            result = compare_images(image1, image2, ALGORITHM)
            debug_print("comparing time = " + str(time.time() - start_time))
            if result == SAME:
                debug_print("Oops. it said 2 different people are ###THE SAME###!")
                save_2_images_different_persons(failed_path, image1, image2, person1_name, person2_name)

            elif result == DIFFERENT:
                debug_print("Great! it said 2 different people are different!")


def compare_person_to_others_big(images, person_index, failed_path):
    person, person_images, person_name = get_person_from_images(images, person_index)

    num_of_people = len(images)

    for i in range(person_index + 1, num_of_people):
        curr_person, curr_person_images, curr_person_name = get_person_from_images(images, i)
        compare_different_persons(person_images, person_name, curr_person_images, curr_person_name, failed_path)
        if i % 5 == 0:
            print(i)


def big_tester(main_dir_path):
    images = load_images(main_dir_path)
    results_folder = "results_folder/"
    compared_himself_folder = "compared_himself/"
    failed_folder = "failed_pictures/"
    not_exist_folder = "not_exist_faces/"
    compared_himself_path, failed_path, not_exist_path = create_results_dir(results_folder, compared_himself_folder,
                                                                            failed_folder, not_exist_folder)

    num_of_people = len(images)
    for i in range(num_of_people):
        print(i)
        person, person_images, person_name = get_person_from_images(images, i)

        n = len(person_images)
        if n > 1:
            compare_person_to_himself(person_images, person_name, compared_himself_path, not_exist_path)

        compare_person_to_others_big(images, i, failed_path)


big_tester(SMALL_DS)
