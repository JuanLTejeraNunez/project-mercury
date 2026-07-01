import pytest

from mercury.integrations.polymarket_client import (
    create_api_credentials,
    get_authenticated_client,
    PolymarketApiCredentials,
)


class DummyClobClient:
    def __init__(self, host, chain_id, key, creds=None, signature_type=None, funder_address=None):
        self.host = host
        self.chain_id = chain_id
        self.key = key
        self.creds = creds
        self.signature_type = signature_type
        self.funder_address = funder_address

    def create_or_derive_api_key(self):
        return {
            "apiKey": "test-api-key",
            "secret": "test-secret",
            "passphrase": "test-passphrase",
        }


@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("PRIVATE_KEY", "0xTEST_PRIVATE_KEY")
    monkeypatch.setenv("CLOB_API_URL", "https://clob.polymarket.com")
    monkeypatch.setenv("CLOB_CHAIN_ID", "137")


def test_create_api_credentials(monkeypatch):
    import mercury.integrations.polymarket_client as module
    monkeypatch.setattr(module, "ClobClient", DummyClobClient)

    creds = create_api_credentials()

    assert isinstance(creds, PolymarketApiCredentials)
    assert creds.api_key == "test-api-key"
    assert creds.secret == "test-secret"
    assert creds.passphrase == "test-passphrase"


def test_get_authenticated_client_requires_l2(monkeypatch):
    # Sin L2 en env
    monkeypatch.delenv("CLOB_API_KEY", raising=False)
    monkeypatch.delenv("CLOB_SECRET", raising=False)
    monkeypatch.delenv("CLOB_PASSPHRASE", raising=False)
    monkeypatch.setenv("DEPOSIT_WALLET_ADDRESS", "0xDEPOSIT")

    with pytest.raises(RuntimeError):
        get_authenticated_client()


def test_get_authenticated_client_ok(monkeypatch):
    monkeypatch.setenv("CLOB_API_KEY", "test-api-key")
    monkeypatch.setenv("CLOB_SECRET", "test-secret")
    monkeypatch.setenv("CLOB_PASSPHRASE", "test-passphrase")
    monkeypatch.setenv("DEPOSIT_WALLET_ADDRESS", "0xDEPOSIT")

    import mercury.integrations.polymarket_client as module
    monkeypatch.setattr(module, "ClobClient", DummyClobClient)

    client = get_authenticated_client()

    assert isinstance(client, DummyClobClient)
    assert client.creds is not None
    assert client.creds.api_key == "test-api-key"
    assert client.signature_type == 3
    assert client.funder_address == "0xDEPOSIT"

