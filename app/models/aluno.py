class Aluno:

    def __init__(
        self,
        id,
        matricula,
        nome,
        turma,
        foto_path,
        encoding_path,
        encoding
    ):

        self.id = id

        self.matricula = matricula

        self.nome = nome

        self.turma = turma

        self.foto_path = foto_path

        self.encoding_path = (
            encoding_path
        )

        self.encoding = encoding