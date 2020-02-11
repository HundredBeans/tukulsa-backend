import face_recognition
import argparse
import pickle
import cv2
import time
from exif import Image
import datetime 
import urllib3
import numpy as np
import cv2
from base64 import b64decode

def face_identification(encoding, image_file, method="cnn"):
    if "http" in image_file:
        resp=urllib3.PoolManager()
        der=resp.request("GET", image_file)
        with open("admin_photo.jpg", "wb") as f:
            f.write(der.data)
       
        image=cv2.imread("admin_photo.jpg")
        width=int(image.shape[1])*(20/100)
        height=int(image.shape[0])*(20/100)
        size=(round(width),round(height))
        image=cv2.resize(image,size)
    else:
        image=cv2.imread(image_file)
        if int(image.shape[1])>400 and int(image.shape[0])>400:
            width=int(image.shape[1])*(20/100)
            height=int(image.shape[0])*(20/100)
            size=(round(width),round(height))
            image=cv2.resize(image,size)
        
    
    data=pickle.loads(open(encoding,"rb").read())
    rgb=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
    boxes=face_recognition.face_locations(rgb, model=method)

    if boxes==[]:
        return "Face Didn't Detected, Please Try Again!"
    
    encodings=face_recognition.face_encodings(rgb,boxes)
    
    names=[]
    # print("ENC", encodings)
    for encoding in encodings:
        comparison=face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.4)
        name="unknown"
        # print("LL",comparison)

        if True in comparison:
            matchedIdxs = [i for (i, b) in enumerate(comparison) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            # name=max(counts)
            name = max(counts, key=counts.get)
            
        names.append(name)
       

        for ((top, right, bottom, left), name) in zip(boxes, names):
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            # print(name)
            cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
    cv2.imshow("image", image)

    if name=="ulum" or name=="daffa":
        cv2.waitKey(10000)
        return "BERHASIL LOGIN"
    else:
        cv2.waitKey(10000)
        return "GAGAL"
        
# print(face_identification("tukulsa_admin.pickle", "alibando.jpeg" ))

