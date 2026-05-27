import os
import shutil
import numpy as np
import face_recognition as fr

from app.database.connection import (
    conectar
)


class CadastroService:

    @staticmethod
    def cadastrar(
        matricula,
        nome,
        turma,
        caminho_imagem
    ):

        os.makedirs(
            'data/alunos',
            exist_ok=True
        )

        os.makedirs(
            'data/encodings',
            exist_ok=True
        )

        extensao = os.path.splitext(
            caminho_imagem
        )[1]

        nome_arquivo = (
            f'{matricula}_{nome}'
            f'{extensao}'
        )

        destino_imagem = os.path.join(
            'data/alunos',
            nome_arquivo
        )

        shutil.copy(
            caminho_imagem,
            destino_imagem
        )

        imagem = fr.load_image_file(
            destino_imagem
        )

        encodings = fr.face_encodings(
            imagem
        )

        if len(encodings) == 0:

            print(
                'Nenhum rosto encontrado.'
            )

            return

        encoding = encodings[0]

        caminho_encoding = os.path.join(
            'data/encodings',
            f'{matricula}.npy'
        )

        np.save(
            caminho_encoding,
            encoding
        )

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO alunos
            (
                matricula,
                nome,
                turma,
                foto_path,
                encoding_path
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                matricula,
                nome,
                turma,
                destino_imagem,
                caminho_encoding
            )
        )

        conexao.commit()

        cursor.close()

        conexao.close()

        print(
            'Aluno cadastrado.'
        )