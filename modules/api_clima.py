import json
from datetime import date
from urllib import error, request
from urllib.parse import urlencode


class APIClimaIndisponivel(Exception):
    pass


def buscar_clima_diario(
    latitude: float,
    longitude: float,
    data_inicio: date,
    data_fim: date,
    url_base: str,
    timeout_segundos: int,
) -> list[dict]:
    parametros = {
        "latitude": f"{latitude:.6f}",
        "longitude": f"{longitude:.6f}",
        "start_date": data_inicio.isoformat(),
        "end_date": data_fim.isoformat(),
        "daily": "temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum",
        "timezone": "America/Sao_Paulo",
    }
    url = f"{url_base}?{urlencode(parametros)}"
    try:
        with request.urlopen(url, timeout=timeout_segundos) as resposta:
            corpo = resposta.read().decode("utf-8")
    except error.HTTPError as erro:
        raise APIClimaIndisponivel(f"API retornou HTTP {erro.code}: {erro.reason}")
    except error.URLError as erro:
        raise APIClimaIndisponivel(f"Falha de rede: {erro.reason}")
    except TimeoutError:
        raise APIClimaIndisponivel(f"Tempo limite excedido ({timeout_segundos}s)")
    except OSError as erro:
        raise APIClimaIndisponivel(f"Erro de IO: {erro}")

    try:
        carga = json.loads(corpo)
    except json.JSONDecodeError as erro:
        raise APIClimaIndisponivel(f"Resposta nao e JSON valido: {erro}")

    diario = carga.get("daily")
    if not diario:
        raise APIClimaIndisponivel("Resposta da API sem bloco 'daily'.")

    datas = diario.get("time", [])
    temperaturas = diario.get("temperature_2m_mean", [])
    umidades = diario.get("relative_humidity_2m_mean", [])
    precipitacoes = diario.get("precipitation_sum", [])

    registros: list[dict] = []
    for indice, data_str in enumerate(datas):
        temperatura = _valor_ou_none(temperaturas, indice)
        umidade = _valor_ou_none(umidades, indice)
        precipitacao = _valor_ou_none(precipitacoes, indice)
        if temperatura is None or umidade is None or precipitacao is None:
            continue
        registros.append({
            "data_registro": data_str,
            "temperatura_celsius": float(temperatura),
            "umidade_percentual": float(umidade),
            "precipitacao_mm": float(precipitacao),
        })
    return registros


def _valor_ou_none(lista: list, indice: int):
    if indice >= len(lista):
        return None
    return lista[indice]
