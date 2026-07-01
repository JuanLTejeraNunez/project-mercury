from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from py_clob_client_v2 import ApiCreds, ClobClient

load_dotenv()


@dataclass
class PolymarketApiCredentials:
    api_key: str
    secret: str
    passphrase: str


def _get_private_key() -> str:
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        raise RuntimeError("PRIVATE_KEY no está definido en .env")
    return private_key


def _get_base_config() -> tuple[str, int]:
    host = os.getenv("CLOB_API_URL", "https://clob.polymarket.com")
    chain_id = int(os.getenv("CLOB_CHAIN_ID", "137"))
    return host, chain_id


def create_api_credentials() -> PolymarketApiCredentials:
    """
    L1 ? L2: usa la private key para crear/derivar las credenciales de API.
    """
    private_key = _get_private_key()
    host, chain_id = _get_base_config()

    client = ClobClient(
        host=host,
        chain_id=chain_id,
        key=private_key,
    )

    creds = client.create_or_derive_api_key()

    return PolymarketApiCredentials(
        api_key=creds["apiKey"],
        secret=creds["secret"],
        passphrase=creds["passphrase"],
    )


def get_authenticated_client() -> ClobClient:
    """
    Devuelve un ClobClient listo para tradear con POLY_1271 (deposit wallet).
    """
    private_key = _get_private_key()
    host, chain_id = _get_base_config()

    api_key = os.getenv("CLOB_API_KEY")
    secret = os.getenv("CLOB_SECRET")
    passphrase = os.getenv("CLOB_PASSPHRASE")
    deposit_wallet = os.getenv("DEPOSIT_WALLET_ADDRESS")

    if not (api_key and secret and passphrase):
        raise RuntimeError(
            "Credenciales L2 no definidas en .env "
            "(CLOB_API_KEY, CLOB_SECRET, CLOB_PASSPHRASE)."
        )

    if not deposit_wallet:
        raise RuntimeError("DEPOSIT_WALLET_ADDRESS no definido en .env")

    creds = ApiCreds(
        api_key=api_key,
        api_secret=secret,
        api_passphrase=passphrase,
    )

    client = ClobClient(
        host=host,
        chain_id=chain_id,
        key=private_key,
        creds=creds,
        signature_type=3,  # POLY_1271
        funder_address=deposit_wallet,
    )

    return client


