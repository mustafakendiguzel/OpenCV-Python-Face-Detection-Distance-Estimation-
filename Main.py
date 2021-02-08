import numpy as np
import cv2 

cam = cv2.VideoCapture(0)
face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

known_distance = 40  # kameraya uzaklik
known_width = 12   # yüzünüzün ortalam genisligi

def focal_length(measured_distance, real_width, width_in_rf_image):
   focal_length = (width_in_rf_image * measured_distance)/ real_width
   return focal_length

def distance_finder(Focal_length,real_face_width,face_width_in_frame):
   distance = (real_face_width* Focal_length)/ face_width_in_frame 
   return distance

def face_data(img):
    fotogri = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(fotogri,1.3,2)
    for (x,y,w,h) in faces:
      cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
      global face_width 
      face_width = w
    return face_width

ref_image = cv2.imread('fotom.jpg')
ref_image_face_width = face_data(ref_image)
focal_length_found = focal_length(known_distance,known_width,ref_image_face_width)
fonts = cv2.FONT_HERSHEY_COMPLEX



while True: 
  _,goruntu = cam.read()
  goruntu = cv2.flip(goruntu,1)

  face_width_in_frame = face_data(goruntu)
  if face_width_in_frame !=0:
    Distance = distance_finder(focal_length_found,known_width,face_width_in_frame)
    cv2.putText(goruntu,f"Distance = {Distance}",(50,50),fonts,1,(0,0,255),2)

  cv2.imshow("video",goruntu)
  if cv2.waitKey(30) & 0xFF == ord('q'):
    break
cam.release()
cv2.destroyAllWindows()
