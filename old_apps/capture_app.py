# importing the python open cv library
import cv2
import os


def im_capture():
    # intialize the webcam and pass a constant which is 0
    cam = cv2.VideoCapture(0)

    # title of the app
    cv2.namedWindow('python webcam screenshot app')

    # let's assume the number of images gotten is 0
    img_counter = 0

    # while loop
    while True:
        # intializing the frame, ret
        ret, frame = cam.read()
        # if statement
        if not ret:
            print('failed to grab frame')
            break
        # the frame will show with the title of test
        cv2.imshow('test', frame)
        # to get continuous live video feed from my laptops webcam
        k = cv2.waitKey(1)
        # if the escape key is been pressed, the app will stop
        if k % 256 == 27:
            print('escape hit, closing the app')
            break
        # if the spacebar key is been pressed
        # screenshots will be taken
        elif k % 256 == 32:
            # the format for storing the images scrreenshotted
            img_name = f'opencv_frame_{img_counter}.png'
            # saves the image as a png file
            cv2.imwrite(img_name, frame)
            print('screenshot taken')
            # the number of images automaticallly increases by 1
            img_counter += 1

    # release the camera
    cam.release()

    # stops the camera window
    cv2.destroyAllWindows()

    return img_name


def eye_crop(image_path):
    original_image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                        'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.3,
                                        minNeighbors=5)

    # Assuming there are at least two detected eyes
    if len(eyes) >= 2:
        # Sort the eyes based on x-coordinate
        eyes = sorted(eyes, key=lambda x: x[0])

        # Consider the leftmost and rightmost eyes as a pair
        left_eye, right_eye = eyes[:2]

        # Extract coordinates for the bounding box
        x_left, y_left, w_left, h_left = left_eye
        x_right, y_right, w_right, h_right = right_eye

        # Combine the bounding boxes to include both eyes
        x = min(x_left, x_right)
        y = min(y_left, y_right)
        w = max(x_left + w_left, x_right + w_right) - x
        h = max(y_left + h_left, y_right + h_right) - y

        # Add some padding around the eye pair
        padding = 5
        x -= padding
        y -= padding
        w += 2 * padding
        h += 2 * padding

        # Ensure that the cropped region is within the image boundaries
        x = max(0, x)
        y = max(0, y)
        w = min(original_image.shape[1] - x, w)
        h = min(original_image.shape[0] - y, h)

        # Crop the image to the eye pair region
        cropped_image = original_image[y:y + h, x:x + w]

        # Display the original and cropped images (optional)
        cv2.imshow('Original Image', original_image)
        cv2.imshow('Cropped Image', cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        file_path = os.path.join('webcam_eyes', 'cropped_eyes.jpg')
        # Save the cropped image
        cv2.imwrite(file_path, cropped_image)

        # Delete original image
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"File {image_path} has been deleted successfully.")
        else:
            print(f"File {image_path} not found.")
    else:
        print("At least two eyes are required for eye pair detection.")


# Take webcam picture and save the image path
img_path = im_capture()

# Get cropped eyes image
eyes_img = eye_crop(img_path)
