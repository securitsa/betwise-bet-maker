from functools import lru_cache

from core import settings

environments = {
    settings.EnvironmentTypes.dev: settings.DevelopmentSettings,
    settings.EnvironmentTypes.test: settings.TestSettings,
    settings.EnvironmentTypes.prod: settings.ProductionSettings,
    settings.EnvironmentTypes.local: settings.LocalSettings,
}


@lru_cache
def get_settings() -> settings.BaseAppSettings:
    app_env = settings.BaseAppSettings().environment
    return environments[app_env]()


settings = get_settings()
