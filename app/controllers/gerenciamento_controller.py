from app.services.aluno_service import (
    AlunoService
)

from app.services.gerenciamento_service import (
    GerenciamentoService
)


class GerenciamentoController:

    def iniciar(self):

        matricula = input(
            'Digite a matrícula: '
        )

        aluno = (
            AlunoService
            .buscar_por_matricula(
                matricula
            )
        )

        if not aluno:

            print(
                'Aluno não encontrado'
            )

            return

        print('\n==========')
        print('ALUNO')
        print('==========')

        print(
            f'Nome: {aluno["nome"]}'
        )

        print(
            f'Turma: {aluno["turma"]}'
        )

        print('\n1 - Excluir')
        print('2 - Atualizar')
        print('3 - Voltar')

        opcao = input(
            '\nEscolha: '
        )

        # ==========================
        # EXCLUIR
        # ==========================

        if opcao == '1':

            confirmar = input(
                '\nTem certeza? (s/n): '
            ).lower()

            if confirmar == 's':

                (
                    GerenciamentoService
                    .excluir(
                        matricula
                    )
                )

        # ==========================
        # ATUALIZAR
        # ==========================

        elif opcao == '2':

            novo_nome = input(
                '\nNovo nome: '
            )

            nova_turma = input(
                'Nova turma: '
            ).upper()

            (
                GerenciamentoService
                .atualizar(
                    matricula,
                    novo_nome,
                    nova_turma
                )
            )

        # ==========================
        # VOLTAR
        # ==========================

        elif opcao == '3':

            return

        else:

            print(
                'Opção inválida'
            )