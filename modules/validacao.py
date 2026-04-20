from datetime import date, datetime


def ler_texto_obrigatorio(rotulo: str, tamanho_max: int = 120) -> str:
    while True:
        valor = input(f"{rotulo}: ").strip()
        if not valor:
            print("  > Valor nao pode ser vazio.")
            continue
        if len(valor) > tamanho_max:
            print(f"  > Valor excede {tamanho_max} caracteres.")
            continue
        return valor


def ler_inteiro(rotulo: str, minimo: int | None = None, maximo: int | None = None) -> int:
    while True:
        bruto = input(f"{rotulo}: ").strip()
        try:
            valor = int(bruto)
        except ValueError:
            print("  > Digite um numero inteiro valido.")
            continue
        if minimo is not None and valor < minimo:
            print(f"  > Valor deve ser >= {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"  > Valor deve ser <= {maximo}.")
            continue
        return valor


def ler_decimal(rotulo: str, minimo: float | None = None, maximo: float | None = None) -> float:
    while True:
        bruto = input(f"{rotulo}: ").strip().replace(",", ".")
        try:
            valor = float(bruto)
        except ValueError:
            print("  > Digite um numero decimal valido (use ponto ou virgula).")
            continue
        if minimo is not None and valor < minimo:
            print(f"  > Valor deve ser >= {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"  > Valor deve ser <= {maximo}.")
            continue
        return valor


def ler_data(rotulo: str) -> date:
    while True:
        bruto = input(f"{rotulo} (DD/MM/AAAA): ").strip()
        try:
            return datetime.strptime(bruto, "%d/%m/%Y").date()
        except ValueError:
            print("  > Data invalida. Use o formato DD/MM/AAAA.")


def ler_opcao(rotulo: str, opcoes: tuple[str, ...]) -> str:
    texto_opcoes = "/".join(opcoes)
    while True:
        valor = input(f"{rotulo} ({texto_opcoes}): ").strip().lower()
        if valor in opcoes:
            return valor
        print(f"  > Opcao invalida. Escolha entre: {texto_opcoes}.")


def ler_sim_nao(rotulo: str) -> bool:
    return ler_opcao(rotulo, ("s", "n")) == "s"


def ler_opcao_menu(opcoes_validas: tuple[str, ...]) -> str:
    while True:
        valor = input("Escolha uma opcao: ").strip()
        if valor in opcoes_validas:
            return valor
        print(f"  > Opcao invalida. Disponiveis: {', '.join(opcoes_validas)}.")


def formatar_data(valor) -> str:
    if isinstance(valor, (date, datetime)):
        return valor.strftime("%d/%m/%Y")
    if isinstance(valor, str):
        try:
            return datetime.strptime(valor[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            return valor
    return str(valor)


def converter_data_iso(valor) -> date | None:
    if valor is None:
        return None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if isinstance(valor, str):
        try:
            return datetime.strptime(valor[:10], "%Y-%m-%d").date()
        except ValueError:
            return None
    return None
