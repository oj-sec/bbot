from .base import BaseOutputModule


class Human(BaseOutputModule):
    def handle_event(self, event):
        event_type = f"[{event.type}]"
        event_tags = ""
        if event.tags:
            event_tags = f'\t({", ".join(getattr(event, "tags", []))})'
        self.stdout(f"{event_type:<20}\t{event.data}{event_tags}")