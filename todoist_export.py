import todoist
from datetime import datetime
from typing import List
import yaml


class TodoistAPIClient:
    def __init__(self, token: str):
        self.token = token
        # auth Todoist API
        self.api = todoist.TodoistAPI(token)

    def get_completed_activities(self, from_dt: datetime, until_dt: datetime) -> List:
        activities = []
        # params: https://developer.todoist.com/sync/v8/?shell#get-activity-logs
        # TODO: support more than 100 events
        # activities are ordered from latest
        data = self.api.activity.get(object_type="item", event_type="completed", limit=100)
        # check events are in range
        for ev in data['events']:
            ev_dt = datetime.strptime(ev["event_date"], "%Y-%m-%dT%H:%M:%SZ")
            if from_dt <= ev_dt and ev_dt <= until_dt:
                activities.append(ev)
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
