import os
import requests
import cv2
import numpy as np

def store_images():
    data = open('pos_url.csv','r')
    url_list = data.readlines()

    if not os.path.exists('pos'):
        os.makedirs('pos')

    img_num = 1
    for i in url_list:
        try:
            img = requests.get(i).content
            open(os.getcwd() + '/pos' + '/' + str(img_num) + '.jpg','wb').write(img)
            print(img_num)
            img_num += 1
        except Exception:
            pass



def remove_broke():
    for file_type in ['pos']:
        for pos_img in os.listdir(file_type):
            for broke in os.listdir('broke_img'):
                try:
                    curent_image_path = str(file_type) + '/' + str(pos_img)
                    broke = cv2.imread('broke_img/'+str(broke))
                    question = cv2.imread(curent_image_path)

                    if broke.shape == question.shape and not (np.bitwise_xor(broke,question).any()):
                        os.remove(curent_image_path)

                except Exception:
                    pass






remove_broke()