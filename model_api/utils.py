from constants import MODEL_PATH,LEYE_CLASSIFIER,REYE_CLASSIFIER,FACE_CLASSIFIER,LABELS
import cv2
import tensorflow as tf
import numpy as np
from io import BytesIO
from PIL import Image
def load_classifiers():
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    # Load the Haar cascade file for face detection
    face_cascade = cv2.CascadeClassifier(FACE_CLASSIFIER)
    # Load the Haar cascade file for eye detection
    leye_cascade = cv2.CascadeClassifier(LEYE_CLASSIFIER)
    reye_cascade = cv2.CascadeClassifier(REYE_CLASSIFIER)
    return model,face_cascade,leye_cascade,reye_cascade


def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image


def predict(image,model,face_cascade,leye_cascade,reye_cascade):
    image = np.array(image)
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(image, 1.3, 5)
    if len(faces) < 1:
        return False,-1,-1
    # get face in the image
    (x, y, w, h) = faces[0]
    # Detect eyes on the face
    leye= leye_cascade.detectMultiScale(image[y:y+h, x:x+w], 1.3, 3)
    reye= reye_cascade.detectMultiScale(image[y:y+h, x:x+w], 1.3, 3)
    if len(leye) < 1 or len(reye) < 1:
        return True,LABELS[0],LABELS[0]
    # get left eye in the image
    (x1, y1, w1, h1) = leye[0]
    # get right eye in the image
    (x2, y2, w2, h2) = reye[0]
    # Crop the image to the face
    face = image[y:y + h, x:x + w]
    # Crop the image to the eye using image
    # coordinates from the image
    left_eye = image[y + y1:y + y1 + h1, x + x1:x + x1 + w1]
    right_eye = image[y + y2:y + y2 + h2, x + x2:x + x2 + w2]
    # Resize the eye to the input size of the model
    # Convert to grayscale
    left_eye = cv2.cvtColor(left_eye, cv2.COLOR_BGR2GRAY)
    # Create a 3-channel grayscale image by stacking the grayscale channel three times
    left_eye = cv2.merge([left_eye, left_eye, left_eye])
    right_eye = cv2.cvtColor(right_eye, cv2.COLOR_BGR2GRAY)
    # Create a 3-channel grayscale image by stacking the grayscale channel three times
    right_eye = cv2.merge([right_eye, right_eye, right_eye])
    left_eye = cv2.resize(left_eye, (360, 360))
    right_eye = cv2.resize(right_eye, (360, 360))
    # Predict the label of the eye
    prediction_left= model.predict(left_eye[None, ...],verbose=0)[0]
    prediction_right = model.predict(right_eye[None, ...],verbose=0)[0]
    pred_left=prediction_left.argmax()
    pred_right=prediction_right.argmax()
    print(pred_right, pred_left)
    # Get the labels
    print(pred_right,pred_left)
    label_left = LABELS[pred_left]
    label_right = LABELS[pred_right]
    return True,label_right,label_left