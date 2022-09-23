import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

import runpy
import ast
import os
import csv
from cv2 import cv2
import face_recognition
import imutils
import numpy as np
from gtts import gTTS
import pyttsx3
import speech_recognition as sr
r=sr.Recognizer()
curr_path = os.getcwd()


known_face_encodings = [
]
known_face_names = [
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
speakcmd=pyttsx3.init()




f = open('model.csv','r+' )

with f:
    reader = csv.reader(f)
    
    for row in reader:
        #print(row)
        name , model = row
        model = ast.literal_eval(model)
        model = list(map(float,model))
        print(model)
        known_face_names.append(name)
        known_face_encodings.append(model)




def recognize():
   fi = False
   print("Starting")
   speakcmd.say('Recognizing')
   speakcmd.runAndWait()
   video_capture = cv2.VideoCapture(0)
   

    # Only process every other fram of video to save time
   while not fi:
        ret, frame = video_capture.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (300, 300), fx=0.15, fy=0.15)
        #small_frame =  cv2.resize(frame, (300, 300))   
        #small_frame = frame        
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        
        print("Recognizing")
        for idx , face_encoding in enumerate(face_encodings):
            fi = True
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
            

            # # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                 
                 first_match_index = matches.index(True)
                 name = known_face_names[first_match_index]
                 print(f'''

Face recognized: {name}
''')
                 
                 speakcmd.say('Face Identified ' + name)
                 speakcmd.runAndWait()
            
            else:
                print("hello")
                #return_value, image = video_capture.read()
                #name = input("Enter name: ")
                ni = False
                name = input("Enter name: ")
             #   while not ni:
              #      with sr.Microphone() as source2:
               #         try:
                #            speakcmd.say('State Name')
                 #           speakcmd.runAndWait()
                  #          r.adjust_for_ambient_noise(source2,duration=0.5)
                   #         speakcmd.say('Say Name')
                    #        speakcmd.runAndWait()
                     #       user_said_person_name=r.listen(source2,2,4)
                      #      print(user_said_person_name)
                       #     person_name=r.recognize_google(user_said_person_name)
                        #    print(person_name)
                         #   name=person_name.lower()
                          #  ni=True
                        #except (sr.UnknownValueError,TypeError):
                        #    print("Error")
            # Or instead, use the known face with the smallest distance to the new face
                #face_encoding = face_recognition.face_encodings(frame)[0]
                f = open('model.csv' , 'a')
                with f:
                    writer = csv.writer(f)
                    temp = list(map(str,face_encodings[idx]))
                    writer.writerow([name,temp])
                    
                known_face_encodings.append(face_encodings[idx])
                known_face_names.append(name)
                face_names.append(name)
        
   
   #print(known_face_encodings)

        #process_this_frame = not process_this_frame


    # Display the results
        #for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
         #    top *= 4
          #   right *= 4
           #  bottom *= 4
            # left *= 4

        # Draw a box around the face
 #            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#
        # Draw a label with a name below the face
  #           cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    #         font = cv2.FONT_HERSHEY_DUPLEX
   #          cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
     #   cv2.imshow('Video', frame)
   video_capture.release()
   #cv2.destroyAllWindows()
   print("Exiting")






i=0
def handle_push(channel):
    global i
    #print(f"Sundar presed {i}")
    i+=1
    recognize()
    


GPIO.add_event_detect(10,GPIO.RISING,callback=handle_push,bouncetime=300)

print("Program started")

speakcmd.say('Started Program')
speakcmd.runAndWait()
while True:
    #recognize()
    pass


GPIO.cleanup()
