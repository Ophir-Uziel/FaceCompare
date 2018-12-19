import os
import face_recognition
from trash import functions
from matplotlib.pyplot import *
import random

DEBUG = False
# this one is only the people with their names starting with "a"
DATA_SET_FOLDER_PATH = "/home/ophir/Desktop/dataSets/lfw"

def create_result_dir(results_folder, wrong_pictures_folder,faces_not_found_picture_folder):
    wrong_pictures_folder_path = results_folder + wrong_pictures_folder
    faces_not_found_picture_folder_path = results_folder + faces_not_found_picture_folder

    functions.create_folder(results_folder)
    functions.create_folder(wrong_pictures_folder_path)
    functions.create_folder(faces_not_found_picture_folder_path)

    return wrong_pictures_folder_path,faces_not_found_picture_folder_path

def get_images_from_dir(main_dir_path):
    # region : Get all the pictures:
    # in format : [image, true if the person has a few images, false if only 1]
    images = []
    for subdir, dirs, files in os.walk(main_dir_path):
        for dir in dirs:

            pic_dir_path = main_dir_path + "/" + dir
            images_path_list_in_dir = os.listdir(pic_dir_path)

            new_person_images = []
            for image in images_path_list_in_dir:
                image_path = pic_dir_path + "/" + image
                new_person_images.append(face_recognition.load_image_file(image_path))

            images.append([new_person_images, dir])
    return images
    # end region


def check_on_himself(current_person_images, current_person_name, path):
    results_folder = "comparing_to_himself/"
    results_folder_path = path + results_folder
    functions.create_folder(results_folder_path)
    if DEBUG:
        print(current_person_name, len(current_person_images))
    for i in range(len(current_person_images)):

        # check the picture on the same person's pictures
        for j in range(i + 1, len(current_person_images)):
            current_image = current_person_images[i]
            person_check_image = current_person_images[j]
            if DEBUG:
                print("got before comparison")

            result = functions.compare_between_faces(current_image, person_check_image)

            if DEBUG:
                print("got after comparison with result", result)

            if result == 0:
                if DEBUG:
                    print("Ooh, it just said a person isn't the same with himself")
                current_comparison_results_folder = results_folder_path + current_person_name + str(i) + str(j) + '/'
                functions.create_folder(current_comparison_results_folder)
                imsave(current_comparison_results_folder + str(i), current_image)
                imsave(current_comparison_results_folder + str(j), person_check_image)

            elif result == 1:
                if DEBUG:
                    print("Great! found the person identical to itself!")




def check_on_others_small(images, current_person_images, current_person_name, n, wrong_pictures_folder_path,faces_not_found_picture_folder_path):
    pairs_num = int(n * (n - 1) / 2)
    num_of_people = len(images)
    for j in range(pairs_num):
        person_num = random.randint(0, num_of_people - 1)
        while (person_num == j):
            person_num = random.randint(0, num_of_people - 1)
        check_person = images[person_num]
        check_person_images = check_person[0]
        check_person_name = check_person[1]

        m = len(check_person_images)
        check_person_image_num = random.randint(0, m - 1)
        check_image = check_person_images[check_person_image_num]

        current_person_image_num = random.randint(0, n - 1)
        current_image = current_person_images[current_person_image_num]

        result = functions.compare_between_faces(current_image, check_image)

        if result == functions.DIFFERENT:
            if DEBUG:
                print("Great! it said 2 different people are different!")

        elif result == functions.SAME:
            if DEBUG:
                print("Oops. it said 2 different people are ###THE SAME###!")

            current_comparison_results_folder = wrong_pictures_folder_path + current_person_name + "||" + check_person_name + '/'
            functions.create_folder(current_comparison_results_folder)
            imsave(current_comparison_results_folder + current_person_name + str(person_num), current_image)
            imsave(current_comparison_results_folder + check_person_name + str(j), check_image)

        else:
            if DEBUG:
                print("Damn, faces were not found")
            current_comparison_results_folder = faces_not_found_picture_folder_path + current_person_name + "||" + check_person_name + '/'
            functions.create_folder(current_comparison_results_folder)
            imsave(current_comparison_results_folder + current_person_name + str(person_num), current_image)
            imsave(current_comparison_results_folder + check_person_name + str(j), check_image)


def big_tester(main_dir_path):
    images = []
    for subdir, dirs, files in os.walk(main_dir_path):
        for dir in dirs:

            pic_dir_path = main_dir_path + "/" + dir
            images_path_list_in_dir = os.listdir(pic_dir_path)

            new_person_images = []
            for image in images_path_list_in_dir:
                image_path = pic_dir_path + "/" + image
                new_person_images.append(face_recognition.load_image_file(image_path))

            images.append([new_person_images, dir])

#    for i in range(len(images)):

def small_tester(main_dir_path):

    images = get_images_from_dir(main_dir_path)

    # region : run on the dataSet:

    results_folder = "results_folder/"
    wrong_pictures_folder = "failed_pictures/"
    faces_not_found_picture_folder = "faces_not_found_pictures/"
    wrong_pictures_folder_path, faces_not_found_picture_folder_path = create_result_dir(results_folder, wrong_pictures_folder,faces_not_found_picture_folder)

    num_of_people = len(images)
    for i in range(num_of_people):
        print(i)
        current_person = images[i]
        current_person_images = current_person[0]

        n = len(current_person_images)
        if n < 2:
            continue

        current_person_name = current_person[1]

        check_on_himself(current_person_images, current_person_name, results_folder)

        check_on_others_small(images, current_person_images, current_person_name, n, wrong_pictures_folder_path,faces_not_found_picture_folder_path)
        # check te picture on the other people

small_tester(DATA_SET_FOLDER_PATH)
