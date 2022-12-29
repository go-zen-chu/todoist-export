from todoist_export import TodoistAPIClient, TodoistExport
from unittest import mock
from datetime import datetime, timezone
import testdata


def test_TodoistAPIClient___init__():
    cli = TodoistAPIClient(token="todoist_token")
    assert cli is not None


def test_TodoistAPIClient_get_item_info():
    item_id = "1012059080"
    cli = TodoistAPIClient(token="todoist_token")
    # TIPS: __get method is private so following mock doesn't work
    # cli.__get = mock.MagicMock(side_effect=testdata.get_side_effect)
    with mock.patch.object(
        target=cli, attribute="_TodoistAPIClient__get", new=testdata.get_side_effect
    ):
        acts = cli.get_item_info(item_id=item_id)
        assert acts["content"] == "test0"


def test_TodoistAPIClient_get_completed_items():
    from_dt = datetime.strptime("2020-11-10T10:02:03Z", "%Y-%m-%dT%H:%M:%SZ")
    from_dt = from_dt.replace(tzinfo=timezone.utc)
    until_dt = datetime.strptime("2021-01-10T10:02:03Z", "%Y-%m-%dT%H:%M:%SZ")
    until_dt = until_dt.replace(tzinfo=timezone.utc)
    cli = TodoistAPIClient(token="todoist_token")
    cli.get_item_info = mock.MagicMock(side_effect=testdata.get_item_info_side_effect)
    with mock.patch.object(
        target=cli, attribute="_TodoistAPIClient__get", new=testdata.get_side_effect
    ):
        acts = cli.get_completed_items(from_dt=from_dt, until_dt=until_dt)
        assert len(acts) == 5

    # test with irregular data
    from_dt = datetime.strptime("2020-11-10T10:02:03Z", "%Y-%m-%dT%H:%M:%SZ")
    from_dt = from_dt.replace(tzinfo=timezone.utc)
    until_dt = datetime.strptime("2021-01-10T10:02:03Z", "%Y-%m-%dT%H:%M:%SZ")
    until_dt = until_dt.replace(tzinfo=timezone.utc)
    cli.get_item_info = mock.MagicMock(
        side_effect=testdata.get_irregular_item_info_side_effect
    )
    with mock.patch.object(
        target=cli, attribute="_TodoistAPIClient__get", new=testdata.get_side_effect
    ):
        acts = cli.get_completed_items(from_dt=from_dt, until_dt=until_dt)
        assert len(acts) == 5


def test_TodoistExport___init__():
    cli = TodoistAPIClient(token="todoist_token")
    exp = TodoistExport(cli)
    assert exp is not None


def test_TodoistExport_export_daily_report():
    mcli = mock.MagicMock(spec=TodoistAPIClient)
    mcli.get_completed_items = mock.MagicMock(return_value=testdata.completed_items)
    exp = TodoistExport(cli=mcli)

    # test from, until
    from_dt = datetime.strptime("2020-11-10T10:02:03Z", "%Y-%m-%dT%H:%M:%SZ")
    from_dt = from_dt.replace(tzinfo=timezone.utc)
    until_dt = datetime.strptime("2021-01-10T10:02:03Z", "%Y-%m-%dT%H:%M:%SZ")
    until_dt = until_dt.replace(tzinfo=timezone.utc)
    assert (
        exp.export_daily_report(from_dt=from_dt, until_dt=until_dt)
        == testdata.daily_report_str_yaml
    )

    # test pj_filter
    filter1 = ".*"
    assert (
        exp.export_daily_report(from_dt=from_dt, until_dt=until_dt, pj_filter=filter1)
        == testdata.daily_report_str_yaml
    )
    filter2 = "pj1+"
    assert (
        exp.export_daily_report(from_dt=from_dt, until_dt=until_dt, pj_filter=filter2)
        == testdata.daily_report_str_pj111
    )
    filter3 = "xxxx"
    assert (
        exp.export_daily_report(from_dt=from_dt, until_dt=until_dt, pj_filter=filter3)
        == "{}\n"
    )

    # test export format
    assert (
        exp.export_daily_report(from_dt=from_dt, until_dt=until_dt, format="txt")
        == testdata.daily_report_str_txt
    )
