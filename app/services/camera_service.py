import cv2


class CameraService:

    def __init__(self):

        self.cap = cv2.VideoCapture(
            0,
            cv2.CAP_DSHOW
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )

        self.cap.set(
            cv2.CAP_PROP_FPS,
            30
        )

        self.cap.set(
            cv2.CAP_PROP_AUTOFOCUS,
            0
        )

    def ler_frame(self):

        return self.cap.read()

    def liberar(self):

        self.cap.release()