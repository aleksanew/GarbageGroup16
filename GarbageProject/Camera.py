import cv2

class Camera:

    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def capture_frame(self, grayscale:bool):
        ret, frame = self.camera.read()

        if grayscale:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            return frame