import datetime
from datetime import timezone


def get_completed_items_side_effect(since, until, limit):
    d = {
        "2020-11-10T10:02": {
            "items": [
                {
                    "completed_date": "2020-11-13T15:32:51Z",
                    "content": "test0",
                    "id": 1012059080,
                    "meta_data": None,
                    "project_id": 2000000000,
                    "task_id": 5000885110,
                    "user_id": 10000000,
                },
                {
                    "completed_date": "2020-11-10T10:44:15Z",
                    "content": "test1",
                    "id": 1012059081,
                    "meta_data": None,
                    "project_id": 2000000000,
                    "task_id": 5000885111,
                    "user_id": 10000000,
                },
                {
                    "completed_date": "2020-11-12T10:43:40Z",
                    "content": "test2",
                    "id": 1012059082,
                    "meta_data": None,
                    "project_id": 2000000001,
                    "task_id": 5000885112,
                    "user_id": 10000000,
                },
            ],
            "projects": {
                "2000000000": {
                    "child_order": 2,
                    "collapsed": 0,
                    "color": 35,
                    "id": 2000000000,
                    "is_archived": 0,
                    "is_deleted": 0,
                    "is_favorite": 0,
                    "name": "tasks",
                    "parent_id": None,
                    "shared": False,
                    "sync_id": None,
                },
                "2000000001": {
                    "child_order": 2,
                    "collapsed": 0,
                    "color": 35,
                    "id": 2000000001,
                    "is_archived": 0,
                    "is_deleted": 0,
                    "is_favorite": 0,
                    "name": "tasks",
                    "parent_id": None,
                    "shared": False,
                    "sync_id": None,
                },
            },
        },
        "2020-11-17T10:02": {
            "items": [
                {
                    "completed_date": "2020-11-18T11:32:51Z",
                    "content": "test3",
                    "id": 1012059083,
                    "meta_data": None,
                    "project_id": 2000000000,
                    "task_id": 5000885113,
                    "user_id": 10000000,
                },
            ],
            "projects": {
                "2000000000": {
                    "child_order": 2,
                    "collapsed": 0,
                    "color": 35,
                    "id": 2000000000,
                    "is_archived": 0,
                    "is_deleted": 0,
                    "is_favorite": 0,
                    "name": "tasks",
                    "parent_id": None,
                    "shared": False,
                    "sync_id": None,
                }
            },
        },
        "2020-11-24T10:02": {},
        "2020-12-01T10:02": {},
        "2020-12-08T10:02": {},
        "2020-12-15T10:02": {},
        "2020-12-22T10:02": {},
        "2020-12-29T10:02": {},
        "2021-01-05T10:02": {
            "items": [
                {
                    "completed_date": "2021-01-11T11:32:51Z",
                    "content": "test4",
                    "id": 1012059084,
                    "meta_data": None,
                    "project_id": 2000000000,
                    "task_id": 5000885114,
                    "user_id": 10000000,
                },
            ],
            "projects": {
                "2000000000": {
                    "child_order": 2,
                    "collapsed": 0,
                    "color": 35,
                    "id": 2000000000,
                    "is_archived": 0,
                    "is_deleted": 0,
                    "is_favorite": 0,
                    "name": "tasks",
                    "parent_id": None,
                    "shared": False,
                    "sync_id": None,
                }
            },
        },
    }
    return d[since]


