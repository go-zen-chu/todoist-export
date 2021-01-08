import todoist
from datetime import datetime, date
import pprint
from typing import List
import yaml


class TodoistAPIClient:
    def __init__(self, token: str):
        self.token = token
        # auth Todoist API
        self.api = todoist.TodoistAPI(token)

    def get_completed_activities(self, from_dt: datetime, until_dt: datetime) -> List:
        activities = []
        # activities are ordered from latest
        
        # params: https://developer.todoist.com/sync/v8/?shell#get-activity-logs
        events = self.api.activity.get(object_type="item", event_type="completed", limit=100)
        # check events are in range
        for ev in events['events']:
            ev_dt = datetime.strftime(ev.'%Y-%m-%dT%H:%M:%SZ')
        return activities


class TodoistExport:
    def __init__(self, cli: TodoistAPIClient):
        self.cli = cli

    def export(self, from_dt: datetime, until_dt: datetime, format: str = "yaml") -> str:
        acts = self.cli.get_completed_activities(from_dt=from_dt, until_dt=until_dt)
        if format in ("yml", "yaml"):
            return yaml.dump(acts)
        else:
            raise ValueError("unsupported format: {}".format(format))
