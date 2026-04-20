import json
from datetime import datetime
from pathlib import Path


def carregar_config(caminho: str) -> dict:
    with Path(caminho).open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def registrar_log(caminho: str, operacao: str) -> None:
    caminho_log = Path(caminho)
    caminho_log.parent.mkdir(parents=True, exist_ok=True)
    momento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{momento}] {operacao}\n"
    try:
        with caminho_log.open("a", encoding="utf-8") as arquivo:
            arquivo.write(linha)
    except OSError as erro:
        print(f"  > Falha ao gravar log: {erro}")


def exportar_json(caminho: str, dados: dict) -> None:
    caminho_export = Path(caminho)
    caminho_export.parent.mkdir(parents=True, exist_ok=True)
    with caminho_export.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False, default=str)


def importar_txt_clima(caminho: str) -> list[dict]:
    registros: list[dict] = []
    with Path(caminho).open("r", encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            partes = [p.strip() for p in linha.split(";")]
            if len(partes) != 4:
                print(f"  > Linha {numero} ignorada (esperado 4 campos separados por ';').")
                continue
            try:
                data_iso = datetime.strptime(partes[0], "%d/%m/%Y").date().isoformat()
                registros.append({
                    "data_registro": data_iso,
                    "temperatura_celsius": float(partes[1].replace(",", ".")),
                    "umidade_percentual": float(partes[2].replace(",", ".")),
                    "precipitacao_mm": float(partes[3].replace(",", "."))
                })
            except ValueError:
                print(f"  > Linha {numero} ignorada (formato invalido).")
                continue
    return registros


def ler_json(caminho: str) -> dict:
    with Path(caminho).open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def escrever_json(caminho: str, dados: dict) -> None:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False, default=str)
