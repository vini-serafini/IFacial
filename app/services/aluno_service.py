from app.database.connection import conectar

from app.models.aluno import Aluno

from app.services.encoding_service import (
    EncodingService
)


class AlunoService:

    @staticmethod
    def carregar_alunos():

        conn = conectar()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
        SELECT * FROM alunos
        """)

        registros = cursor.fetchall()

        alunos = []

        for registro in registros:

            encoding = (
                EncodingService.carregar(
                    registro[
                        'encoding_path'
                    ]
                )
            )

            aluno = Aluno(

                id=registro['id'],

                matricula=registro[
                    'matricula'
                ],

                nome=registro['nome'],

                turma=registro['turma'],

                foto_path=registro[
                    'foto_path'
                ],

                encoding_path=registro[
                    'encoding_path'
                ],

                encoding=encoding
            )

            alunos.append(aluno)

        conn.close()

        return alunos

    @staticmethod
    def buscar_por_matricula(
        matricula
    ):

        conn = conectar()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
        SELECT * FROM alunos
        WHERE matricula = %s
        """, (matricula,))

        registro = cursor.fetchone()

        conn.close()

        return registro