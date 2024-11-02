import cv2
import dlib
import numpy as np
import pickle
import os

path = os.path.dirname(os.path.realpath(__file__))

# Load pre-trained models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(path + "/models/shape_predictor_68_face_landmarks.dat")
faceRecogModel = dlib.face_recognition_model_v1(path + "/models/dlib_face_recognition_resnet_model_v1.dat")

def pickleObject(data):
    return pickle.dumps(data)

def unpickleObject(data):
    return pickle.loads(data)

# Function to compute the 128D face embedding
def getFaceEmbedding(faceImage, shape):
    faceEmbedding = faceRecogModel.compute_face_descriptor(faceImage, shape)
    return np.array(faceEmbedding)

# Function to load an image, detect a face, and compute the embedding
def getEmbeddingFromImage(fileBytes):
    # Read the image from the file object
    alteredFileBytes = np.asarray(bytearray(fileBytes), dtype=np.uint8)  # Read bytes from the file object
    image = cv2.imdecode(alteredFileBytes, cv2.IMREAD_COLOR)  # Decode the image

    if image is None:
        print("Failed to decode image.")
        return None, None
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = detector(gray)
    
    if len(faces) == 0:
        print("No face found in the image.")
        return None, None
    
    # Get the shape of the first detected face (assuming one face per image)
    face = faces[0]
    shape = predictor(gray, face)
    
    # Get the embedding for the face
    embedding = getFaceEmbedding(image, shape)
    
    return embedding, image


# Function to compare two face embeddings using Euclidean distance
def compareFaces(knownEmbedding, newEmbedding, threshold=0.6):
    distance = np.linalg.norm(knownEmbedding - newEmbedding)
    return distance < threshold  # Return True if the distance is below the threshold
