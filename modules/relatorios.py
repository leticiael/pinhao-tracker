from modules.arquivo import exportar_json, registrar_log
from modules.colheita import produtividade_por_propriedade
from modules.validacao import ler_decimal


def produtividade_por_safra(repositorio, config: dict) -> None:
    colheitas = repositorio.listar("colheitas")
    if not colheitas:
        print("  > Nenhuma colheita registrada.")
        return
    totais_por_ano = agrupar_kg_por_ano(colheitas)
    print("\n--- Produtividade por Safra ---")
    print(f"{'Safra':<10} {'Kg Total':>12} {'Registros':>12}")
    print("-" * 40)
    for ano in sorted(totais_por_ano):
        kg = totais_por_ano[ano]["kg"]
        registros = totais_por_ano[ano]["registros"]
        print(f"{ano:<10} {kg:>12.2f} {registros:>12}")
    total = sum(dados["kg"] for dados in totais_por_ano.values())
    print("-" * 40)
    print(f"{'TOTAL':<10} {total:>12.2f}")


def comparativo_entre_anos(repositorio, config: dict) -> None:
    colheitas = repositorio.listar("colheitas")
    if not colheitas:
        print("  > Nenhuma colheita registrada.")
        return
    totais = agrupar_kg_por_ano(colheitas)
    anos_ordenados = sorted(totais.keys())
    if len(anos_ordenados) < 2:
        print("  > E necessario ao menos duas safras para comparacao.")
        return
    print("\n--- Comparativo entre Safras ---")
    print(f"{'Safra':<8} {'Kg':>12} {'Variacao %':>14} {'Variacao abs.':>16}")
    print("-" * 55)
    anterior_kg: float | None = None
    for ano in anos_ordenados:
        kg = totais[ano]["kg"]
        if anterior_kg is None:
            print(f"{ano:<8} {kg:>12.2f} {'-':>14} {'-':>16}")
        else:
            variacao_abs = kg - anterior_kg
            variacao_pct = (variacao_abs / anterior_kg * 100) if anterior_kg > 0 else 0.0
            print(f"{ano:<8} {kg:>12.2f} {variacao_pct:>13.2f}% {variacao_abs:>16.2f}")
        anterior_kg = kg


def custo_versus_receita(repositorio, config: dict) -> None:
    colheitas = repositorio.listar("colheitas")
    if not colheitas:
        print("  > Nenhuma colheita registrada.")
        return
    precos = repositorio.listar("precos")
    preco_referencia = obter_preco_referencia(precos, config)
    kg_total = sum(float(c["kg_coletados"]) for c in colheitas)
    receita = kg_total * preco_referencia

    print("\n--- Custo vs Receita ---")
    print(f"Kg total colhido:             {kg_total:.2f} kg")
    print(f"Preco de referencia usado:    R$ {preco_referencia:.2f}/kg")
    print(f"Receita bruta estimada:       R$ {receita:,.2f}")
    custo = ler_decimal("Custo operacional total da safra (R$)", minimo=0.0, maximo=10_000_000.0)
    margem = receita - custo
    margem_pct = (margem / receita * 100) if receita > 0 else 0.0
    print("-" * 50)
    print(f"Custo informado:              R$ {custo:,.2f}")
    print(f"Margem liquida:               R$ {margem:,.2f}")
    print(f"Margem percentual:            {margem_pct:.2f}%")
    if margem < 0:
        print("[ALERTA] Operacao com prejuizo no periodo analisado.")
    elif margem_pct < 15:
        print("[ATENCAO] Margem reduzida. Revisar custos e momento de venda.")
    else:
        print("[OK] Margem saudavel para a safra analisada.")


def produtividade_por_propriedade_relatorio(repositorio, config: dict) -> None:
    totais = produtividade_por_propriedade(repositorio)
    if not totais:
        print("  > Nenhuma colheita registrada.")
        return
    propriedades = {int(p["id"]): p for p in repositorio.listar("propriedades")}
    print("\n--- Produtividade por Propriedade ---")
    print(f"{'ID':<4} {'Nome':<25} {'Municipio':<20} {'Kg Total':>12}")
    print("-" * 65)
    for propriedade_id, kg in sorted(totais.items(), key=lambda x: x[1], reverse=True):
        propriedade = propriedades.get(propriedade_id)
        nome = str(propriedade["nome"])[:25] if propriedade else "(removida)"
        municipio = str(propriedade["municipio"])[:20] if propriedade else "-"
        print(f"{propriedade_id:<4} {nome:<25} {municipio:<20} {kg:>12.2f}")
    total_geral = sum(totais.values())
    print("-" * 65)
    print(f"{'TOTAL':<51} {total_geral:>12.2f}")


def exportar_dados_completos(repositorio, config: dict) -> None:
    caminho = config["arquivos"]["exportacao_json"]
    conteudo = {
        "sistema": config["sistema"],
        "dados": repositorio.exportar_tudo(),
    }
    try:
        exportar_json(caminho, conteudo)
    except OSError as erro:
        print(f"  > Falha ao exportar: {erro}")
        return
    registrar_log(config["arquivos"]["log_operacoes"], f"Exportacao JSON gerada em {caminho}")
    print(f"Exportacao salva em: {caminho}")


def agrupar_kg_por_ano(colheitas: list[dict]) -> dict[str, dict]:
    agregado: dict[str, dict] = {}
    for c in colheitas:
        data_str = str(c["data_colheita"])
        ano = data_str[:4]
        entrada = agregado.setdefault(ano, {"kg": 0.0, "registros": 0})
        entrada["kg"] += float(c["kg_coletados"])
        entrada["registros"] += 1
    return agregado


def obter_preco_referencia(precos: list[dict], config: dict) -> float:
    if precos:
        valores = [float(p["preco_kg"]) for p in precos]
        return sum(valores) / len(valores)
    return float(config["precos"]["medio_produtor_2025_kg"])
