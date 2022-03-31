from typing import Optional

from decouple import config

# Redis
REDIS_HOST: str = config("REDIS_HOST")
REDIS_PORT: int = config("REDIS_PORT", default=6379, cast=int)
REDIS_PASSWORD: Optional[str] = config("REDIS_PASSWORD", default=None)

# Rasa
RASA_REDIS_INPUT_CHANNEL: str = config("RASA_REDIS_INPUT_CHANNEL")
RASA_REDIS_OUTPUT_CHANNEL: str = config("RASA_REDIS_OUTPUT_CHANNEL")
RASA_SIO_SERVER_ADDR: str = config("RASA_SIO_SERVER_ADDR")
RASA_USER_MSG_EVT: str = config("RASA_USER_MSG_EVT", default="user_message")
RASA_BOT_MSG_EVT: str = config("RASA_BOT_MSG_EVT", default="bot_message")
RASA_SENDER_NAME: str = config("RASA_SENDER_NAME", default="alfred_user")
