class BaseDataClient:
    """
    Interfaz base para todos los proveedores de datos.
    """

    def get_markets(self):
        raise NotImplementedError("get_markets() debe ser implementado por el proveedor.")

    def get_event(self, event_id):
        raise NotImplementedError("get_event() debe ser implementado por el proveedor.")

    def get_probability(self, event_id):
        raise NotImplementedError("get_probability() debe ser implementado por el proveedor.")

    def get_history(self, event_id):
        raise NotImplementedError("get_history() debe ser implementado por el proveedor.")


