"""Carrega as configurações de acesso ao banco de dados a partir do .env."""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import pyodbc
from dotenv import load_dotenv

BASE_DIR = Path(getattr(sys, "_MEIPASS", "")) if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

_REQUIRED_KEYS = ("DB_DRIVER", "DB_SERVER", "DB_DATABASE", "DB_UID", "DB_PWD")

# Ordem de preferência para tentar encontrar um driver SQL Server instalado na
# máquina, caso o driver configurado no .env não esteja disponível (o .env é
# embutido no executável em tempo de build, então pode não bater com o que
# está instalado na máquina de cada usuário).
_DRIVERS_PREFERENCIA = (
    "ODBC Driver 18 for SQL Server",
    "ODBC Driver 17 for SQL Server",
    "ODBC Driver 13 for SQL Server",
    "SQL Server Native Client 11.0",
    "SQL Server",
)


def _resolver_driver(driver_configurado: str) -> str:
    disponiveis = set(pyodbc.drivers())
    if driver_configurado in disponiveis:
        return driver_configurado
    for candidato in _DRIVERS_PREFERENCIA:
        if candidato in disponiveis:
            return candidato
    raise RuntimeError(
        f"Nenhum driver ODBC do SQL Server encontrado nesta máquina "
        f"(configurado: '{driver_configurado}'). Instale o 'ODBC Driver 17 for "
        "SQL Server' da Microsoft e tente novamente."
    )


@dataclass(frozen=True)
class DBConfig:
    driver: str
    server: str
    database: str
    uid: str
    pwd: str

    @property
    def connection_string(self) -> str:
        return (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.uid};"
            f"PWD={self.pwd};"
        )


def load_db_config() -> DBConfig:
    valores = {chave: os.getenv(chave) for chave in _REQUIRED_KEYS}
    faltando = [chave for chave, valor in valores.items() if not valor]
    if faltando:
        raise RuntimeError(
            "Variáveis ausentes no arquivo .env: " + ", ".join(faltando)
        )
    return DBConfig(
        driver=_resolver_driver(valores["DB_DRIVER"]),
        server=valores["DB_SERVER"],
        database=valores["DB_DATABASE"],
        uid=valores["DB_UID"],
        pwd=valores["DB_PWD"],
    )
