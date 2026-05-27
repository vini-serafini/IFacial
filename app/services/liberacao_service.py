import gspread

from datetime import datetime

from oauth2client.service_account import (
    ServiceAccountCredentials
)


class LiberacaoService:

    # =========================================================
    # CONFIGURAÇÕES
    # =========================================================

    ABAS = {
        "1a": "1º Ano A 2026",
        "1b": "1º Ano B 2026",
        "2a": "2º Ano A 2026",
        "2b": "2º Ano B 2026",
        "3a": "3º Ano A 2026",
        "3b": "3º Ano B 2026"
    }

    URL_PLANILHA = (
        "https://docs.google.com/spreadsheets/d/"
        "1P0TrHMAze0SBN_YRPHzRT2Z-eOQQ8N0Eqyb4kmEgzm4/"
        "edit?gid=268787651#gid=268787651"
    )

    CREDENCIAL = "credencial.json"

    # =========================================================
    # LINHAS
    # =========================================================

    LINHAS_MANHA = [3, 4, 5, 7, 8]

    LINHAS_TARDE = [10, 11, 12, 14, 15]

    # =========================================================
    # HORÁRIOS
    # =========================================================

    HORARIOS_MANHA = {
        1: ("07:45", "08:30"),
        2: ("08:30", "09:15"),
        3: ("09:15", "10:00"),
        4: ("10:15", "11:00"),
        5: ("11:00", "11:45"),
    }

    HORARIOS_TARDE = {
        1: ("13:00", "13:45"),
        2: ("13:45", "14:30"),
        3: ("14:30", "15:15"),
        4: ("15:30", "16:15"),
        5: ("16:15", "17:00"),
    }

    # =========================================================
    # PALAVRAS LIBERADAS
    # =========================================================

    PALAVRAS_LIBERACAO = [
        "AULA VAGA",
        "REUNIÃO",
        "REUNIAO",
        "CONSELHO",
        "SEM AULA",
        ""
    ]

    # =========================================================
    # GOOGLE SHEETS
    # =========================================================

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = (
        ServiceAccountCredentials
        .from_json_keyfile_name(
            CREDENCIAL,
            scope
        )
    )

    client = gspread.authorize(
        creds
    )

    planilha = client.open_by_url(
        URL_PLANILHA
    )

    # =========================================================
    # LIBERAÇÃO
    # =========================================================

    @staticmethod
    def aluno_pode_sair(aluno):

        turma = aluno.turma.lower()

        # =====================================================
        # ABRIR ABA
        # =====================================================

        aba = (
            LiberacaoService.planilha
            .worksheet(
                LiberacaoService.ABAS[turma]
            )
        )

        dados = aba.get_all_values()

        # =====================================================
        # DATA
        # =====================================================

        data_atual = (
            datetime.now()
            .strftime("%d/%m")
        )
        
       # data_atual = "27/05"
            
        cabecalho = dados[2]

        ultimo_valor = ""

        for i in range(len(cabecalho)):

            if cabecalho[i] != "":

                ultimo_valor = cabecalho[i]

            else:

                cabecalho[i] = ultimo_valor

        # =====================================================
        # COLUNA DO DIA
        # =====================================================

        coluna_dia = None

        for i, valor in enumerate(
            cabecalho
        ):

            texto = valor.strip()

            if data_atual in texto:

                coluna_dia = i
                break

        if coluna_dia is None:

            return {
                "liberado": False,
                "erro": "Data não encontrada"
            }

        # =====================================================
        # HORÁRIO
        # =====================================================

        #agora = datetime.now().time()
        agora = datetime.strptime("15:40", "%H:%M").time()

        hora_1145 = (
            datetime.strptime(
                "11:45",
                "%H:%M"
            ).time()
        )

        hora_1300 = (
            datetime.strptime(
                "13:00",
                "%H:%M"
            ).time()
        )

        hora_1700 = (
            datetime.strptime(
                "17:00",
                "%H:%M"
            ).time()
        )

        periodo = None

        if agora < hora_1145:

            periodo = "MANHA"

            horarios = (
                LiberacaoService
                .HORARIOS_MANHA
            )

            linhas = (
                LiberacaoService
                .LINHAS_MANHA
            )

        elif (
            agora >= hora_1300
            and
            agora <= hora_1700
        ):

            periodo = "TARDE"

            horarios = (
                LiberacaoService
                .HORARIOS_TARDE
            )

            linhas = (
                LiberacaoService
                .LINHAS_TARDE
            )

        elif agora > hora_1700:

            return {
                "liberado": True,
                "periodo": "FIM"
            }

        else:

            return {
                "liberado": False,
                "periodo": "ALMOCO"
            }

        # =====================================================
        # AULA ATUAL
        # =====================================================

        numero_aula_atual = None

        for numero_aula, horario in (
            horarios.items()
        ):

            inicio = (
                datetime.strptime(
                    horario[0],
                    "%H:%M"
                ).time()
            )

            fim = (
                datetime.strptime(
                    horario[1],
                    "%H:%M"
                ).time()
            )

            if inicio <= agora <= fim:

                numero_aula_atual = (
                    numero_aula
                )

                break

        if numero_aula_atual is None:

            return {
                "liberado": False,
                "periodo": periodo,
                "status": "INTERVALO"
            }

        # =====================================================
        # MATÉRIA ATUAL
        # =====================================================

        indice_linha = (
            numero_aula_atual - 1
        )

        linha_aula_atual = (
            linhas[indice_linha]
        )

        materia_atual = (
            dados[
                linha_aula_atual
            ][
                coluna_dia
            ]
            .strip()
        )

        # =====================================================
        # AULAS RESTANTES
        # =====================================================

        aulas_restantes = []

        for linha_idx in (
            linhas[indice_linha:]
        ):

            linha = dados[linha_idx]

            if coluna_dia < len(linha):

                aula = (
                    linha[coluna_dia]
                    .strip()
                    .upper()
                )

                aulas_restantes.append(
                    aula
                )

        # =====================================================
        # LIBERAÇÃO
        # =====================================================

        liberado = True

        for aula in aulas_restantes:

            if (
                aula
                not in
                LiberacaoService
                .PALAVRAS_LIBERACAO
            ):

                liberado = False
                break

        # =====================================================
        # RETORNO
        # =====================================================

        return {

            "liberado": liberado,

            "nome": aluno.nome,

            "turma": aluno.turma,

            "periodo": periodo,

            "data": data_atual,

            "horario": agora.strftime(
                "%H:%M"
            ),

            "aula_atual": (
                numero_aula_atual
            ),

            "materia_atual": (
                materia_atual
            ),

            "aulas_restantes": (
                aulas_restantes
            )
        }