class ParlayNotFoundException(Exception):
    def __init__(self, parlay_token: str = ""):
        self.parlay_token = parlay_token
