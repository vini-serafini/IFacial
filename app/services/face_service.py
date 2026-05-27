import cv2
import numpy as np
import face_recognition as fr

from app.config.settings import (
    ESCALA_FRAME,
    TOLERANCIA_RECONHECIMENTO
)


class FaceService:

    @staticmethod
    def processar_frame(frame):

        frame_pequeno = cv2.resize(
            frame,
            (0, 0),
            fx=ESCALA_FRAME,
            fy=ESCALA_FRAME
        )

        rgb = cv2.cvtColor(
            frame_pequeno,
            cv2.COLOR_BGR2RGB
        )

        faces = fr.face_locations(
            rgb,
            model='hog'
        )

        encodings = fr.face_encodings(
            rgb,
            faces
        )

        return faces, encodings

    @staticmethod
    def reconhecer(
        encoding_teste,
        encodings_conhecidos
    ):

        comparacoes = fr.compare_faces(
            encodings_conhecidos,
            encoding_teste,
            tolerance=TOLERANCIA_RECONHECIMENTO
        )

        distancias = fr.face_distance(
            encodings_conhecidos,
            encoding_teste
        )

        melhor_indice = np.argmin(
            distancias
        )

        return (
            comparacoes,
            distancias,
            melhor_indice
        )