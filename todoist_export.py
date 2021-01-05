import todoist
from datetime import datetime, date
import pprint
from typing import List


class TodoistAPIClient:
    def __init__(self, token: str):
        self.token = token
        # auth Todoist API
        self.api = todoist.TodoistAPI(token)

    def get_completed_activities(self, from_dt: datetime, to_dt: datetime) -> List:
        activities = []
        # params: https://developer.todoist.com/sync/v8/?shell#get-activity-logs
        events = self.api.activity.get(object_type="item", event_type="completed", limit=100)
        # check events are in datetime
        for ev in events['events']:
            ev_dt = datetime.strftime(ev.'%Y-%m-%dT%H:%M:%SZ')
        return activities


class TodoistExport:
    def __init__(self, cli: TodoistAPIClient):
        self.cli = cli

    def export(self, from_dt: datetime, to_dt: datetime, format: str = "yaml") -> str:
        acts = self.cli.get_completed_activities()
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(acts)
        return "TBD"
