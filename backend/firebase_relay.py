# Get image from storage, use segmentation, and upload new processed image to database

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import numpy as np
# import cv2
import os
local_directory = os.getcwd()+"/backend"
firebase_new_directory = 'new_images'
firebase_processed_directory = 'processed_images'

currpath = os.listdir(
    os.getcwd()+'/backend/test_result')

cred = credentials.Certificate(
    local_directory+"/backend/secrets/private-traffic-survey-firebase-adminsdk-rlpma-b35f59cfc6.json")

firebase_admin.initialize_app(cred, {

    'storageBucket': 'private-traffic-survey.appspot.com'

})  # end of initialization


def find_latest_file(directory):
    files = [os.path.join(directory, f) for f in os.listdir(
        directory) if os.path.isfile(os.path.join(directory, f))]
    latest_file = max(files, key=os.path.getmtime)
    return latest_file


def upload_to_firebase(local_file_path, bucket_directory):
    bucket = storage.bucket()
    file_name = os.path.basename(local_file_path)
    blob = bucket.blob(f'{bucket_directory}/{file_name}')
    blob.upload_from_filename(local_file_path)
    print(f'File {file_name} uploaded to {bucket_directory} in the bucket.')


def get_latest_image(directory):
    bucket = storage.bucket()
    # Ensure the directory path ends with a '/'
    if not directory.endswith('/'):
        directory += '/'
    # List blobs in the specified directory
    blobs = bucket.list_blobs(prefix=directory)
    latest_blob = None
    latest_name = ""
    for blob in blobs:
        # Check if this blob's name is greater than the latest known, which means it's the newest if sorted by name
        if not latest_blob or blob.name > latest_name:
            latest_blob = blob
            latest_name = blob.name
    return latest_blob


def download_blob(blob, local_file_path):
    if blob:
        blob.download_to_filename(local_file_path)
        print(f'Downloaded latest image to {local_file_path}')
    else:
        print("No files found in the specified bucket directory.")


# download
latest_image_blob = get_latest_image(firebase_new_directory)
download_blob(latest_image_blob, os.getcwd() +
              '/backend/client_images/temp.jpg')

# upload
latest_processed_image = find_latest_file(
    local_directory+"/backend/test_result")
upload_to_firebase(latest_processed_image, firebase_processed_directory)

if __name__ == '__main__':
    pass
