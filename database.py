"""Conexão com o SQL Server e execução da consulta de saldo FAPEU."""
from __future__ import annotations

from pathlib import Path

import pyodbc

from config import DBConfig

BASE_DIR = Path(__file__).resolve().parent
QUERY_PATH = BASE_DIR / "consulta.sql"

COLUNAS = (
    "cdProjeto",
    "PRJ",
    "TotalReceita",
    "TotalDespesas",
    "TotalCLT",
    "TotalPessoalNaoContratado",
    "TotalRedoa",
)


def carregar_consulta() -> str:
    return QUERY_PATH.read_text(encoding="utf-8")


def buscar_saldo_fapeu(config: DBConfig) -> list[tuple]:
    """Executa a consulta.sql e retorna as linhas na ordem de COLUNAS."""
    query = carregar_consulta()
    with pyodbc.connect(config.connection_string, timeout=30) as conexao:
        cursor = conexao.cursor()
        cursor.execute(query)
        return [tuple(linha) for linha in cursor.fetchall()]
