#datasets/data is like an image cache
#we import things from the database and store them there
#then we segment the image
#then update database image
#and Push image back to user, maybe along with major things we see in the video
#like road closure

#can we make our program identify what is a car vs what ia a road closure
#maybe we can print that back to the user

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
#from PIL import Image
import numpy as np
import cv2
import sys

cred = credentials.Certificate("backend/private-traffic-survey-firebase-adminsdk-rlpma-d297ab2207.json")

firebase_admin.initialize_app(cred, {

    'storageBucket': 'private-traffic-survey.appspot.com'

})#end of initialization

bucket = storage.bucket()

#Get all imges in storage
blobs = list(bucket.list_blobs(prefix = 'new_images/'))

#Get the name of the most recent image
x = len(blobs)
x = x - 1
blob = blobs[x].name


blob2 = bucket.get_blob(blob)

#blob -> array -> image
#convert blob to string, then string to array of bytes
arr = np.frombuffer(blob2.download_as_string(), np.uint8)

#get actual image
img = cv2.imdecode(arr, cv2.COLOR_BGR2BGR555)

#write code to datasets/dat file
###with open("backend/datasets/data") as outFile:
###    outFile.write(img)



#take most recent in test_results and upload to firebase