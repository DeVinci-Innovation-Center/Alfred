from decouple import config


class Config:
    ALFRED_ADDRESS: str = config("ALFRED_ADDRESS")
    ALFRED_GRAB_ROUTE: str = config("ALFRED_GRAB_ROUTE")


cfg = Config()
