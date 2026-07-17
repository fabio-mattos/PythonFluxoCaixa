"""Carrega as configurações de acesso ao banco de dados a partir do .env."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

_REQUIRED_KEYS = ("DB_DRIVER", "DB_SERVER", "DB_DATABASE", "DB_UID", "DB_PWD")


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
        driver=valores["DB_DRIVER"],
        server=valores["DB_SERVER"],
        database=valores["DB_DATABASE"],
        uid=valores["DB_UID"],
        pwd=valores["DB_PWD"],
    )
