from app.views.menu_view import (
    MenuView
)
from app.controllers.cadastro_controller import (
    CadastroController
)
from app.controllers.reconhecimento_controller import (
    ReconhecimentoController
)
from app.controllers.gerenciamento_controller import (
    GerenciamentoController
)


class MenuController:

    def iniciar(self):

        while True:

            opcao = MenuView.mostrar()

            match opcao:

                case '1':
                    CadastroController().executar()
                case '2':
                    ReconhecimentoController().executar()
                case '3':

                    GerenciamentoController().iniciar()
                case '4':
                    break

                case _:

                    print('Opção inválida')