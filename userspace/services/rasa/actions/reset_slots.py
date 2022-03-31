from rasa_sdk import Action
from rasa_sdk.events import SlotSet


class ResetToGrab(Action):

    def name(self):
        return "action_reset_to_grab"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("to_grab", None)]
