"""Gravação dos dados de saldo FAPEU na planilha Excel."""
from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook

SHEET_NAME = "saldo fapeu"
HEADERS = (
    "cdProjeto",
    "PRJ",
    "TotalReceita",
    "TotalDespesas",
    "TotalCLT",
    "TotalPessoalNaoContratado",
    "TotalRedoa",
)

# Formato contábil brasileiro sem o símbolo de moeda (mesmo padrão já usado na aba "saldo fapeu").
FORMATO_MOEDA_BRL = '_(* #,##0.00_);_(* \\(#,##0.00\\);_(* "-"??_);_(@_)'
COLUNAS_MOEDA = range(3, len(HEADERS) + 1)  # colunas C a G (TotalReceita..TotalRedoa)


class AvisoPlanilha(RuntimeError):
    """Levantado quando o arquivo ou a aba de destino não são encontrados."""


def _parse_valor_brl(valor: str | None) -> float:
    """Converte números formatados em pt-BR (ex.: '1.234,56') para float."""
    if valor is None:
        return 0.0
    texto = str(valor).strip().replace(".", "").replace(",", ".")
    return float(texto) if texto else 0.0


def atualizar_planilha(caminho_planilha: Path, linhas: list[tuple]) -> None:
    """Limpa a aba saldo fapeu e regrava com os dados atuais da consulta."""
    if not caminho_planilha.exists():
        raise AvisoPlanilha(
            f"Arquivo '{caminho_planilha.name}' não encontrado em:\n{caminho_planilha.parent}"
        )

    try:
        workbook = load_workbook(caminho_planilha)
    except PermissionError as exc:
        raise RuntimeError(
            f"Não foi possível abrir '{caminho_planilha.name}'. "
            "Feche o arquivo no Excel e tente novamente."
        ) from exc
    if SHEET_NAME not in workbook.sheetnames:
        raise AvisoPlanilha(f"Aba '{SHEET_NAME}' não encontrada em {caminho_planilha.name}")

    planilha = workbook[SHEET_NAME]
    planilha.delete_rows(1, planilha.max_row)

    planilha.append(HEADERS)
    for cd_projeto, prj, *valores in linhas:
        linha_num = planilha.max_row + 1
        planilha.append([cd_projeto, prj, *(_parse_valor_brl(v) for v in valores)])
        for coluna in COLUNAS_MOEDA:
            planilha.cell(row=linha_num, column=coluna).number_format = FORMATO_MOEDA_BRL

    try:
        workbook.save(caminho_planilha)
    except PermissionError as exc:
        raise RuntimeError(
            f"Não foi possível salvar '{caminho_planilha.name}'. "
            "Feche o arquivo no Excel e tente novamente."
        ) from exc
