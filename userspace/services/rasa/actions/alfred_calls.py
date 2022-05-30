import logging
from typing import Any, Dict, List, Text

import requests
from rasa_sdk import Action, Tracker

from .config import cfg

logger = logging.getLogger("rasa")


class GrabItem(Action):
    def name(self):
        return "action_grab_item"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        to_grab = tracker.slots["to_grab"]

        data = {"grasping_target": to_grab}
        logging.debug("HTTP Request: POST %s, data: %s", (cfg.ALFRED_GRAB_ROUTE, data))

        _ = requests.post(f"{cfg.ALFRED_ADDRESS}/{cfg.ALFRED_GRAB_ROUTE}", data=data)

        return []
