from typing import List, Optional, Union

from decouple import config


def _split_comma(x: str):
    return x.split(",")


def _int_or_str_or_none(x: Optional[str]):
    if x is None:
        return None

    return int(x) if x.isnumeric() else x


# Redis
REDIS_HOST: str = config("REDIS_HOST")
REDIS_PORT: int = config("REDIS_PORT", default=6379, cast=int)
REDIS_PASSWORD: Optional[str] = config("REDIS_PASSWORD", default=None)

# azure speech key
AZURE_KEY: str = config("AZURE_KEY")
# azure speech region
AZURE_REGION: str = config("AZURE_REGION")
# comma-separated list of languages
AZURE_LANG: List[str] = config("AZURE_LANG", cast=_split_comma)
# device id or name for microphone. see `python -m sounddevice`
MICROPHONE_ID: Optional[Union[str, int]] = config(
    "MICROPHONE_ID", default=None, cast=_int_or_str_or_none
)
