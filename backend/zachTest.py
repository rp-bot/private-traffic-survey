# Get image from storage, use segmentation, and upload new processed image to database

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import numpy as np
# import cv2
import os
print(os.getcwd())

currpath = os.listdir(
    os.getcwd()+'/backend/test_result')

cred = credentials.Certificate(
    "backend/private-traffic-survey-firebase-adminsdk-rlpma-b35f59cfc6.json")

firebase_admin.initialize_app(cred, {

    'storageBucket': 'private-traffic-survey.appspot.com'

})  # end of initialization


def get_latest_image():
    bucket = storage.bucket()
    blobs = bucket.list_blobs() 
    latest_blob = None
    latest_name = ""
    for blob in blobs:
        if not latest_blob or blob.name > latest_name:
            latest_blob = blob
            latest_name = blob.name
    return latest_blob


def download_blob(blob, local_file_path):
    if blob:
        blob.download_to_filename(local_file_path)
        print(f'Downloaded latest image to {local_file_path}')
    else:
        print("No files found in bucket.")


latest_image_blob = get_latest_image()

download_blob(latest_image_blob, os.getcwd() +
              '/backend/downloaded_latest_image.jpg')

