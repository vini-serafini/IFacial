from tkinter import Tk
from tkinter.filedialog import askopenfilename

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

        # ==========================
        # SELECIONAR IMAGEM
        # ==========================

        from tkinter import Tk
        from tkinter import filedialog

        root = Tk()

        # Deixa a janela invisível
        root.withdraw()

        # Garante que ela seja criada
        root.update()

        # Coloca ela na frente
        root.attributes("-topmost", True)

        caminho_imagem = filedialog.askopenfilename(
            parent=root,
            title="Selecione a foto do aluno",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png"),
                ("Todos os arquivos", "*.*")
            ]
        )

        root.destroy()

        if not caminho_imagem:

            print(
                "Nenhuma imagem selecionada."
            )

            return

        print(
            f"Imagem selecionada: {caminho_imagem}"
        )

        CadastroService.cadastrar(
            matricula,
            nome,
            turma,
            caminho_imagem
        )