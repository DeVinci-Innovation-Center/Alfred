from typing import Any, Dict, List, Text

import requests
from rasa_sdk import Action, Tracker

from .config import cfg


class GrabItem(Action):
    def name(self):
        return "action_grab_item"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        to_grab = tracker.slots["to_grab"]

        req = requests.post(
            f"{cfg.ALFRED_ADDRESS}/{cfg.ALFRED_GRAB_ROUTE}",
            data={"to_grab": to_grab},
        )

        return []
