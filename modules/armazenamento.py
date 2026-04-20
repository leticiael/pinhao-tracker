from datetime import date, timedelta

from modules.arquivo import registrar_log
from modules.validacao import (
    converter_data_iso,
    formatar_data,
    ler_data,
    ler_decimal,
    ler_inteiro,
    ler_opcao,
)


METODOS_ARMAZENAMENTO = ("granel", "vacuo", "congelado")


def registrar_armazenamento(repositorio, config: dict) -> None:
    print("\n--- Registro de Armazenamento ---")
    if not repositorio.listar("propriedades"):
        print("  > Cadastre uma propriedade antes.")
        return

    propriedade_id = ler_inteiro("ID da propriedade", minimo=1)
    if repositorio.buscar_por_id("propriedades", propriedade_id) is None:
        print("  > Propriedade nao encontrada.")
        return

    kg = ler_decimal("Kg armazenados", minimo=0.01, maximo=100000.0)
    metodo = ler_opcao("Metodo", METODOS_ARMAZENAMENTO)
    data_entrada = ler_data("Data de entrada no armazenamento")
    prazo = obter_prazo_dias(metodo, config)

    registro = {
        "propriedade_id": propriedade_id,
        "kg_armazenados": kg,
        "metodo": metodo,
        "data_entrada": data_entrada.isoformat(),
        "prazo_dias": prazo,
    }
    try:
        novo_id = repositorio.inserir("armazenamentos", registro)
    except RuntimeError as erro:
        print(f"  > {erro}")
        return

    vencimento = data_entrada + timedelta(days=prazo)
    registrar_log(
        config["arquivos"]["log_operacoes"],
        f"Armazenamento id={novo_id} propriedade={propriedade_id} kg={kg} metodo={metodo} venc={vencimento.isoformat()}",
    )
    print(f"Armazenamento cadastrado com ID {novo_id}.")
    print(f"Validade estimada: {formatar_data(vencimento)} ({prazo} dias).")


def verificar_vencimentos(repositorio, config: dict) -> None:
    armazenamentos = repositorio.listar("armazenamentos")
    if not armazenamentos:
        print("  > Nenhum armazenamento registrado.")
        return
    limite_alerta = int(config["armazenamento"]["dias_alerta_vencimento"])
    hoje = date.today()
    print("\n--- Status de Armazenamento ---")
    print(f"{'ID':<4} {'Prop.':<6} {'Kg':>9} {'Metodo':<10} {'Entrada':<12} {'Vencim.':<12} {'Dias':>6} {'Status':<10}")
    print("-" * 75)
    for item in sorted(armazenamentos, key=lambda x: str(x["data_entrada"])):
        entrada = converter_data_iso(item["data_entrada"])
        if entrada is None:
            continue
        vencimento = entrada + timedelta(days=int(item["prazo_dias"]))
        dias_restantes = (vencimento - hoje).days
        status = classificar_status(dias_restantes, limite_alerta)
        print(
            f"{item['id']:<4} {item['propriedade_id']:<6} "
            f"{float(item['kg_armazenados']):>9.2f} "
            f"{item['metodo']:<10} "
            f"{formatar_data(entrada):<12} "
            f"{formatar_data(vencimento):<12} "
            f"{dias_restantes:>6} {status:<10}"
        )


def obter_prazo_dias(metodo: str, config: dict) -> int:
    mapeamento = {
        "granel": config["armazenamento"]["granel_dias"],
        "vacuo": config["armazenamento"]["vacuo_refrigerado_dias"],
        "congelado": config["armazenamento"]["congelado_dias"],
    }
    return int(mapeamento[metodo])


def classificar_status(dias_restantes: int, limite_alerta: int) -> str:
    if dias_restantes < 0:
        return "VENCIDO"
    if dias_restantes <= limite_alerta:
        return "ALERTA"
    return "OK"
