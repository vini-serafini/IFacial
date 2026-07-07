import time
import cv2

from app.services.aluno_service import (
    AlunoService
)

from app.services.face_service import (
    FaceService
)

from app.services.camera_service import (
    CameraService
)

from app.services.liberacao_service import (
    LiberacaoService
)

from app.views.camera_view import (
    CameraView
)

from app.utils.interface import (
    desenhar_interface
)

from app.config.settings import (
    TEMPO_COOLDOWN,
    TEMPO_AUSENTE
)


class ReconhecimentoController:

    def __init__(self):

        self.ultimo_resultado = None

        self.alunos = (
            AlunoService.carregar_alunos()
        )

        self.encodings_conhecidos = [
            aluno.encoding
            for aluno in self.alunos
        ]

        self.camera = CameraService()

        # ==========================
        # CONTROLE
        # ==========================

        self.ultimos_acessos = {}

        self.rostos_presentes = {}

        self.ultimo_frame_visto = {}

        # ==========================
        # INTERFACE
        # ==========================

        self.ultimo_aluno = None

        self.ultima_face = None

        self.ultimo_status = False

    # ==========================
    # EXECUTAR
    # ==========================

    def executar(self):

        while True:

            sucesso, frame = (
                self.camera.ler_frame()
            )

            if not sucesso:

                print(
                    'Erro ao acessar webcam'
                )

                break

            agora = time.time()

            # ==========================
            # PROCESSAR FRAME
            # ==========================

            (
                faces,
                encodings
            ) = FaceService.processar_frame(
                frame
            )

            # ==========================
            # RESET
            # ==========================

            self.ultimo_aluno = None

            self.ultima_face = None

            self.ultimo_status = False

            self.ultimo_resultado = None

            # ==========================
            # PROCESSAR ROSTOS
            # ==========================

            for (
                encoding,
                face
            ) in zip(
                encodings,
                faces
            ):

                (
                    comparacoes,
                    distancias,
                    melhor_indice
                ) = FaceService.reconhecer(
                    encoding,
                    self.encodings_conhecidos
                )

                # ==========================
                # RECONHECIDO
                # ==========================

                if (
                    comparacoes[
                        melhor_indice
                    ]
                ):

                    aluno = self.alunos[
                        melhor_indice
                    ]

                    (
                        liberado,
                        resultado
                    ) = self.processar_aluno(
                        aluno,
                        agora
                    )

                    self.ultimo_aluno = aluno

                    self.ultima_face = face

                    self.ultimo_status = liberado

                    self.ultimo_resultado = resultado

                # ==========================
                # DESCONHECIDO
                # ==========================

                else:

                    self.ultimo_aluno = None

                    self.ultima_face = face

                    self.ultimo_status = False

                    self.ultimo_resultado = None

            # ==========================
            # REMOVER AUSENTES
            # ==========================

            self.remover_ausentes(
                agora
            )

            # ==========================
            # INTERFACE
            # ==========================

            tela = desenhar_interface(
                frame,
                self.ultima_face,
                self.ultimo_aluno,
                self.ultimo_status,
                self.ultimo_resultado
            )

            CameraView.mostrar(
                tela
            )

            # ==========================
            # FECHAR
            # ==========================

            if (
                cv2.waitKey(1)
                & 0xFF == ord('q')
            ):

                break

        self.finalizar()

    # ==========================
    # PROCESSAR ALUNO
    # ==========================

    def processar_aluno(
        self,
        aluno,
        agora
    ):

        # ==========================
        # RESULTADO LIBERAÇÃO
        # ==========================

        resultado = (
            LiberacaoService
            .aluno_pode_sair(aluno)
        )

        matricula = aluno.matricula

        # ==========================
        # ÚLTIMO FRAME
        # ==========================

        self.ultimo_frame_visto[
            matricula
        ] = agora

        # ==========================
        # JÁ PRESENTE
        # ==========================

        if (
            matricula
            in self.rostos_presentes
        ):

            estado = (
                self.rostos_presentes[
                    matricula
                ]
            )

            # ==========================
            # LIBERADO
            # ==========================

            if estado == 'liberado':

                return True, resultado

            # ==========================
            # BLOQUEADO
            # ==========================

            elif estado == 'bloqueado':

                ultimo_acesso = (
                    self.ultimos_acessos.get(
                        matricula
                    )
                )

                # nunca liberou antes
                if ultimo_acesso is None:

                    return False, resultado

                tempo_passado = (
                    agora - ultimo_acesso
                )

                restante = int(
                    TEMPO_COOLDOWN -
                    tempo_passado
                )

                # ==========================
                # LIBERAR AUTOMÁTICO
                # ==========================

                if restante <= 0:

                    self.rostos_presentes[
                        matricula
                    ] = 'liberado'

                    self.ultimos_acessos[
                        matricula
                    ] = agora

                    return True, resultado

                return False, resultado

        # ==========================
        # REGRA ESCOLAR
        # ==========================

        liberado = resultado[
            "liberado"
        ]

        bloqueado = not liberado

        # ==========================
        # COOLDOWN
        # ==========================

        ultimo_acesso = (
            self.ultimos_acessos.get(
                matricula
            )
        )

        if ultimo_acesso is not None:

            tempo_passado = (
                agora - ultimo_acesso
            )

            if (
                tempo_passado
                < TEMPO_COOLDOWN
            ):

                bloqueado = True

        # ==========================
        # BLOQUEADO
        # ==========================

        if bloqueado:

            self.rostos_presentes[
                matricula
            ] = 'bloqueado'

            return False, resultado

        # ==========================
        # LIBERADO
        # ==========================

        print(
            f'{aluno.nome} liberado'
        )

        self.ultimos_acessos[
            matricula
        ] = agora

        self.rostos_presentes[
            matricula
        ] = 'liberado'

        return True, resultado

    # ==========================
    # REMOVER AUSENTES
    # ==========================

    def remover_ausentes(
        self,
        agora
    ):

        remover = []

        for matricula in (
            self.ultimo_frame_visto
        ):

            tempo_sem_ver = (
                agora -
                self.ultimo_frame_visto[
                    matricula
                ]
            )

            if (
                tempo_sem_ver
                > TEMPO_AUSENTE
            ):

                remover.append(
                    matricula
                )

        for matricula in remover:

            self.rostos_presentes.pop(
                matricula,
                None
            )

            self.ultimo_frame_visto.pop(
                matricula,
                None
            )

    # ==========================
    # FINALIZAR
    # ==========================

    def finalizar(self):

        self.camera.liberar()

        CameraView.fechar()