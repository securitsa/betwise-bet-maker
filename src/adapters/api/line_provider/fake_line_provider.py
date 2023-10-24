from core.exceptions.external_exceptions import LineProviderException
from ports.api.line_provider import LineProvider


class FakeLineProvider(LineProvider):
    with_error: bool = False

    async def get_active_events(self):
        if self.with_error:
            raise LineProviderException
