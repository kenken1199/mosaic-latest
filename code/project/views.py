from flask import flash, redirect, render_template, request, url_for
from project.mosaic import mosaic_edit
from project.utils import save_picture
from project import app
import numpy as np
import boto3

client = boto3.client(
    's3',
    aws_access_key_id='AKIAYFQ27WLIED4ZG4WZ',
    aws_secret_access_key='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',
    region_name='ap-northeast-1'
)

@app.route('/', methods=['GET', 'POST'])
def mosaic_view():
    if request.method == 'POST':
        stream = request.files['img_file'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        row_picture_file = request.files['img_file']
        picture_file_before = save_picture(row_picture_file)
        img_url_before = url_for('static', filename='before_image/' + picture_file_before)
        picture_file_after = mosaic_edit(img_array , row_picture_file)
        img_url_after = url_for('static', filename='after_image/' + picture_file_after)

        return render_template('index.html', img_url_before = img_url_before, img_url_after = img_url_after)
    return render_template('index.html')
