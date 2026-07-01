import os
from dotenv import load_dotenv
from py_clob_client_v2 import ClobClient

load_dotenv()


def main() -> None:
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        raise RuntimeError("PRIVATE_KEY no está definido en .env")

    host = os.getenv("CLOB_API_URL", "https://clob.polymarket.com")
    chain_id = int(os.getenv("CLOB_CHAIN_ID", "137"))

    client = ClobClient(
        host=host,
        chain_id=chain_id,
        key=private_key,
    )

    wallet = client.create_deposit_wallet()

    print("=== Deposit Wallet creada ===")
    print(f"DEPOSIT_WALLET_ADDRESS={wallet['address']}")
    print(f"DEPOSIT_WALLET_ID={wallet.get('id', '')}")
    print("\nCopia estos valores en tu archivo .env.")


if __name__ == "__main__":
    main()

