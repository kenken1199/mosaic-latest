import os
import cv2
# import secrets
from PIL import Image
from flask import current_app
import boto3

client = boto3.client(
    's3',
    aws_access_key_id='AKIAYFQ27WLIED4ZG4WZ',
    aws_secret_access_key='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',
    region_name='ap-northeast-1'
)

def save_picture(row_picture_file):
    # random_hex = secrets.token_hex(8)
    # _, f_ext = os.path.splitext(form_picture.filename)
    # picture_fn = random_hex + f_ext
    picture_fn = row_picture_file.filename
    picture_path = os.path.join(current_app.root_path, 'static/before_image', picture_fn)

    output_size = (600, 600)
    i = Image.open(row_picture_file)
    i.thumbnail(output_size)
    i.save(picture_path)

    Filename = picture_path
    Bucket = 'mosaic-app-docker'
    Key = '/before_image/' + picture_fn
    client.upload_file(Filename, Bucket, Key)

    return picture_fn
