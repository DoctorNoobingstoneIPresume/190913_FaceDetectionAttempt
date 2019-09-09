import face_recognition
import cv2
import numpy as np

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("../obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("../biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a second sample picture and learn how to recognize it.
andra_image = face_recognition.load_image_file("antrenare/andra/andra1.jpg")
andra_image = face_recognition.load_image_file("antrenare/andra/andra2.jpg")
andra_image = face_recognition.load_image_file("antrenare/andra/andra3.jpg")
andra_face_encoding = face_recognition.face_encodings(andra_image)[0]



# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    andra_face_encoding
]

known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "Andra Tomi"
]
