from modules.armazenamento import registrar_armazenamento, verificar_vencimentos
from modules.clima import (
    importar_clima_de_arquivo,
    listar_registros_climaticos,
    registrar_clima_manual,
)
from modules.colheita import listar_colheitas, registrar_colheita
from modules.precos import analisar_momento_venda, listar_precos, registrar_preco
from modules.propriedade import (
    cadastrar_arvores,
    cadastrar_propriedade,
    exibir_detalhes_propriedade,
    listar_arvores,
    listar_propriedades,
)
from modules.relatorios import (
    comparativo_entre_anos,
    custo_versus_receita,
    exportar_dados_completos,
    produtividade_por_safra,
)
from modules.validacao import ler_opcao_menu


LARGURA = 62


def executar_menu_principal(repositorio, config: dict) -> None:
    acoes = {
        "1": ("Propriedades e Arvores", submenu_propriedades),
        "2": ("Colheita", submenu_colheita),
        "3": ("Monitoramento Climatico", submenu_clima),
        "4": ("Armazenamento", submenu_armazenamento),
        "5": ("Precos e Venda", submenu_precos),
        "6": ("Relatorios", submenu_relatorios),
        "7": ("Exportar Dados (JSON)", exportar_dados_completos),
    }
    while True:
        imprimir_cabecalho(config)
        for chave, (rotulo, _) in acoes.items():
            print(f"  {chave}. {rotulo}")
        print("  0. Sair")
        print("-" * LARGURA)
        opcao = ler_opcao_menu(tuple(acoes.keys()) + ("0",))
        if opcao == "0":
            print("\nEncerrando Pinhao Tracker. Ate a proxima safra!")
            return
        acao = acoes[opcao][1]
        try:
            acao(repositorio, config)
        except KeyboardInterrupt:
            print("\n  > Operacao cancelada pelo usuario.")
        except Exception as erro:
            print(f"  > Erro inesperado: {erro}")
        input("\nPressione ENTER para continuar...")


def submenu_propriedades(repositorio, config: dict) -> None:
    opcoes = {
        "1": ("Cadastrar propriedade", cadastrar_propriedade),
        "2": ("Cadastrar arvores", cadastrar_arvores),
        "3": ("Listar propriedades", listar_propriedades),
        "4": ("Listar arvores", listar_arvores),
        "5": ("Detalhes de propriedade", exibir_detalhes_propriedade),
    }
    executar_submenu("Propriedades e Arvores", opcoes, repositorio, config)


def submenu_colheita(repositorio, config: dict) -> None:
    opcoes = {
        "1": ("Registrar colheita diaria", registrar_colheita),
        "2": ("Listar colheitas", listar_colheitas),
    }
    executar_submenu("Colheita", opcoes, repositorio, config)


def submenu_clima(repositorio, config: dict) -> None:
    opcoes = {
        "1": ("Registrar clima manualmente", registrar_clima_manual),
        "2": ("Importar clima de arquivo .txt", importar_clima_de_arquivo),
        "3": ("Listar registros climaticos", listar_registros_climaticos),
    }
    executar_submenu("Monitoramento Climatico", opcoes, repositorio, config)


def submenu_armazenamento(repositorio, config: dict) -> None:
    opcoes = {
        "1": ("Registrar entrada em armazenamento", registrar_armazenamento),
        "2": ("Verificar status e vencimentos", verificar_vencimentos),
    }
    executar_submenu("Armazenamento", opcoes, repositorio, config)


def submenu_precos(repositorio, config: dict) -> None:
    opcoes = {
        "1": ("Registrar preco", registrar_preco),
        "2": ("Listar precos", listar_precos),
        "3": ("Analisar momento de venda", analisar_momento_venda),
    }
    executar_submenu("Precos e Venda", opcoes, repositorio, config)


def submenu_relatorios(repositorio, config: dict) -> None:
    opcoes = {
        "1": ("Produtividade por safra", produtividade_por_safra),
        "2": ("Comparativo entre anos", comparativo_entre_anos),
        "3": ("Custo vs Receita", custo_versus_receita),
    }
    executar_submenu("Relatorios", opcoes, repositorio, config)


def executar_submenu(titulo: str, opcoes: dict, repositorio, config: dict) -> None:
    while True:
        print("\n" + "=" * LARGURA)
        print(f"  {titulo}")
        print("=" * LARGURA)
        for chave, (rotulo, _) in opcoes.items():
            print(f"  {chave}. {rotulo}")
        print("  0. Voltar")
        print("-" * LARGURA)
        opcao = ler_opcao_menu(tuple(opcoes.keys()) + ("0",))
        if opcao == "0":
            return
        acao = opcoes[opcao][1]
        try:
            acao(repositorio, config)
        except KeyboardInterrupt:
            print("\n  > Operacao cancelada pelo usuario.")
        except Exception as erro:
            print(f"  > Erro inesperado: {erro}")
        input("\nPressione ENTER para continuar...")


def imprimir_cabecalho(config: dict) -> None:
    sistema = config["sistema"]
    modo = "ORACLE" if config.get("__modo_oracle__") else "JSON"
    print("\n" + "=" * LARGURA)
    print(f"  {sistema['nome']} v{sistema['versao']} - Safra {sistema['ano']}")
    print(f"  Regiao-alvo: {sistema['regiao_alvo']}")
    print(f"  Modo de armazenamento: {modo}")
    print("=" * LARGURA)
