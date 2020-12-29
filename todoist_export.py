import todoist
from datetime import datetime


class TodoistAPIClient:
    def __init__(self, token: str):
        self.token = token
        # auth Todoist API
        self.api = todoist.TodoistAPI(token)


class TodoistExport:
    def __init__(self, cli: TodoistAPIClient):
        self.cli = cli

    def export(self, from_dt: datetime, to_dt: datetime, format: str = "yaml") -> str:
        return "TBD"
        # activities = api.activity.get(object_type="item", event_type="completed", page=1)
        # pprint.pprint(activities)
