# Get image from storage, use segmentation, and upload new processed image to database

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import numpy as np
# import cv2
import os
import argparse

local_directory = os.getcwd()
firebase_new_directory = 'new_images'
firebase_processed_directory = 'processed_images'


cred = credentials.Certificate(
    local_directory+"/secrets/private-traffic-survey-firebase-adminsdk-rlpma-b35f59cfc6.json")

firebase_admin.initialize_app(cred, {

    'storageBucket': 'private-traffic-survey.appspot.com'

})  # end of initialization


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('command', choices=[
                        'download', 'upload'], help='Command to execute: download or upload')
    return parser.parse_args()


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
    # Ensure the directory path ends with '/'
    if not directory.endswith('/'):
        directory += '/'

    # Initialize storage bucket
    bucket = storage.bucket()

    # List blobs in the specified directory
    blobs = bucket.list_blobs(prefix=directory)
    latest_blob = None
    latest_time = None

    for blob in blobs:
        # Reload metadata
        blob.reload()
        # Compare the 'updated' time
        if not latest_blob or blob.updated > latest_time:
            latest_blob = blob
            latest_time = blob.updated

    return latest_blob


def download_blob(blob, local_file_path):
    if blob:
        blob.download_to_filename(local_file_path)
        print(f'Downloaded latest image to {local_file_path}')
    else:
        print("No files found in the specified bucket directory.")


if __name__ == '__main__':
    # download
    # latest_image_blob = get_latest_image(firebase_new_directory)
    # download_blob(latest_image_blob, os.getcwd() +
    #           '/backend/client_images/temp.jpg')
    args = parse_args()

    if args.command == 'download':
        # Perform the download operation
        latest_image_blob = get_latest_image(firebase_new_directory)
        if latest_image_blob:
            download_blob(latest_image_blob, os.getcwd() +
                          '/client_images/temp.jpg')
        else:
            print("No latest image found to download.")

    elif args.command == 'upload':
        # Perform the upload operation
        latest_processed_image = find_latest_file(
            os.getcwd() + "/test_result")
        if latest_processed_image:
            upload_to_firebase(latest_processed_image,
                               firebase_processed_directory)
        else:
            print("No processed image found to upload.")
