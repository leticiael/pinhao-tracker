from datetime import date

from modules.arquivo import registrar_log
from modules.validacao import (
    formatar_data,
    ler_decimal,
    ler_inteiro,
    ler_opcao,
    ler_texto_obrigatorio,
)


def cadastrar_propriedade(repositorio, config: dict) -> None:
    print("\n--- Cadastro de Propriedade ---")
    nome = ler_texto_obrigatorio("Nome da propriedade")
    municipio = ler_texto_obrigatorio("Municipio")
    area = ler_decimal("Area (hectares)", minimo=0.01, maximo=100000.0)
    altitude = ler_decimal("Altitude (metros)", minimo=0.0, maximo=3000.0)
    produtor = ler_texto_obrigatorio("Nome do produtor")

    registro = {
        "nome": nome,
        "municipio": municipio,
        "area_hectares": area,
        "altitude_metros": altitude,
        "produtor": produtor,
        "data_cadastro": date.today().isoformat(),
    }
    try:
        novo_id = repositorio.inserir("propriedades", registro)
    except RuntimeError as erro:
        print(f"  > {erro}")
        return

    altitude_ideal = config["arvore"]["altitude_ideal_min_metros"]
    if altitude < altitude_ideal:
        print(f"[ALERTA] Altitude {altitude:.1f}m esta abaixo do ideal ({altitude_ideal}m) para araucaria produtiva.")
    else:
        print(f"[OK] Altitude adequada para a cultura da araucaria.")

    registrar_log(
        config["arquivos"]["log_operacoes"],
        f"Propriedade cadastrada id={novo_id} nome='{nome}' municipio='{municipio}'",
    )
    print(f"Propriedade registrada com ID {novo_id}.")


def cadastrar_arvores(repositorio, config: dict) -> None:
    print("\n--- Cadastro de Arvores ---")
    propriedades = repositorio.listar("propriedades")
    if not propriedades:
        print("  > Nenhuma propriedade cadastrada. Cadastre uma propriedade primeiro.")
        return
    listar_propriedades(repositorio, config)
    propriedade_id = ler_inteiro("ID da propriedade", minimo=1)
    if repositorio.buscar_por_id("propriedades", propriedade_id) is None:
        print("  > Propriedade nao encontrada.")
        return
    tipo = ler_opcao("Tipo", ("nativa", "enxertada"))
    quantidade = ler_inteiro("Quantidade de arvores", minimo=1, maximo=100000)
    idade = ler_inteiro("Idade estimada (anos)", minimo=0, maximo=500)

    faixa = obter_faixa_producao(tipo, config)
    avaliar_idade_arvore(tipo, idade, faixa)
    exibir_estimativa_pinhoes(quantidade, config)

    registro = {
        "propriedade_id": propriedade_id,
        "quantidade": quantidade,
        "tipo": tipo,
        "idade_anos": idade,
    }
    try:
        novo_id = repositorio.inserir("arvores", registro)
    except RuntimeError as erro:
        print(f"  > {erro}")
        return

    registrar_log(
        config["arquivos"]["log_operacoes"],
        f"Arvores cadastradas id={novo_id} propriedade={propriedade_id} tipo={tipo} qtd={quantidade}",
    )
    print(f"Grupo de arvores registrado com ID {novo_id}.")


def listar_propriedades(repositorio, config: dict) -> None:
    propriedades = repositorio.listar("propriedades")
    if not propriedades:
        print("  > Nenhuma propriedade cadastrada.")
        return
    print("\n--- Propriedades ---")
    print(f"{'ID':<4} {'Nome':<25} {'Municipio':<20} {'Area(ha)':>9} {'Alt(m)':>8} {'Produtor':<20}")
    print("-" * 90)
    for p in propriedades:
        print(
            f"{p['id']:<4} "
            f"{str(p['nome'])[:25]:<25} "
            f"{str(p['municipio'])[:20]:<20} "
            f"{float(p['area_hectares']):>9.2f} "
            f"{float(p['altitude_metros']):>8.1f} "
            f"{str(p['produtor'])[:20]:<20}"
        )


def listar_arvores(repositorio, config: dict) -> None:
    arvores = repositorio.listar("arvores")
    if not arvores:
        print("  > Nenhum grupo de arvores cadastrado.")
        return
    print("\n--- Grupos de Arvores ---")
    print(f"{'ID':<4} {'Prop.':<6} {'Tipo':<12} {'Qtd':>6} {'Idade':>6}")
    print("-" * 40)
    for a in arvores:
        print(f"{a['id']:<4} {a['propriedade_id']:<6} {a['tipo']:<12} {a['quantidade']:>6} {a['idade_anos']:>6}")


def obter_faixa_producao(tipo: str, config: dict) -> tuple[int, int]:
    if tipo == "nativa":
        return (
            config["arvore"]["nativa_anos_producao_min"],
            config["arvore"]["nativa_anos_producao_max"],
        )
    return (
        config["arvore"]["enxertada_anos_producao_min"],
        config["arvore"]["enxertada_anos_producao_max"],
    )


def avaliar_idade_arvore(tipo: str, idade: int, faixa: tuple[int, int]) -> None:
    minimo, maximo = faixa
    if idade < minimo:
        print(f"[AVISO] Araucaria {tipo} comeca a produzir entre {minimo} e {maximo} anos. Arvores ainda imaturas.")
    elif idade >= minimo and idade <= maximo + 5:
        print(f"[OK] Arvores em faixa produtiva esperada para tipo {tipo}.")
    else:
        print(f"[INFO] Arvores maduras (acima da faixa esperada de {minimo}-{maximo} anos).")


def exibir_estimativa_pinhoes(quantidade_arvores: int, config: dict) -> None:
    pinhoes_min = config["pinha"]["pinhoes_min"]
    pinhoes_max = config["pinha"]["pinhoes_max"]
    print(
        f"[INFO] Cada pinha contem {pinhoes_min} a {pinhoes_max} pinhoes. "
        f"Considere a producao media de pinhas por arvore para estimar a colheita total."
    )


def exibir_detalhes_propriedade(repositorio, config: dict) -> None:
    listar_propriedades(repositorio, config)
    if not repositorio.listar("propriedades"):
        return
    propriedade_id = ler_inteiro("ID da propriedade", minimo=1)
    propriedade = repositorio.buscar_por_id("propriedades", propriedade_id)
    if not propriedade:
        print("  > Propriedade nao encontrada.")
        return
    arvores = repositorio.listar("arvores", {"propriedade_id": propriedade_id})
    total_arvores = sum(a["quantidade"] for a in arvores)
    print("\n--- Detalhes da Propriedade ---")
    print(f"ID:          {propriedade['id']}")
    print(f"Nome:        {propriedade['nome']}")
    print(f"Municipio:   {propriedade['municipio']}")
    print(f"Area:        {float(propriedade['area_hectares']):.2f} hectares")
    print(f"Altitude:    {float(propriedade['altitude_metros']):.1f} metros")
    print(f"Produtor:    {propriedade['produtor']}")
    print(f"Cadastro:    {formatar_data(propriedade['data_cadastro'])}")
    print(f"Arvores:     {total_arvores} ({len(arvores)} grupos)")
