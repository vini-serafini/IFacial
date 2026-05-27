import cv2


class CameraView:

    @staticmethod
    def mostrar(frame):

        cv2.imshow(
            'IFacial',
            frame
        )

    @staticmethod
    def fechar():

        cv2.destroyAllWindows()