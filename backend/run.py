import subprocess
import firebase_relay

#download latest image from new images file in firebase storage
firebase_relay.download()

#run the image segmentation
subprocess.run(["python3", "process.py"])

#upload new image to processed folder in firebase storage
firebase_relay.upload()
