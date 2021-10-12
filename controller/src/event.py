"""
Events:
    - new_command_str: convert command to Command object before decomposing..
      Input: same as Command's __str__ method output.
    - new_command: decompose new command received and add it to queue to be executed.
      Input: Command object
"""

from typing import Any, Callable


_subscribers: dict = {}

def subscribe(event_type: str, fn: Callable) -> None:
    """Subscribe a function to an event."""

    if not event_type in _subscribers:
        _subscribers[event_type] = []

    _subscribers[event_type].append(fn)

def post_event(event_type: str, data: Any) -> None:
    """Trigger event: call functions subscribed to this event_type."""

    if not event_type in _subscribers:
        return

    for fn in _subscribers[event_type]:
        fn(data)
