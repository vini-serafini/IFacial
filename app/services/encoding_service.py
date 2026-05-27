import numpy as np

class EncodingService:

    @staticmethod
    def salvar(
        caminho,
        encoding
    ):

        np.save(
            caminho,
            encoding
        )

    @staticmethod
    def carregar(caminho):

        return np.load(caminho)