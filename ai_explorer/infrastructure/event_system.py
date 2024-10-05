from typing import Any, Dict, List


class EventSystem:
    def __init__(self):
        self.subscribers: Dict[str, List[callable]] = {}

    def subscribe(self, event: str, callback: callable) -> None:
        if event not in self.subscribers:
            self.subscribers[event] = []
        self.subscribers[event].append(callback)

    def publish(self, event: str, data: Any) -> None:
        if event in self.subscribers:
            for callback in self.subscribers[event]:
                callback(data)


event_system = EventSystem()
