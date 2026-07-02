from mercury.integrations.polymarket_client import create_api_credentials


def main() -> None:
    creds = create_api_credentials()

    print("=== Polymarket API Credentials (L2) ===")
    print(f"CLOB_API_KEY={creds.api_key}")
    print(f"CLOB_SECRET={creds.secret}")
    print(f"CLOB_PASSPHRASE={creds.passphrase}")
    print("\nCopia estos valores en tu archivo .env.")


if __name__ == "__main__":
    main()


