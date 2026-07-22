"""Conexão com o SQL Server e execução da consulta de saldo FAPEU."""
from __future__ import annotations

import sys
from pathlib import Path

import pyodbc

from config import DBConfig

BASE_DIR = Path(getattr(sys, "_MEIPASS", "")) if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
QUERY_PATH = BASE_DIR / "consulta.sql"
QUERY_PATH_CLT_RPA = BASE_DIR / "consulta_clt_rpa.sql"

COLUNAS = (
    "cdProjeto",
    "PRJ",
    "TotalReceita",
    "TotalDespesas",
    "TotalCLT",
    "TotalPessoalNaoContratado",
    "TotalRedoa",
)

COLUNAS_CLT_RPA = (
    "cdProjeto",
    "Ano",
    "Mes",
    "TotalCLT",
    "TotalPessoalNaoContratado",
)


def carregar_consulta() -> str:
    return QUERY_PATH.read_text(encoding="utf-8")


def carregar_consulta_clt_rpa() -> str:
    return QUERY_PATH_CLT_RPA.read_text(encoding="utf-8")


def _executar_consulta(config: DBConfig, query: str) -> list[tuple]:
    with pyodbc.connect(config.connection_string, timeout=30) as conexao:
        cursor = conexao.cursor()
        cursor.execute(query)
        return [tuple(linha) for linha in cursor.fetchall()]


def buscar_saldo_fapeu(config: DBConfig) -> list[tuple]:
    """Executa a consulta.sql e retorna as linhas na ordem de COLUNAS."""
    return _executar_consulta(config, carregar_consulta())


def buscar_saldo_clt_rpa(config: DBConfig) -> list[tuple]:
    """Executa a consulta_clt_rpa.sql e retorna as linhas na ordem de COLUNAS_CLT_RPA."""
    return _executar_consulta(config, carregar_consulta_clt_rpa())
