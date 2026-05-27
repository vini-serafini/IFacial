from app.services.cadastro_service import (
    CadastroService
)


class CadastroController:

    @staticmethod
    def executar():

        matricula = input(
            'Matrícula: '
        )

        nome = input(
            'Nome: '
        )

        turma = input(
            'Turma (1A, 1B, 2A...): '
        ).upper()

        caminho_imagem = input(
            'Caminho da imagem: '
        )

        CadastroService.cadastrar(
            matricula,
            nome,
            turma,
            caminho_imagem
        )