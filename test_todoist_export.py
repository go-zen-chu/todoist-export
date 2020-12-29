from todoist_export import TodoistAPIClient, TodoistExport
from unittest import mock
from datetime import datetime, timedelta


def test_TodoistAPIClient___init__():
    cli = TodoistAPIClient("todoist_token")
    assert cli is not None


def test_TodoistExport___init__():
    cli = TodoistAPIClient("todoist_token")
    exp = TodoistExport(cli)
    assert exp is not None


def test_TodoistExport_export():
    mcli = mock.MagicMock(return_value="some return value")
    exp = TodoistExport(mcli)
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    assert exp.export(from_dt=yesterday, to_dt=now, format="yaml") == "TBD"
