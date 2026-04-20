from modules.arquivo import registrar_log
from modules.validacao import (
    formatar_data,
    ler_data,
    ler_decimal,
    ler_texto_obrigatorio,
)


def registrar_preco(repositorio, config: dict) -> None:
    print("\n--- Registro de Preco ---")
    data_registro = ler_data("Data do registro")
    preco = ler_decimal("Preco por kg (R$)", minimo=0.01, maximo=1000.0)
    regiao = ler_texto_obrigatorio("Regiao/praca")

    minimo_federal = float(config["precos"]["pgpm_bio_minimo_kg"])
    if preco < minimo_federal:
        print(f"[ALERTA] Preco informado (R$ {preco:.2f}) abaixo do PGPM-Bio (R$ {minimo_federal:.2f}).")

    registro = {
        "data_registro": data_registro.isoformat(),
        "preco_kg": preco,
        "regiao": regiao,
    }
    try:
        novo_id = repositorio.inserir("precos", registro)
    except RuntimeError as erro:
        print(f"  > {erro}")
        return

    registrar_log(
        config["arquivos"]["log_operacoes"],
        f"Preco id={novo_id} data={data_registro.isoformat()} preco={preco} regiao='{regiao}'",
    )
    print(f"Preco cadastrado com ID {novo_id}.")


def listar_precos(repositorio, config: dict) -> None:
    precos = repositorio.listar("precos")
    if not precos:
        print("  > Nenhum preco registrado.")
        return
    print("\n--- Historico de Precos ---")
    print(f"{'ID':<4} {'Data':<12} {'R$/kg':>10} {'Regiao':<30}")
    print("-" * 60)
    for p in sorted(precos, key=lambda r: str(r["data_registro"]), reverse=True):
        print(
            f"{p['id']:<4} "
            f"{formatar_data(p['data_registro']):<12} "
            f"{float(p['preco_kg']):>10.2f} "
            f"{str(p['regiao'])[:30]:<30}"
        )


def analisar_momento_venda(repositorio, config: dict) -> None:
    precos = repositorio.listar("precos")
    if not precos:
        print("  > Nenhum preco registrado para analise.")
        return

    valores = [float(p["preco_kg"]) for p in precos]
    preco_atual = obter_preco_mais_recente(precos)
    media = sum(valores) / len(valores)
    minimo = min(valores)
    maximo = max(valores)

    minimo_federal = float(config["precos"]["pgpm_bio_minimo_kg"])
    referencia = float(config["precos"]["medio_produtor_2025_kg"])
    limiar_favoravel = float(config["precos"]["limiar_venda_favoravel"])
    limiar_desfavoravel = float(config["precos"]["limiar_venda_desfavoravel"])
    nome_referencia = config["precos"]["referencia_medio"]

    print("\n--- Analise de Momento de Venda ---")
    print(f"Registros analisados:        {len(valores)}")
    print(f"Preco mais recente:          R$ {preco_atual:.2f}/kg")
    print(f"Media historica:             R$ {media:.2f}/kg")
    print(f"Minimo registrado:           R$ {minimo:.2f}/kg")
    print(f"Maximo registrado:           R$ {maximo:.2f}/kg")
    print(f"Preco minimo federal (PGPM): R$ {minimo_federal:.2f}/kg")
    print(f"Referencia 2025 ({nome_referencia}): R$ {referencia:.2f}/kg")
    print("-" * 55)

    sugestao = gerar_sugestao(preco_atual, media, minimo_federal, limiar_favoravel, limiar_desfavoravel)
    print(f"SUGESTAO: {sugestao}")


def obter_preco_mais_recente(precos: list[dict]) -> float:
    mais_recente = max(precos, key=lambda p: str(p["data_registro"]))
    return float(mais_recente["preco_kg"])


def gerar_sugestao(
    preco_atual: float,
    media: float,
    minimo_federal: float,
    limiar_favoravel: float,
    limiar_desfavoravel: float,
) -> str:
    if preco_atual < minimo_federal:
        return "AGUARDAR - preco atual abaixo do minimo federal PGPM-Bio."
    if preco_atual >= media * limiar_favoravel:
        return "VENDER AGORA - preco atual acima da media historica."
    if preco_atual < media * limiar_desfavoravel:
        return "AGUARDAR - preco atual abaixo da media historica."
    return "NEUTRO - preco atual em linha com a media. Avaliar custos de armazenagem."