def get_item_info_side_effect(task_id):
    d = {
        5000885110: {
            "added_by_uid": 10000000,
            "assigned_by_uid": None,
            "checked": 1,
            "child_order": 10,
            "collapsed": 0,
            "content": "test0",
            "date_added": "2020-11-10T01:12:12Z",
            "date_completed": "2020-11-13T15:32:51Z",
            "due": {
                "date": "2020-11-10T11:32:00Z",
                "is_recurring": False,
                "lang": "en",
                "string": "2020-11-10 20:32",
                "timezone": "Asia/Tokyo",
            },
            "id": 5000885110,
            "in_history": 1,
            "is_deleted": 0,
            "labels": [],
            "parent_id": None,
            "priority": 1,
            "project_id": 2000000000,
            "responsible_uid": None,
            "section_id": None,
            "sync_id": None,
            "user_id": 10000000,
        },
        5000885111: {
            "added_by_uid": 10000000,
            "assigned_by_uid": None,
            "checked": 1,
            "child_order": 10,
            "collapsed": 0,
            "content": "test1",
            "date_added": "2020-11-10T10:42:15",
            "date_completed": "2020-11-10T10:44:15",
            "id": 5000885110,
            "in_history": 1,
            "is_deleted": 0,
            "labels": [],
            "parent_id": None,
            "priority": 1,
            "project_id": 2000000000,
            "responsible_uid": None,
            "section_id": None,
            "sync_id": None,
            "user_id": 10000000,
        },
        5000885112: {
            "added_by_uid": 10000000,
            "assigned_by_uid": None,
            "checked": 1,
            "child_order": 10,
            "collapsed": 0,
            "content": "test2",
            "date_added": "2020-11-10T10:43:40Z",
            "date_completed": "2020-11-12T10:43:40Z",
            "due": {
                "date": "2021-05-10T11:32:00Z",
                "is_recurring": True,
                "lang": "en",
                "string": "2020-05-10 20:32",
                "timezone": "Asia/Tokyo",
            },
            "id": 5000885112,
            "in_history": 1,
            "is_deleted": 0,
            "labels": [],
            "parent_id": None,
            "priority": 1,
            "project_id": 2000000001,
            "responsible_uid": None,
            "section_id": None,
            "sync_id": None,
            "user_id": 10000000,
        },
        5000885113: {
            "added_by_uid": 10000000,
            "assigned_by_uid": None,
            "checked": 1,
            "child_order": 10,
            "collapsed": 0,
            "content": "test3",
            "date_added": "2020-11-01T11:32:51Z",
            "date_completed": "2020-11-18T11:32:51Z",
            "due": {
                "date": "2020-11-18T20:32:51Z",
                "is_recurring": False,
                "lang": "en",
                "string": "2020-11-19 5:32",
                "timezone": "Asia/Tokyo",
            },
            "id": 5000885113,
            "in_history": 1,
            "is_deleted": 0,
            "labels": [],
            "parent_id": None,
            "priority": 1,
            "project_id": 2000000000,
            "responsible_uid": None,
            "section_id": None,
            "sync_id": None,
            "user_id": 10000000,
        },
        5000885114: {
            "added_by_uid": 10000000,
            "assigned_by_uid": None,
            "checked": 1,
            "child_order": 10,
            "collapsed": 0,
            "content": "test4",
            "date_added": "2021-01-01T11:32:51Z",
            "date_completed": "2021-01-11T11:32:51Z",
            "due": {
                "date": "2021-01-09T11:32:51",
                "is_recurring": False,
                "lang": "en",
                "string": "2021-01-09 11:32",
                "timezone": None,
            },
            "id": 5000885114,
            "in_history": 1,
            "is_deleted": 0,
            "labels": [],
            "parent_id": None,
            "priority": 1,
            "project_id": 2000000000,
            "responsible_uid": None,
            "section_id": None,
            "sync_id": None,
            "user_id": 10000000,
        },
    }
    return d[task_id]


completed_items = [
    {
        "content": "test0",
        "project_id": 2000000000,
        "project_name": "pj111",
        "completed_date": datetime.datetime(
            2020, 11, 10, 1, 12, 12, tzinfo=timezone.utc
        ),
        "due": {
            "date": datetime.datetime(2020, 11, 10, 11, 32, 00, tzinfo=timezone.utc),
            "is_recurring": False,
        },
    },
    {
        "content": "test1",
        "project_id": 2000000000,
        "project_name": "pj111",
        "completed_date": datetime.datetime(
            2020, 11, 10, 10, 44, 15, tzinfo=timezone.utc
        ),
        "due": {
            "date": None,
            "is_recurring": False,
        },
    },
    {
        "content": "test2",
        "project_id": 2000000001,
        "project_name": "pj222",
        "completed_date": datetime.datetime(
            2020, 11, 12, 10, 43, 40, tzinfo=timezone.utc
        ),
        "due": {
            "date": datetime.datetime(2021, 5, 10, 11, 32, 00, tzinfo=timezone.utc),
            "is_recurring": True,
        },
    },
    {
        "content": "test3",
        "project_id": 2000000000,
        "project_name": "pj111",
        "completed_date": datetime.datetime(
            2020, 11, 18, 11, 32, 51, tzinfo=timezone.utc
        ),
        "due": {
            "date": datetime.datetime(2020, 11, 18, 20, 32, 51, tzinfo=timezone.utc),
            "is_recurring": False,
        },
    },
    {
        "content": "test4",
        "project_id": 2000000000,
        "project_name": "pj111",
        "completed_date": datetime.datetime(
            2021, 1, 11, 11, 32, 51, tzinfo=timezone.utc
        ),
        "due": {
            "date": datetime.datetime(2021, 1, 9, 11, 32, 51, tzinfo=timezone.utc),
            "is_recurring": False,
        },
    },
]

daily_report_str = """'2020-11-10':
  pj111:
  - date: 2020-11-10T11:32:00+0000
    name: test0
  - date: 2020-11-10T10:44:15+0000
    name: test1
'2020-11-12':
  pj222:
  - date: 2020-11-12T10:43:40+0000
    name: test2
'2020-11-18':
  pj111:
  - date: 2020-11-18T20:32:51+0000
    name: test3
'2021-01-09':
  pj111:
  - date: 2021-01-09T11:32:51+0000
    name: test4
"""

daily_report_str_pj111 = """'2020-11-10':
  pj111:
  - date: 2020-11-10T11:32:00+0000
    name: test0
  - date: 2020-11-10T10:44:15+0000
    name: test1
'2020-11-18':
  pj111:
  - date: 2020-11-18T20:32:51+0000
    name: test3
'2021-01-09':
  pj111:
  - date: 2021-01-09T11:32:51+0000
    name: test4
"""
