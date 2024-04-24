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
cred = credentials.Certificate("backend/private-traffic-survey-firebase-adminsdk-rlpma-d297ab2207.json")

firebase_admin.initialize_app(cred, {

    'storageBucket': 'private-traffic-survey.appspot.com'

})#end of initialization

bucket = storage.bucket()
blob = bucket.get_blob("AC448CB6-E2A8-43CD-A3C2-F44B89EA2301.jpg")

#blob -> array -> image

#convert blob to string, then string to array of bytes
arr = np.frombuffer(blob.download_as_string(), np.uint8)

#img = Image.frombytes("RGBA", (300, 300), arr)

#img.show()

#get actual image
img = cv2.imdecode(arr, cv2.COLOR_BGR2BGR555)

#img = cv2.imread(img)

cv2.imshow('image', img)
cv2.waitKey(5000)

cv2.destroyAllWindows()


#next I want to write those image to the dataset file
