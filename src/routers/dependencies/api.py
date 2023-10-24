from fastapi import Depends

from adapters.api.line_provider.btw_line_provider import BTWLineProvider
from adapters.api.line_provider.fake_line_provider import FakeLineProvider
from core.config import get_settings
from core.settings import BaseAppSettings, EnvironmentTypes


def get_line_provider_api(settings: BaseAppSettings = Depends(get_settings)):
    if settings.environment in (EnvironmentTypes.test,):
        return FakeLineProvider()
    return BTWLineProvider(settings)
