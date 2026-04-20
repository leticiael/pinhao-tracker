from datetime import date, datetime
from pathlib import Path

from modules.arquivo import ler_json, escrever_json

try:
    import oracledb
    ORACLEDB_DISPONIVEL = True
except ImportError:
    oracledb = None
    ORACLEDB_DISPONIVEL = False


TABELAS = (
    "propriedades",
    "arvores",
    "colheitas",
    "registros_climaticos",
    "armazenamentos",
    "precos",
)


class Repositorio:
    def __init__(self, config: dict):
        self.config = config
        self.caminho_json = Path(config["arquivos"]["dados_json"])
        self.conexao = None
        self.usando_oracle = False
        self._preparar_armazenamento_json()
        self._tentar_conectar_oracle()

    def _preparar_armazenamento_json(self) -> None:
        self.caminho_json.parent.mkdir(parents=True, exist_ok=True)
        if not self.caminho_json.exists():
            estrutura = {tabela: [] for tabela in TABELAS}
            escrever_json(str(self.caminho_json), estrutura)

    def _tentar_conectar_oracle(self) -> None:
        if not ORACLEDB_DISPONIVEL:
            print("[AVISO] Biblioteca 'oracledb' nao instalada. Operando em modo JSON.")
            return
        cfg = self.config["oracle"]
        try:
            self.conexao = oracledb.connect(user=cfg["user"], password=cfg["password"], dsn=cfg["dsn"])
        except Exception as erro:
            print(f"[AVISO] Oracle indisponivel ({erro}). Operando em modo JSON.")
            return
        if not self._tabelas_existem():
            print("[AVISO] Tabelas nao encontradas no Oracle. Execute setup_database.sql. Operando em modo JSON.")
            try:
                self.conexao.close()
            except Exception:
                pass
            self.conexao = None
            return
        self.usando_oracle = True
        print("[OK] Conectado ao Oracle Database.")

    def _tabelas_existem(self) -> bool:
        try:
            cursor = self.conexao.cursor()
            for tabela in TABELAS:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela} WHERE ROWNUM = 1")
                cursor.fetchone()
            cursor.close()
            return True
        except Exception:
            return False

    def inserir(self, tabela: str, registro: dict) -> int:
        if self.usando_oracle:
            return self._inserir_oracle(tabela, registro)
        return self._inserir_json(tabela, registro)

    def listar(self, tabela: str, filtros: dict | None = None) -> list[dict]:
        if self.usando_oracle:
            return self._listar_oracle(tabela, filtros)
        return self._listar_json(tabela, filtros)

    def buscar_por_id(self, tabela: str, identificador: int) -> dict | None:
        resultados = self.listar(tabela, {"id": identificador})
        return resultados[0] if resultados else None

    def exportar_tudo(self) -> dict:
        return {tabela: self.listar(tabela) for tabela in TABELAS}

    def fechar(self) -> None:
        if self.conexao is not None:
            try:
                self.conexao.close()
            except Exception:
                pass
            self.conexao = None
            self.usando_oracle = False

    def _inserir_json(self, tabela: str, registro: dict) -> int:
        dados = ler_json(str(self.caminho_json))
        if tabela not in dados:
            dados[tabela] = []
        proximo_id = max((r.get("id", 0) for r in dados[tabela]), default=0) + 1
        registro_normalizado = {chave: self._serializar_valor(valor) for chave, valor in registro.items()}
        novo = {"id": proximo_id, **registro_normalizado}
        dados[tabela].append(novo)
        escrever_json(str(self.caminho_json), dados)
        return proximo_id

    def _listar_json(self, tabela: str, filtros: dict | None) -> list[dict]:
        dados = ler_json(str(self.caminho_json))
        registros = dados.get(tabela, [])
        if not filtros:
            return list(registros)
        return [r for r in registros if all(r.get(chave) == valor for chave, valor in filtros.items())]

    def _inserir_oracle(self, tabela: str, registro: dict) -> int:
        cursor = self.conexao.cursor()
        try:
            valores_oracle = {chave: self._valor_para_oracle(valor) for chave, valor in registro.items()}
            colunas = ", ".join(valores_oracle.keys())
            placeholders = ", ".join(f":{chave}" for chave in valores_oracle.keys())
            novo_id_var = cursor.var(oracledb.NUMBER)
            sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders}) RETURNING id INTO :novo_id_var"
            parametros = {**valores_oracle, "novo_id_var": novo_id_var}
            cursor.execute(sql, parametros)
            self.conexao.commit()
            return int(novo_id_var.getvalue()[0])
        except Exception as erro:
            self.conexao.rollback()
            raise RuntimeError(f"Falha ao inserir em {tabela}: {erro}") from erro
        finally:
            cursor.close()

    def _listar_oracle(self, tabela: str, filtros: dict | None) -> list[dict]:
        cursor = self.conexao.cursor()
        try:
            sql = f"SELECT * FROM {tabela}"
            parametros: dict = {}
            if filtros:
                clausulas = [f"{chave} = :{chave}" for chave in filtros.keys()]
                sql += " WHERE " + " AND ".join(clausulas)
                parametros = {chave: self._valor_para_oracle(valor) for chave, valor in filtros.items()}
            cursor.execute(sql, parametros)
            colunas = [descricao[0].lower() for descricao in cursor.description]
            return [self._normalizar_linha(dict(zip(colunas, linha))) for linha in cursor.fetchall()]
        except Exception as erro:
            raise RuntimeError(f"Falha ao consultar {tabela}: {erro}") from erro
        finally:
            cursor.close()

    @staticmethod
    def _serializar_valor(valor):
        if isinstance(valor, (date, datetime)):
            return valor.isoformat() if isinstance(valor, date) and not isinstance(valor, datetime) else valor.date().isoformat()
        return valor

    @staticmethod
    def _valor_para_oracle(valor):
        if isinstance(valor, str) and len(valor) == 10 and valor[4] == "-" and valor[7] == "-":
            try:
                return datetime.strptime(valor, "%Y-%m-%d").date()
            except ValueError:
                return valor
        return valor

    @staticmethod
    def _normalizar_linha(linha: dict) -> dict:
        resultado = {}
        for chave, valor in linha.items():
            if isinstance(valor, datetime):
                resultado[chave] = valor.date().isoformat()
            elif isinstance(valor, date):
                resultado[chave] = valor.isoformat()
            else:
                resultado[chave] = valor
        return resultado
