import cv2

class Camera:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.camera_index = camera_index

    def set_camera(self, camera_index):
        self.cap.release()
        self.cap = cv2.VideoCapture(camera_index)
        self.camera_index = camera_index

    def get_frame(self):
        success, frame = self.cap.read()
        if success:
            ret, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
        return None

    def release(self):
        self.cap.release()
