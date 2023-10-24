class EventNotFoundException(Exception):
    def __init__(self, event_token: str = ""):
        self.event_token = event_token
