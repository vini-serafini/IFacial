import gspread

from datetime import datetime

from oauth2client.service_account import (
    ServiceAccountCredentials
)

print("Aqui é o liberacao_serivice")
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

    # =========================================================
    # PERÍODO DAS TURMAS
    # =========================================================

    url_plan = (
        "https://docs.google.com/spreadsheets/d/"
        "1P0TrHMAze0SBN_YRPHzRT2Z-eOQQ8N0Eqyb4kmEgzm4/"
        "edit?gid=268787651#gid=268787651"
    )

    cred = "credencial.json"

    # =========================================================
    # LINHAS
    # =========================================================

    LINHAS_AULAS = [
        3,
        4,
        5,
        7,
        8,
        10,
        11,
        12,
        14,
        15
    ]

    # =========================================================
    # HORÁRIOS
    # =========================================================

    HORARIOS = {

        1: ("07:45", "08:30"),
        2: ("08:30", "09:15"),
        3: ("09:15", "10:00"),
        4: ("10:15", "11:00"),
        5: ("11:00", "11:45"),

        6: ("13:00", "13:45"),
        7: ("13:45", "14:30"),
        8: ("14:30", "15:15"),
        9: ("15:30", "16:15"),
        10: ("16:15", "17:00")
    }

    # =========================================================
    # PALAVRAS QUE LIBERAM
    # =========================================================

    plv_lib = [
        "AULA VAGA",
        "REUNIÃO",
        "REUNIAO",
        "CONSELHO",
        "SEM AULA",
        ""#,
        #"GEOGRAFIA (GEO.)",
        #"L. PORTUGUESA",
        #"OPT. FIS / PROD. TEX"
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
            cred,
            scope
        )
    )

    client = gspread.authorize(
        creds
    )

    planilha = client.open_by_url(
        url_plan
    )

    # =========================================================
    # LIBERAÇÃO
    # =========================================================

    @staticmethod
    def aluno_pode_sair(aluno):

        print("ENTROU aluno_pode_sair")
        print("Aluno:", aluno.nome)

        turma = aluno.turma.lower()

        linhas = (
            LiberacaoService
            .LINHAS_AULAS
        )

        horarios = (
            LiberacaoService
            .HORARIOS
        )

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
        print("Planilha carregada")

        # =====================================================
        # DATA
        # =====================================================

        hoje = (
            datetime.now()
            .strftime("%d/%m")
        )
        print("Data atual:", hoje)

        # hoje = "28/05"

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

        col_dia = None

        for i, valor in enumerate(
            cabecalho
        ):

            texto = valor.strip()

            if hoje in texto:

                col_dia = i
                break

        print("Coluna encontrada:", col_dia)
        if col_dia is None:

            return {
                "liberado": False,
                "erro": "Data não encontrada"
            }

        # =====================================================
        # HORÁRIO ATUAL
        # =====================================================

        agora = datetime.now().time()
        print("Horario atual:", agora)

        intervalos = [

            ("10:00", "10:15"),

            ("11:45", "13:00"),

            ("15:15", "15:30")
        ]

        for inicio, fim in intervalos:

            h_inicio = datetime.strptime(
                inicio,
                "%H:%M"
            ).time()

            h_fim = datetime.strptime(
                fim,
                "%H:%M"
            ).time()

            if h_inicio <= agora <= h_fim:
                return {

                    "liberado": False,

                    "status": "INTERVALO"
                }

        # agora = datetime.strptime(
        #     "15:40",
        #     "%H:%M"
        # ).time()

        # =====================================================
        # PERÍODO JÁ TERMINOU
        # =====================================================

        hora_final_dia = datetime.strptime(
            "17:00",
            "%H:%M"
        ).time()

        if agora > hora_final_dia:

            return {

                "liberado": True,

                "nome": aluno.nome,

                "turma": aluno.turma,

                "periodo": periodo_turma,

                "data": hoje,

                "horario": agora.strftime(
                    "%H:%M"
                ),

                "status": "FIM_PERIODO"
            }

        # =====================================================
        # DESCOBRIR AULA ATUAL
        # =====================================================

        n_al_agr = None

        for n_al, horario in (
            LiberacaoService
            .HORARIOS.items()
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

                n_al_agr = n_al
                break

        print("Aula atual:", n_al_agr)
        if n_al_agr is None:

            return {

                "liberado": False,

                "periodo": periodo_turma,

                "status": "INTERVALO"
            }

        # =====================================================
        # MATÉRIA ATUAL
        # =====================================================

        i_lin = (
            n_al_agr - 1
        )

        l_al_agr = (
            LiberacaoService
            .LINHAS_AULAS[i_lin]
        )
        print("Linha da aula:", l_al_agr)

        materia_atual = (
            dados[
                l_al_agr
            ][
                col_dia
            ]
            .strip()
        )

        print("Materia atual:", materia_atual)

        # =====================================================
        # AULAS RESTANTES
        # =====================================================

        al_rest = []

        for lin_idx in (
            LiberacaoService
            .LINHAS_AULAS[i_lin:]
        ):

            linha = dados[lin_idx]

            if col_dia < len(linha):

                aula = (
                    linha[col_dia]
                    .strip()
                    .upper()
                )

                al_rest.append(
                    aula
                )

        # =====================================================
        # VERIFICAR LIBERAÇÃO
        # =====================================================

        liberado = True

        for aula in al_rest:

            if (
                aula
                not in
                LiberacaoService
                .plv_lib
            ):

                liberado = False
                break

        # =====================================================
        # RETORNO
        # =====================================================

        print("====Debug====")
        print("Aluno", aluno.nome)
        print("Liberado", liberado)
        print("Aula atual", n_al_agr)
        print("Materia atual", materia_atual)
        print("Aulas Restantes", al_rest)
        print("=======================\n")


        return {

            "liberado": liberado,

            "nome": aluno.nome,

            "turma": aluno.turma,

            "data": hoje,

            "horario": agora.strftime(
                "%H:%M"
            ),

            "aula_atual": (
                n_al_agr
            ),

            "materia_atual": (
                materia_atual
            ),

            "aulas_restantes": (
                al_rest
            )
        }