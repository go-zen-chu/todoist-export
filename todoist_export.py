from logging import getLogger
import logging
from datetime import datetime, timezone, timedelta
import os
from typing import List

import requests
import yaml
import re

# https://developer.todoist.com/sync/v9/#overview
api_endpoint = "https://api.todoist.com/sync/v9/"


class TodoistAPIClient:
    def __init__(self, token: str, log_level=logging.WARN):
        self.logger = getLogger(__name__)
        self.logger.setLevel(log_level)
        self.cache = {}
        self.token = token
        self.session = requests.Session()
        self.auth(token=token)

    def auth(self, token: str):
        headers = {"Authorization": "Bearer {}".format(token)}
        params = {
            "sync_token": "*",
            "resource_types": '["all"]',
        }
        r = self.session.get(
            os.path.join(api_endpoint, "sync"), headers=headers, params=params
        )
        if r.status_code != 200:
            raise RuntimeError(
                "failed to auth todoist API: status code {}, text {}".format(
                    r.status_code, r.text
                )
            )
        # https://developer.todoist.com/sync/v9/#read-resources
        self.resources = r.json()

    def get_item_info(self, item_id: int):
        if "items" not in self.cache:
            self.cache["items"] = {}
        if item_id in self.cache["items"]:
            return self.cache["items"][item_id]
        else:
            # https://developer.todoist.com/sync/v9/#update-day-orders
            item = self.session.get(
                os.path.join(api_endpoint, "items/get", params={"item_id": item_id})
            ).json()
            if item is None:
                self.logger.warning(
                    "Could not find item by id {}. May be repeated task deleted.".format(
                        item_id
                    )
                )
                return None
            else:
                # return only item info
                return item["item"]

    def get_completed_items(self, from_dt: datetime, until_dt: datetime) -> List:
        """get completed items from todoist api

        Args:
            from_dt (datetime): from datetime (timezone aware)
            until_dt (datetime): until datetime (timezone aware)

        Returns:
            List: list of completed items
        """
        compl_items = []
        tz = from_dt.tzinfo
        # split from - until by 1 week
        tmp_from_dt = from_dt
        tmp_until_dt = from_dt + timedelta(days=7)
        while tmp_from_dt < until_dt:
            # set until to actual until_dt
            if tmp_until_dt > until_dt:
                tmp_until_dt = until_dt
            self.logger.info(
                "get completed items from week before {} to {}".format(
                    tmp_from_dt, tmp_until_dt
                )
            )
            # convert to utc for todoist api
            since_utc_str = tmp_from_dt.astimezone(tz=timezone.utc).strftime(
                "%Y-%m-%dT%H:%M"
            )
            until_utc_str = tmp_until_dt.astimezone(tz=timezone.utc).strftime(
                "%Y-%m-%dT%H:%M"
            )
            # get completed items during specified range
            # https://developer.todoist.com/sync/v9/#get-all-completed-items
            data = self.session.get(
                os.join(api_endpoint, "completed/get_all"),
                params={"since": since_utc_str, "until": until_utc_str, "limit": 100},
            )
            if "error" in data:
                self.logger.critical(
                    "todoist api returned error: {}".format(data["error_tag"])
                )
            elif "items" not in data:
                self.logger.info("no items")
            else:
                # get project dict
                pjs = data["projects"]
                for item in data["items"]:
                    pj = pjs[str(item["project_id"])]
                    # get due date if exists
                    item_info = self.get_item_info(item["task_id"])
                    if item_info is None:
                        self.logger.info("could not get item. skipping")
                    else:
                        due_date = None
                        due_is_recurring = False
                        if "due" in item_info:
                            due_is_recurring = item_info["due"]["is_recurring"]
                            if item_info["due"]["timezone"] is not None:
                                due_date = datetime.strptime(
                                    item_info["due"]["date"], "%Y-%m-%dT%H:%M:%SZ"
                                )
                                due_date.astimezone(tz=timezone.utc)
                            else:
                                # TIPS: there are some case that timezone of due date is not set (repeated task).
                                # In that case, timezone is uncertain (omg).
                                due_date = datetime.strptime(
                                    item_info["due"]["date"], "%Y-%m-%dT%H:%M:%S"
                                )
                                due_date.astimezone(tz=tz)
                    compl_date = datetime.strptime(
                        item["completed_date"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                    compl_date.astimezone(tz=timezone.utc)
                    # get due datetime if exists
                    compl_items.append(
                        {
                            "content": item["content"],
                            "project_id": item["project_id"],
                            "project_name": pj["name"],
                            "completed_date": compl_date,
                            "due": {"date": due_date, "is_recurring": due_is_recurring},
                        }
                    )
            # increment to next range
            tmp_from_dt += timedelta(days=7)
            tmp_until_dt = tmp_from_dt + timedelta(days=7)
        return compl_items


class TodoistExport:
    def __init__(self, cli: TodoistAPIClient, log_level=logging.WARN):
        self.cli = cli
        self.logger = getLogger(__name__)
        self.logger.setLevel(log_level)

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
        items = self.cli.get_completed_items(from_dt=from_dt, until_dt=until_dt)
        # report structure:
        # { date: {project: [events]}}
        report = {}
        for item in items:
            # filter pj
            pj_name = item["project_name"]
            if pj_prog.match(pj_name) is None:
                self.logger.info("project not matched: {}".format(pj_name))
                continue
            compl_date = item["completed_date"]
            if item["due"]["date"] is not None:
                if item["due"]["is_recurring"]:
                    # if recurring case, due date would be future. so use completed_date
                    compl_date = item["completed_date"]
                else:
                    # if there is due date, then use it as completed time
                    # for those who forgot to complete item by the time
                    compl_date = item["due"]["date"]
            # change UTC time to specified timezone for export
            compl_date.astimezone(tz=tz)
            date_str = compl_date.strftime("%Y-%m-%d")
            if date_str not in report:
                report[date_str] = {}
            if pj_name not in report[date_str]:
                report[date_str][pj_name] = []
            report[date_str][pj_name].append(
                {
                    "date": compl_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "name": item["content"],
                }
            )
        if format == "yaml":
            # allow_unicode True for printing utf-8 strings
            return yaml.dump(report, sort_keys=True, allow_unicode=True)
        elif format == "txt":
            # sort report dict by key(date_str)
            report_sorted = sorted(report.items(), key=lambda x: x[0])
            report_lines = []
            for tpl in report_sorted:
                report_lines.append(tpl[0])
                for pj in tpl[1]:
                    report_lines.append(pj + ":")
                    for it in tpl[1][pj]:
                        report_lines.append("- " + it["name"])
                report_lines.append("")
            return "\n".join(report_lines)
        else:
            raise ValueError("unsupported format: {}".format(format))
