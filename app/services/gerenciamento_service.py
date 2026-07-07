import os

from app.database.connection import (
    conectar
)


class GerenciamentoService:

    @staticmethod
    def atualizar(
        matricula,
        novo_nome,
        nova_turma
    ):

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE alunos
            SET nome = %s,
                turma = %s
            WHERE matricula = %s
            """,
            (
                novo_nome,
                nova_turma,
                matricula
            )
        )

        conexao.commit()

        cursor.close()

        conexao.close()

        print(
            '\nAluno atualizado.'
        )

    @staticmethod
    def excluir(
        matricula
    ):

        conexao = conectar()

        cursor = conexao.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM alunos
            WHERE matricula = %s
            """,
            (matricula,)
        )

        aluno = cursor.fetchone()

        if not aluno:

            print(
                '\nAluno não encontrado.'
            )

            return

        # ==========================
        # APAGAR FOTO
        # ==========================

        if os.path.exists(
            aluno['foto_path']
        ):

            os.remove(
                aluno['foto_path']
            )

        # ==========================
        # APAGAR ENCODING
        # ==========================

        if os.path.exists(
            aluno['encoding_path']
        ):

            os.remove(
                aluno['encoding_path']
            )

        # ==========================
        # REMOVER DO BANCO
        # ==========================

        cursor.execute(
            """
            DELETE FROM alunos
            WHERE matricula = %s
            """,
            (matricula,)
        )

        conexao.commit()

        cursor.close()

        conexao.close()

        print(
            '\nAluno removido.'
        )