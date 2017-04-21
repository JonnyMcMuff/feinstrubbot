import googlemaps

class GoogleMapManager:
    def __init__(self):
        pass

    def get_map_client(self, token):
        return googlemaps.Client(key=token)
