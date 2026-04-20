import json
import sys
from pathlib import Path

from modules.arquivo import carregar_config, registrar_log
from modules.database import Repositorio
from modules.menu import executar_menu_principal


CAMINHO_CONFIG = "config.json"


def carregar_configuracao(caminho: str) -> dict | None:
    try:
        return carregar_config(caminho)
    except FileNotFoundError:
        print(f"[ERRO] Arquivo de configuracao nao encontrado: {caminho}")
    except json.JSONDecodeError as erro:
        print(f"[ERRO] Configuracao invalida ({erro}).")
    except OSError as erro:
        print(f"[ERRO] Falha ao abrir configuracao: {erro}")
    return None


def executar() -> int:
    diretorio_base = Path(__file__).resolve().parent
    caminho_config = diretorio_base / CAMINHO_CONFIG
    config = carregar_configuracao(str(caminho_config))
    if config is None:
        return 1

    repositorio = Repositorio(config)
    config["__modo_oracle__"] = repositorio.usando_oracle

    registrar_log(config["arquivos"]["log_operacoes"], "Sistema iniciado")
    try:
        executar_menu_principal(repositorio, config)
        return 0
    except KeyboardInterrupt:
        print("\n\nSistema interrompido pelo usuario.")
        return 0
    finally:
        repositorio.fechar()
        registrar_log(config["arquivos"]["log_operacoes"], "Sistema encerrado")


if __name__ == "__main__":
    sys.exit(executar())
