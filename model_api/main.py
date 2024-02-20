import cv2
import tensorflow as tf
import numpy as np


def predict():
    score = 0
    while True:
        # Capture an image from the camera
        _, image = camera.read()
        # Convert the image to a numpy array
        image = np.array(image)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(image, 1.3, 5)

        if len(faces) >= 1:
            # get face in the image
            (x, y, w, h) = faces[0]
            # Detect eyes on the face
            leye= leye_cascade.detectMultiScale(image[y:y+h, x:x+w], 1.3, 3)
            reye= reye_cascade.detectMultiScale(image[y:y+h, x:x+w], 1.3, 3)
            if len(leye) >= 1 and len(reye) >= 1:
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
                label_left = labels[pred_left]
                label_right = labels[pred_right]
                if label_left == 'Closed' or label_right == 'Closed':
                    score = score + 1
                else:
                    score = score-1
                if score < 0:
                    score = 0
                if score > 24:
                    #Alert for drowsiness on the screen
                    cv2.putText(image, "DROWSINESS ALERT!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                # Draw a rectangle around the face
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # Draw a rectangle around the eye on image
                cv2.rectangle(image, (x + x1, y + y1), (x + x1 + w1, y + y1 + h1), (0, 255, 0), 2)
                cv2.rectangle(image, (x + x2, y + y2), (x + x2 + w2, y + y2 + h2), (0, 255, 0), 2)
                # Display the prediction on the image
                cv2.putText(image, label_left, (x + x1, y + y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(image, label_right, (x + x2, y + y2 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the image with the face detection and prediction
        cv2.imshow('Drowsiness detection', image)

        # Check if the user pressed 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    # Load the trained model
    model = tf.keras.models.load_model('model.h5',compile=False)
    cv2.setUseOptimized(True)
    # Initialize the camera
    camera = cv2.VideoCapture(0)
    # Load the Haar cascade file for face detection
    face_cascade = cv2.CascadeClassifier('haar cascade files\haarcascade_frontalface_alt.xml')
    # Load the Haar cascade file for eye detection
    leye_cascade = cv2.CascadeClassifier('haar cascade files/' + "haarcascade_lefteye_2splits.xml")
    reye_cascade = cv2.CascadeClassifier('haar cascade files/'+ "haarcascade_righteye_2splits.xml")
    labels = ['Closed', 'Open']
    labels2={'Closed':"Drowsiness Detected",'Open':"No Drowsiness Detected"}
    predict()
    # Release the camera
    camera.release()
    cv2.destroyAllWindows()