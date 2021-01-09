from todoist_export import TodoistAPIClient, TodoistExport
from unittest import mock
from datetime import datetime


def test_TodoistAPIClient___init__():
    cli = TodoistAPIClient('todoist_token')
    assert cli is not None


def test_TodoistAPIClient_get_completed_activities():
    cli = TodoistAPIClient('todoist_token')
    m = mock.MagicMock(return_value=activity_logs_valid_data)
    cli.api.activity.get = m
    from_dt = datetime.strptime('2020-11-10T10:02:03Z', '%Y-%m-%dT%H:%M:%SZ')
    until_dt = datetime.strptime('2021-01-10T10:02:03Z', '%Y-%m-%dT%H:%M:%SZ')
    acts = cli.get_completed_activities(from_dt=from_dt, until_dt=until_dt)
    assert len(acts) == 3


def test_TodoistExport___init__():
    cli = TodoistAPIClient('todoist_token')
    exp = TodoistExport(cli)
    assert exp is not None


def test_TodoistExport_export():
    mcli = mock.MagicMock(spec=TodoistAPIClient)
    mcli.get_completed_activities = mock.MagicMock(return_value=activity_valid_data)
    exp = TodoistExport(mcli)
    from_dt = datetime.strptime('2020-11-10T10:02:03Z', '%Y-%m-%dT%H:%M:%SZ')
    until_dt = datetime.strptime('2021-01-10T10:02:03Z', '%Y-%m-%dT%H:%M:%SZ')
    assert exp.export(from_dt=from_dt, until_dt=until_dt) == activity_valid_data_str



# raw structure from todoist api
activity_logs_valid_data = {
    'count': 3,
    'events': [
        {
            'event_date': '2020-12-27T02:30:40Z',
            'event_type': 'completed',
            'extra_data': {
                'client': 'Mozilla/5.0; Todoist/1063',
                'content': 'test1'
            },
            'id': 10600000001,
            'initiator_id': None,
            'object_id': 4000000001,
            'object_type': 'item',
            'parent_item_id': None,
            'parent_project_id': 2000000001
        },
        {
            'event_date': '2020-12-27T01:30:40Z',
            'event_type': 'completed',
            'extra_data': {
                'client': 'Mozilla/5.0; Todoist/1063',
                'content': 'test2'
            },
            'id': 10600000002,
            'initiator_id': None,
            'object_id': 4000000002,
            'object_type': 'item',
            'parent_item_id': None,
            'parent_project_id': 2000000001
        },
        {
            'event_date': '2020-12-25T01:30:40Z',
            'event_type': 'completed',
            'extra_data': {
                'client': 'Mozilla/5.0; Todoist/1063',
                'content': 'test3'
            },
            'id': 10600000003,
            'initiator_id': None,
            'object_id': 4000000003,
            'object_type': 'item',
            'parent_item_id': None,
            'parent_project_id': 3000000001
        }
    ]
}

# activity event data
activity_valid_data = [
    {
        'event_date': '2020-12-27T02:30:40Z',
        'event_type': 'completed',
        'extra_data': {
            'client': 'Mozilla/5.0; Todoist/1063',
            'content': 'test1'
        },
        'id': 10600000001,
        'initiator_id': None,
        'object_id': 4000000001,
        'object_type': 'item',
        'parent_item_id': None,
        'parent_project_id': 2000000001
    },
    {
        'event_date': '2020-12-27T01:30:40Z',
        'event_type': 'completed',
        'extra_data': {
            'client': 'Mozilla/5.0; Todoist/1063',
            'content': 'test2'
        },
        'id': 10600000002,
        'initiator_id': None,
        'object_id': 4000000002,
        'object_type': 'item',
        'parent_item_id': None,
        'parent_project_id': 2000000001
    },
    {
        'event_date': '2020-12-25T01:30:40Z',
        'event_type': 'completed',
        'extra_data': {
            'client': 'Mozilla/5.0; Todoist/1063',
            'content': 'test3'
        },
        'id': 10600000003,
        'initiator_id': None,
        'object_id': 4000000003,
        'object_type': 'item',
        'parent_item_id': None,
        'parent_project_id': 3000000001
    }
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