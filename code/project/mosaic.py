import cv2
import os
import numpy as np
from flask import current_app
import boto3

client = boto3.client(
    's3',
    aws_access_key_id='AKIAYFQ27WLIED4ZG4WZ',
    aws_secret_access_key='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',
    region_name='ap-northeast-1'
)

def mosaic(img, rect, size):
    (x1, y1, x2, y2) = rect
    w = x2 - x1
    h = y2- y1
    i_rect = img[y1:y2, x1:x2]

    i_small = cv2.resize(i_rect, (size, size))
    i_mos = cv2.resize(i_small, (w, h), interpolation=cv2.INTER_AREA)

    img2 = img.copy()
    img2[y1:y2, x1:x2] = i_mos
    return img2

def mosaic_edit(img_array , row_picture_file):
    cascade_file = "/code/project/static/haarcascade_frontalface_alt.xml"
    cascade = cv2.CascadeClassifier(cascade_file)
    picture_fn = row_picture_file.filename
    picture_path = os.path.join(current_app.root_path, 'static/after_image', picture_fn)
    img = cv2.imdecode(img_array, 1)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_list = cascade.detectMultiScale(img_gray, minSize=(150,150))

    if len(face_list) == 0:
        print("失敗")
        quit()

    for (x,y,w,h) in face_list:
        img = mosaic(img, (x, y, x+w, y+h), 10)

    dst = cv2.resize(img, (600, 600))
    cv2.imwrite(picture_path, dst)

    Filename = picture_path
    Bucket = 'mosaic-app-docker'
    Key = '/after_image/' + picture_fn
    client.upload_file(Filename, Bucket, Key)

    return picture_fn
