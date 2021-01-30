import logging
from datetime import datetime, timezone
from typing import List

import todoist
import yaml
import re


class TodoistAPIClient:
    def __init__(self, token: str):
        self.token = token
        # auth Todoist API
        self.api = todoist.TodoistAPI(token)
        self.logger = logging.getLogger(__name__)
        self.cache = {}

    def get_completed_activities(self, from_dt: datetime, until_dt: datetime) -> List:
        activities = []
        # params: https://developer.todoist.com/sync/v8/?shell#get-activity-logs
        # TODO: support more than 100 events
        # activities are ordered from latest
        data = self.api.activity.get(
            object_type="item", event_type="completed", limit=100
        )
        if "error" in data:
            self.logger.error(
                "todoist api returned error: {}".format(data["error_tag"])
            )
        else:
            # check events are in range
            for ev in data["events"]:
                ev_dt = datetime.strptime(ev["event_date"], "%Y-%m-%dT%H:%M:%SZ")
                # set naive datetime to tz aware (todoist api returns UTC time)
                ev_dt = ev_dt.replace(tzinfo=timezone.utc)
                if from_dt <= ev_dt and ev_dt <= until_dt:
                    activities.append(ev)
        return activities

    def get_project(self, project_id: int):
        if "projects" not in self.cache:
            self.cache["projects"] = {}
        if project_id in self.cache["projects"]:
            return self.cache["projects"][project_id]
        else:
            # https://developer.todoist.com/sync/v8/?shell#get-project-info
            pj = self.api.projects.get(project_id=project_id)
            self.cache["projects"][project_id] = pj["project"]
            return pj["project"]


class TodoistExport:
    def __init__(self, cli: TodoistAPIClient):
        self.cli = cli
        self.logger = logging.getLogger(__name__)

    def export_daily_report(
        self,
        from_dt: datetime,
        until_dt: datetime,
        pj_filter: str = ".*",
        tz: timezone = timezone.utc,
        format: str = "yaml",
    ) -> str:
        """export daily report in string

        Args:
            from_dt (datetime): from datetime
            until_dt (datetime): until datetime
            tz (timezone, optional): timezone for adjustment. Defaults to timezone.utc.
            format (str, optional): string format. Defaults to 'yaml'.

        Raises:
            ValueError: error when unsupported format specified

        Returns:
            str: daily report string
        """
        pj_prog = re.compile(pj_filter)
        acts = self.cli.get_completed_activities(from_dt=from_dt, until_dt=until_dt)
        # report structure:
        # { date: {project: [events]}}
        report = {}
        for act in acts:
            # filter pj
            pj = self.cli.get_project(act["parent_project_id"])
            pj_name = pj["name"]
            if pj_prog.match(pj_name) is None:
                self.logger.info("project not matched: {}".format(pj_name))
                continue
            dt = datetime.strptime(act["event_date"], "%Y-%m-%dT%H:%M:%SZ")
            utc_dt = dt.replace(tzinfo=timezone.utc)
            # change UTC time to specified timezone for export
            tz_dt = utc_dt.astimezone(tz=tz)
            date_str = tz_dt.strftime("%Y-%m-%d")
            if date_str not in report:
                report[date_str] = {}
            if pj_name not in report[date_str]:
                report[date_str][pj_name] = []
            report[date_str][pj_name].append(
                {"datetime": act["event_date"], "name": act["extra_data"]["content"]}
            )
        if format == "yaml":
            # allow_unicode True for printing utf-8 strings
            return yaml.dump(report, sort_keys=True, allow_unicode=True)
        else:
            raise ValueError("unsupported format: {}".format(format))
