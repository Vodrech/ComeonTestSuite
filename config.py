
class Environment:

    def __init__(self, name, base_url, headers):
        self.name = name
        self.baseURL = base_url
        self.headers = headers
        self.casino = self.baseURL + 'casino/explore'
        self.verify = self.baseURL + 'player/status'
