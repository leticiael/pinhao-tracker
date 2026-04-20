from modules.arquivo import importar_txt_clima, registrar_log
from modules.validacao import (
    formatar_data,
    ler_data,
    ler_decimal,
    ler_inteiro,
    ler_texto_obrigatorio,
)


def registrar_clima_manual(repositorio, config: dict) -> None:
    print("\n--- Registro Climatico Manual ---")
    if not repositorio.listar("propriedades"):
        print("  > Cadastre uma propriedade antes.")
        return

    propriedade_id = ler_inteiro("ID da propriedade", minimo=1)
    if repositorio.buscar_por_id("propriedades", propriedade_id) is None:
        print("  > Propriedade nao encontrada.")
        return

    data_registro = ler_data("Data do registro")
    temperatura = ler_decimal("Temperatura (C)", minimo=-20.0, maximo=50.0)
    umidade = ler_decimal("Umidade (%)", minimo=0.0, maximo=100.0)
    precipitacao = ler_decimal("Precipitacao (mm)", minimo=0.0, maximo=1000.0)

    avaliar_condicoes(temperatura, umidade, config)

    registro = {
        "propriedade_id": propriedade_id,
        "data_registro": data_registro.isoformat(),
        "temperatura_celsius": temperatura,
        "umidade_percentual": umidade,
        "precipitacao_mm": precipitacao,
    }
    try:
        novo_id = repositorio.inserir("registros_climaticos", registro)
    except RuntimeError as erro:
        print(f"  > {erro}")
        return

    registrar_log(
        config["arquivos"]["log_operacoes"],
        f"Clima id={novo_id} propriedade={propriedade_id} temp={temperatura} umid={umidade} prec={precipitacao}",
    )
    print(f"Registro climatico cadastrado com ID {novo_id}.")


def importar_clima_de_arquivo(repositorio, config: dict) -> None:
    print("\n--- Importacao de Dados Climaticos (.txt) ---")
    print("Formato esperado por linha: DD/MM/AAAA;temperatura;umidade;precipitacao")
    caminho = ler_texto_obrigatorio("Caminho do arquivo .txt")
    if not repositorio.listar("propriedades"):
        print("  > Cadastre uma propriedade antes.")
        return
    propriedade_id = ler_inteiro("ID da propriedade para vincular os registros", minimo=1)
    if repositorio.buscar_por_id("propriedades", propriedade_id) is None:
        print("  > Propriedade nao encontrada.")
        return

    try:
        registros = importar_txt_clima(caminho)
    except FileNotFoundError:
        print(f"  > Arquivo nao encontrado: {caminho}")
        return
    except OSError as erro:
        print(f"  > Erro ao abrir arquivo: {erro}")
        return

    if not registros:
        print("  > Nenhum registro valido encontrado no arquivo.")
        return

    importados = 0
    for reg in registros:
        reg["propriedade_id"] = propriedade_id
        try:
            repositorio.inserir("registros_climaticos", reg)
            importados += 1
        except RuntimeError as erro:
            print(f"  > Falha ao inserir registro: {erro}")

    registrar_log(
        config["arquivos"]["log_operacoes"],
        f"Importacao clima propriedade={propriedade_id} arquivo='{caminho}' registros={importados}",
    )
    print(f"Importacao concluida: {importados} registro(s).")


def listar_registros_climaticos(repositorio, config: dict) -> None:
    registros = repositorio.listar("registros_climaticos")
    if not registros:
        print("  > Nenhum registro climatico.")
        return
    print("\n--- Registros Climaticos ---")
    print(f"{'ID':<4} {'Prop.':<6} {'Data':<12} {'Temp(C)':>9} {'Umid(%)':>9} {'Prec(mm)':>10}")
    print("-" * 55)
    for r in sorted(registros, key=lambda x: str(x["data_registro"]), reverse=True):
        print(
            f"{r['id']:<4} {r['propriedade_id']:<6} "
            f"{formatar_data(r['data_registro']):<12} "
            f"{float(r['temperatura_celsius']):>9.2f} "
            f"{float(r['umidade_percentual']):>9.2f} "
            f"{float(r['precipitacao_mm']):>10.2f}"
        )


def avaliar_condicoes(temperatura: float, umidade: float, config: dict) -> None:
    minimo = config["arvore"]["temperatura_ideal_min_celsius"]
    maximo = config["arvore"]["temperatura_ideal_max_celsius"]
    if temperatura < minimo:
        print(f"[ATENCAO] Temperatura {temperatura:.1f}C abaixo da media ideal anual ({minimo}-{maximo}C).")
    elif temperatura > maximo:
        print(f"[ATENCAO] Temperatura {temperatura:.1f}C acima da media ideal anual ({minimo}-{maximo}C).")
    else:
        print(f"[OK] Temperatura na faixa ideal ({minimo}-{maximo}C).")
    if umidade < 40:
        print(f"[ATENCAO] Umidade baixa ({umidade:.1f}%) pode afetar qualidade do pinhao.")
    elif umidade > 90:
        print(f"[ATENCAO] Umidade alta ({umidade:.1f}%) favorece fungos em estoque.")
