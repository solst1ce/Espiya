from numpy import *
from cv2 import VideoCapture, imwrite, destroyAllWindows

from utils.config import IMAGE_PATH

class Camera():
    def __init__(self) -> None:
        self.camera = None
        self.status = ""

    def capture_image(self):
        """
        captures still image via camera
        needs to warm up the camera before taking
        a picture with good lighting
        """
        ss_image = "snapshot-image.jpg"

        self.camera = VideoCapture(0)
        if not self.camera.isOpened():
            self.camera = None
            self.status = "[-] Camera is not available on this device!"
            return self.camera, self.status

        for counting in range (1, 30):
            ret, frame = self.camera.read()
            imwrite(f'{IMAGE_PATH}\{ss_image}', frame)
        
        self.camera.release()
        destroyAllWindows()

        return ret, ss_image
        