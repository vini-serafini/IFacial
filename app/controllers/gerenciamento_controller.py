from app.services.aluno_service import (
    AlunoService
)


class GerenciamentoController:

    def iniciar(self):

        matricula = input(
            'Digite a matrícula: '
        )

        aluno = (
            AlunoService.buscar_por_matricula(
                matricula
            )
        )

        if not aluno:

            print('Aluno não encontrado')
            return

        print(f'\nNome: {aluno["nome"]}')

        print('\n1 - Excluir')
        print('2 - Atualizar')

        opcao = input('\nEscolha: ')