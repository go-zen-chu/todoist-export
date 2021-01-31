from todoist_export import TodoistAPIClient, TodoistExport
from unittest import mock
from datetime import datetime, timezone


now = datetime.now()


def test_TodoistAPIClient___init__():
    cli = TodoistAPIClient("todoist_token")
    assert cli is not None


def test_TodoistAPIClient_get_completed_activities():
    cli = TodoistAPIClient("todoist_token")
    m = mock.MagicMock(side_effect=get_activities_side_effect)
    cli.api.activity.get = m
    from_dt = datetime.strptime("2020-11-10T10:02:03Z", "%Y-%m-%dT%H:%M:%SZ")
    from_dt = from_dt.replace(tzinfo=timezone.utc)
    until_dt = datetime.strptime("2021-01-10T10:02:03Z", "%Y-%m-%dT%H:%M:%SZ")
    until_dt = until_dt.replace(tzinfo=timezone.utc)
    acts = cli.get_completed_activities(from_dt=from_dt, until_dt=until_dt)
    assert len(acts) == 3
    # TODO: check future date pattern


def test_TodoistExport___init__():
    cli = TodoistAPIClient("todoist_token")
    exp = TodoistExport(cli)
    assert exp is not None


def test_TodoistExport_export_daily_report():
    mcli = mock.MagicMock(spec=TodoistAPIClient)
    mcli.get_completed_activities = mock.MagicMock(return_value=activity_valid_data)
    mcli.get_project = mock.MagicMock(side_effect=get_project_side_effect)
    exp = TodoistExport(mcli)

    # test from, until
    from_dt = datetime.strptime("2020-11-10T10:02:03Z", "%Y-%m-%dT%H:%M:%SZ")
    from_dt = from_dt.replace(tzinfo=timezone.utc)
    until_dt = datetime.strptime("2021-01-10T10:02:03Z", "%Y-%m-%dT%H:%M:%SZ")
    until_dt = until_dt.replace(tzinfo=timezone.utc)
    assert (
        exp.export_daily_report(from_dt=from_dt, until_dt=until_dt) == daily_report_str
    )

    # test pj_filter
    filter1 = ".*"
    assert (
        exp.export_daily_report(from_dt=from_dt, until_dt=until_dt, pj_filter=filter1)
        == daily_report_str
    )
    filter2 = "pj1+"
    assert (
        exp.export_daily_report(from_dt=from_dt, until_dt=until_dt, pj_filter=filter2)
        == daily_report_str_pj111
    )
    filter3 = "xxxx"
    assert (
        exp.export_daily_report(from_dt=from_dt, until_dt=until_dt, pj_filter=filter3)
        == "{}\n"
    )


# raw structure from todoist api
activity_logs_valid_data = {
    "count": 3,
    "events": [
        {
            "event_date": "2020-12-27T02:30:40Z",
            "event_type": "completed",
            "extra_data": {"client": "Mozilla/5.0; Todoist/1063", "content": "test1"},
            "id": 10600000001,
            "initiator_id": None,
            "object_id": 4000000001,
            "object_type": "item",
            "parent_item_id": None,
            "parent_project_id": 2000000001,
        },
        {
            "event_date": "2020-12-27T01:30:40Z",
            "event_type": "completed",
            "extra_data": {"client": "Mozilla/5.0; Todoist/1063", "content": "test2"},
            "id": 10600000002,
            "initiator_id": None,
            "object_id": 4000000002,
            "object_type": "item",
            "parent_item_id": None,
            "parent_project_id": 2000000001,
        },
        {
            "event_date": "2020-12-25T01:30:40Z",
            "event_type": "completed",
            "extra_data": {"client": "Mozilla/5.0; Todoist/1063", "content": "test3"},
            "id": 10600000003,
            "initiator_id": None,
            "object_id": 4000000003,
            "object_type": "item",
            "parent_item_id": None,
            "parent_project_id": 3000000001,
        },
    ],
}

# activity event data
activity_valid_data = [
    {
        "event_date": "2020-12-27T02:30:40Z",
        "event_type": "completed",
        "extra_data": {"client": "Mozilla/5.0; Todoist/1063", "content": "test1"},
        "id": 10600000001,
        "initiator_id": None,
        "object_id": 4000000001,
        "object_type": "item",
        "parent_item_id": None,
        "parent_project_id": 2000000001,
    },
    {
        "event_date": "2020-12-27T01:30:40Z",
        "event_type": "completed",
        "extra_data": {"client": "Mozilla/5.0; Todoist/1063", "content": "test2"},
        "id": 10600000002,
        "initiator_id": None,
        "object_id": 4000000002,
        "object_type": "item",
        "parent_item_id": None,
        "parent_project_id": 2000000001,
    },
    {
        "event_date": "2020-12-25T01:30:40Z",
        "event_type": "completed",
        "extra_data": {"client": "Mozilla/5.0; Todoist/1063", "content": "test3"},
        "id": 10600000003,
        "initiator_id": None,
        "object_id": 4000000003,
        "object_type": "item",
        "parent_item_id": None,
        "parent_project_id": 3000000001,
    },
]

activity_valid_data_str = """- event_date: '2020-12-27T02:30:40Z'
  event_type: completed
  extra_data:
    client: Mozilla/5.0; Todoist/1063
    content: test1
  id: 10600000001
  initiator_id: null
  object_id: 4000000001
  object_type: item
  parent_item_id: null
  parent_project_id: 2000000001
- event_date: '2020-12-27T01:30:40Z'
  event_type: completed
  extra_data:
    client: Mozilla/5.0; Todoist/1063
    content: test2
  id: 10600000002
  initiator_id: null
  object_id: 4000000002
  object_type: item
  parent_item_id: null
  parent_project_id: 2000000001
- event_date: '2020-12-25T01:30:40Z'
  event_type: completed
  extra_data:
    client: Mozilla/5.0; Todoist/1063
    content: test3
  id: 10600000003
  initiator_id: null
  object_id: 4000000003
  object_type: item
  parent_item_id: null
  parent_project_id: 3000000001
"""

daily_report_str = """'2020-12-25':
  pj222:
  - datetime: '2020-12-25T01:30:40Z'
    name: test3
'2020-12-27':
  pj111:
  - datetime: '2020-12-27T02:30:40Z'
    name: test1
  - datetime: '2020-12-27T01:30:40Z'
    name: test2
"""

daily_report_str_pj111 = """'2020-12-27':
  pj111:
  - datetime: '2020-12-27T02:30:40Z'
    name: test1
  - datetime: '2020-12-27T01:30:40Z'
    name: test2
"""

# variable for singleton pattern
get_activities_side_effect_returned = False


def get_activities_side_effect(
    object_type="item", event_type="completed", page=0, limit=100
):
    global get_activities_side_effect_returned
    # TODO: proper impl for returning activity data
    if get_activities_side_effect_returned:
        return {"count": 0, "events": []}
    else:
        get_activities_side_effect_returned = True
        return activity_logs_valid_data


def get_project_side_effect(project_id):
    d = {
        "2000000001": {
            "child_order": 0,
            "collapsed": 0,
            "color": 1,
            "id": 2000000001,
            "is_archived": 0,
            "is_deleted": 0,
            "is_favorite": 0,
            "name": "pj111",
            "parent_id": None,
        },
        "3000000001": {
            "child_order": 0,
            "collapsed": 0,
            "color": 1,
            "id": 3000000001,
            "is_archived": 0,
            "is_deleted": 0,
            "is_favorite": 0,
            "name": "pj222",
            "parent_id": None,
        },
    }
    return d[str(project_id)]
