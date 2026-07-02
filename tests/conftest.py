import pytest
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

@pytest.fixture(scope="session", autouse=True)
def kalshi_test_env(tmp_path_factory):
    """
    Fixture global que crea una clave RSA temporal y fija las variables de entorno
    necesarias para inicializar KalshiClient en los tests.
    Usa pytest.MonkeyPatch() internamente para poder ejecutarse con scope=session.
    """
    # crear clave RSA temporal
    key_path = tmp_path_factory.getbasetemp() / "kalshi_test_key.pem"
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    key_path.write_bytes(pem)

    # usar MonkeyPatch manualmente para poder ejecutarlo en scope=session
    mp = pytest.MonkeyPatch()
    mp.setenv("KALSHI_API_KEY_ID", "TEST_API_KEY_ID")
    mp.setenv("KALSHI_PRIVATE_KEY_PATH", str(key_path))
    mp.setenv("KALSHI_BASE_URL", "https://api.kalshi.com")

    yield

    # limpiar variables de entorno al finalizar la sesión
    mp.undo()

