from modules.api_clima import APIClimaIndisponivel, buscar_clima_diario
from modules.arquivo import importar_txt_clima, registrar_log
from modules.propriedade import listar_propriedades
from modules.validacao import (
    formatar_data,
    ler_data,
    ler_decimal,
    ler_inteiro,
    ler_texto_obrigatorio,
)


COORDENADAS_REFERENCIA = (
    ("Quatro Barras", -25.3676, -49.0775),
    ("Campina Grande do Sul", -25.3056, -49.0572),
)


def registrar_clima_manual(repositorio, config: dict) -> None:
    print("\n--- Registro Climatico Manual ---")
    if not repositorio.listar("propriedades"):
        print("  > Cadastre uma propriedade antes.")
        return

    listar_propriedades(repositorio, config)
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
    listar_propriedades(repositorio, config)
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


def importar_clima_da_api(repositorio, config: dict) -> None:
    api_cfg = config.get("api_clima", {})
    if not api_cfg.get("habilitada", False):
        print("  > Recurso desativado. Ative em config.json -> api_clima.habilitada.")
        return
    print("\n--- Importacao Automatica de Clima (API Open-Meteo) ---")
    print(f"Fonte: {api_cfg.get('atribuicao', 'Open-Meteo')}")
    if not repositorio.listar("propriedades"):
        print("  > Cadastre uma propriedade antes.")
        return
    listar_propriedades(repositorio, config)
    propriedade_id = ler_inteiro("ID da propriedade", minimo=1)
    if repositorio.buscar_por_id("propriedades", propriedade_id) is None:
        print("  > Propriedade nao encontrada.")
        return

    print("Coordenadas de referencia da regiao-alvo:")
    for nome, lat, lon in COORDENADAS_REFERENCIA:
        print(f"  - {nome}: latitude {lat}, longitude {lon}")
    latitude = ler_decimal("Latitude (graus decimais)", minimo=-90.0, maximo=90.0)
    longitude = ler_decimal("Longitude (graus decimais)", minimo=-180.0, maximo=180.0)
    data_inicio = ler_data("Data inicial")
    data_fim = ler_data("Data final")
    if data_fim < data_inicio:
        print("  > Data final anterior a inicial. Operacao cancelada.")
        return

    try:
        registros = buscar_clima_diario(
            latitude=latitude,
            longitude=longitude,
            data_inicio=data_inicio,
            data_fim=data_fim,
            url_base=api_cfg["url_base"],
            timeout_segundos=int(api_cfg.get("timeout_segundos", 15)),
        )
    except APIClimaIndisponivel as erro:
        print(f"  > {erro}")
        print("  > Alternativa: use 'Importar clima de arquivo .txt'.")
        return

    if not registros:
        print("  > Nenhum registro retornado para o periodo informado.")
        return

    importados = 0
    for reg in registros:
        reg["propriedade_id"] = propriedade_id
        try:
            repositorio.inserir("registros_climaticos", reg)
            importados += 1
        except RuntimeError as erro:
            print(f"  > Falha ao inserir: {erro}")

    registrar_log(
        config["arquivos"]["log_operacoes"],
        f"Importacao API clima propriedade={propriedade_id} "
        f"lat={latitude} lon={longitude} "
        f"periodo={data_inicio.isoformat()}/{data_fim.isoformat()} "
        f"registros={importados}",
    )
    print(f"Importacao concluida: {importados} dia(s) baixado(s) da Open-Meteo.")


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
