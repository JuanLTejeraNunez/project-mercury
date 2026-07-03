from src.providers.polymarket_client import PolymarketClient

class MercuryDataClient:
    """
    Router de proveedores de datos:
    - polymarket (actual)
    """

    def __init__(self, provider="polymarket"):
        provider = provider.lower()

        if provider == "polymarket":
            self.client = PolymarketClient()
        else:
            raise ValueError(f"Proveedor '{provider}' no estÃ¡ implementado aÃºn.")

    def get_event(self, event_id):
        return self.client.get_event(event_id)

    def get_probability(self, event_id):
        return self.client.get_probability(event_id)

    def get_markets(self):
        return self.client.get_markets()

    def get_history(self, event_id):
        return self.client.get_history(event_id)



