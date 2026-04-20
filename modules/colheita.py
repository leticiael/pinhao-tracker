from datetime import date

from modules.arquivo import registrar_log
from modules.validacao import (
    formatar_data,
    ler_data,
    ler_decimal,
    ler_inteiro,
    ler_opcao,
    ler_sim_nao,
)


def registrar_colheita(repositorio, config: dict) -> None:
    print("\n--- Registro de Colheita Diaria ---")
    propriedades = repositorio.listar("propriedades")
    if not propriedades:
        print("  > Cadastre uma propriedade antes de registrar colheitas.")
        return

    propriedade_id = ler_inteiro("ID da propriedade", minimo=1)
    if repositorio.buscar_por_id("propriedades", propriedade_id) is None:
        print("  > Propriedade nao encontrada.")
        return

    data_colheita = ler_data("Data da colheita")
    validar_data_nao_futura(data_colheita)
    kg = ler_decimal("Kg coletados", minimo=0.01, maximo=100000.0)
    metodo = ler_opcao("Metodo", ("chao", "escalada"))
    uso_epi = ler_sim_nao("Uso de EPI")

    verificar_periodo_safra(data_colheita, kg, config)
    avaliar_seguranca(metodo, uso_epi)

    registro = {
        "propriedade_id": propriedade_id,
        "data_colheita": data_colheita.isoformat(),
        "kg_coletados": kg,
        "metodo": metodo,
        "uso_epi": "S" if uso_epi else "N",
    }
    try:
        novo_id = repositorio.inserir("colheitas", registro)
    except RuntimeError as erro:
        print(f"  > {erro}")
        return

    registrar_log(
        config["arquivos"]["log_operacoes"],
        f"Colheita id={novo_id} propriedade={propriedade_id} data={data_colheita.isoformat()} kg={kg}",
    )
    print(f"Colheita registrada com ID {novo_id}.")


def listar_colheitas(repositorio, config: dict) -> None:
    colheitas = repositorio.listar("colheitas")
    if not colheitas:
        print("  > Nenhuma colheita registrada.")
        return
    print("\n--- Historico de Colheitas ---")
    print(f"{'ID':<4} {'Prop.':<6} {'Data':<12} {'Kg':>10} {'Metodo':<10} {'EPI':<4}")
    print("-" * 50)
    for c in sorted(colheitas, key=lambda r: str(r["data_colheita"]), reverse=True):
        print(
            f"{c['id']:<4} {c['propriedade_id']:<6} "
            f"{formatar_data(c['data_colheita']):<12} "
            f"{float(c['kg_coletados']):>10.2f} "
            f"{c['metodo']:<10} {c['uso_epi']:<4}"
        )
    total_kg = sum(float(c["kg_coletados"]) for c in colheitas)
    print("-" * 50)
    print(f"Total acumulado: {total_kg:.2f} kg ({len(colheitas)} registros)")


def validar_data_nao_futura(data_colheita: date) -> None:
    if data_colheita > date.today():
        print("[AVISO] Data informada esta no futuro. Confirme se foi digitada corretamente.")


def verificar_periodo_safra(data_colheita: date, kg: float, config: dict) -> None:
    inicio = config["safra"]["inicio_mes_dia"]
    fim = config["safra"]["fim_mes_dia"]
    instrucao = config["safra"]["instrucao_normativa"]
    mes_dia = data_colheita.strftime("%m-%d")
    if inicio <= mes_dia <= fim:
        print(f"[OK] Colheita dentro do periodo de safra oficial ({instrucao}).")
        return
    multa_por_50kg = config["multa"]["valor_reais_por_50kg_min"]
    multa_estimada = (kg / 50.0) * multa_por_50kg
    print(f"[ALERTA] Colheita fora do periodo oficial ({inicio} a {fim}).")
    print(f"         Base legal: {instrucao}.")
    print(f"         Multa minima estimada: R$ {multa_estimada:,.2f} (R$ {multa_por_50kg:.2f} a cada 50 kg).")


def avaliar_seguranca(metodo: str, uso_epi: bool) -> None:
    if metodo == "escalada" and not uso_epi:
        print("[ALERTA SEGURANCA] Coleta por escalada sem EPI representa risco grave de queda.")
    elif metodo == "escalada":
        print("[OK] Coleta por escalada com EPI registrado.")
    elif not uso_epi:
        print("[INFO] Coleta no chao: recomenda-se luvas e calcados de protecao.")


def produtividade_por_propriedade(repositorio) -> dict[int, float]:
    colheitas = repositorio.listar("colheitas")
    totais: dict[int, float] = {}
    for c in colheitas:
        propriedade_id = int(c["propriedade_id"])
        totais[propriedade_id] = totais.get(propriedade_id, 0.0) + float(c["kg_coletados"])
    return totais
