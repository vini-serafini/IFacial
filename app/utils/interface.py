import cv2
import numpy as np

from datetime import datetime

from app.config.settings import (
    ESCALA_FRAME
)

# ==========================
# CONFIG
# ==========================

LARGURA = 400
ALTURA = 740

ALTURA_CAMERA = 500


# ==========================
# CANTOS DO BOX
# ==========================

def desenhar_cantos(
    img,
    left,
    top,
    right,
    bottom,
    color=(255, 255, 255),
    thickness=2,
    tamanho=18
):

    # superior esquerdo
    cv2.line(
        img,
        (left, top),
        (left + tamanho, top),
        color,
        thickness
    )

    cv2.line(
        img,
        (left, top),
        (left, top + tamanho),
        color,
        thickness
    )

    # superior direito
    cv2.line(
        img,
        (right, top),
        (right - tamanho, top),
        color,
        thickness
    )

    cv2.line(
        img,
        (right, top),
        (right, top + tamanho),
        color,
        thickness
    )

    # inferior esquerdo
    cv2.line(
        img,
        (left, bottom),
        (left + tamanho, bottom),
        color,
        thickness
    )

    cv2.line(
        img,
        (left, bottom),
        (left, bottom - tamanho),
        color,
        thickness
    )

    # inferior direito
    cv2.line(
        img,
        (right, bottom),
        (right - tamanho, bottom),
        color,
        thickness
    )

    cv2.line(
        img,
        (right, bottom),
        (right, bottom - tamanho),
        color,
        thickness
    )


# ==========================
# REDIMENSIONAR SEM DISTORCER
# ==========================

def redimensionar_sem_distorcer(
    frame,
    largura,
    altura
):

    h, w = frame.shape[:2]

    escala = max(
        largura / w,
        altura / h
    )

    novo_w = int(w * escala)
    novo_h = int(h * escala)

    frame = cv2.resize(
        frame,
        (novo_w, novo_h)
    )

    # crop central
    x_offset = (
        novo_w - largura
    ) // 2

    y_offset = (
        novo_h - altura
    ) // 2

    frame_cropado = frame[
        y_offset:y_offset + altura,
        x_offset:x_offset + largura
    ]

    return (
        frame_cropado,
        escala,
        x_offset,
        y_offset
    )


# ==========================
# INTERFACE
# ==========================

def desenhar_interface(
    frame,
    face,
    aluno,
    liberado,
    resultado
):

    canvas = np.full(
        (
            ALTURA,
            LARGURA,
            3
        ),
        240,
        dtype=np.uint8
    )

    # ==========================
    # AJUSTE DA CAMERA
    # ==========================

    (
        frame,
        escala_camera,
        x_offset,
        y_offset
    ) = redimensionar_sem_distorcer(
        frame,
        LARGURA,
        ALTURA_CAMERA
    )

    canvas[
        0:ALTURA_CAMERA,
        0:LARGURA
    ] = frame

    # ==========================
    # BOX FACIAL
    # ==========================

    if face is not None:

        top, right, bottom, left = face

        # escala do face_recognition
        escala_face = int(
            1 / ESCALA_FRAME
        )

        # converte coordenadas
        top = int(
            top * escala_face * escala_camera
        ) - y_offset

        right = int(
            right * escala_face * escala_camera
        ) - x_offset

        bottom = int(
            bottom * escala_face * escala_camera
        ) - y_offset

        left = int(
            left * escala_face * escala_camera
        ) - x_offset

        desenhar_cantos(
            canvas,
            left,
            top,
            right,
            bottom,
            color=(255, 255, 255)
        )

    # ==========================
    # PAINEL INFERIOR
    # ==========================

    cor = (
        (0, 180, 0)
        if liberado
        else
        (0, 0, 255)
    )

    cv2.rectangle(
        canvas,
        (0, ALTURA_CAMERA),
        (LARGURA, ALTURA),
        cor,
        -1
    )

    agora = datetime.now()

    hora = agora.strftime(
        '%H:%M'
    )

    data = agora.strftime(
        '%d/%m/%Y'
    )

    status = (
        'LIBERADO'
        if liberado
        else
        'BLOQUEADO'
    )

    # ==========================
    # INFORMAÇÕES DO ALUNO
    # ==========================

    if aluno is not None:

        cv2.putText(
            canvas,
            f'Reconhecido: {aluno.nome}',
            (20, 560),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            canvas,
            f'Turma: {aluno.turma}',
            (20, 600),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # ==========================
    # STATUS
    # ==========================

    cv2.putText(
        canvas,
        f'Status: {status}',
        (20, 640),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # ==========================
    # AULA ATUAL
    # ==========================

    if (
        resultado is not None
        and
        "materia_atual" in resultado
    ):

        aula = resultado[
            "materia_atual"
        ]

        cv2.putText(
            canvas,
            f'Aula: {aula}',
            (20, 680),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

    # ==========================
    # DATA E HORA
    # ==========================

    cv2.putText(
        canvas,
        hora,
        (300, 560),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        canvas,
        data,
        (240, 600),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    return canvas