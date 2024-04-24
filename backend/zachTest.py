#Get image from storage, use segmentation, and upload new processed image to database

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
#from PIL import Image
import numpy as np
import cv2
import os

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

###Do actual image segmentation

#path to grab image from datasets/test_results
newPath = os.listdir('backend/test_results')

#grab most recent image name
y = len(newPath) - 1

#get name of file I want to grab
newImgId = os.listdir('backend/test_results')[y]

#open file and grab image
with open ("backend/test_results") as inFile:
    newImg = inFile.read(newImgId)


#show image
#cv2.imshow('image', newImg)
#cv2.waitkey(5000)
#v2.destroyAllWindows()
