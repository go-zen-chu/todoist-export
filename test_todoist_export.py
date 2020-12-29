from todoist_export import TodoistAPIClient, TodoistExport


def test_TodoistAPIClient___init__():
    cli = TodoistAPIClient("todoist_token")
    assert cli is not None


def test_TodoistExport___init__():
    cli = TodoistAPIClient("todoist_token")
    exp = TodoistExport(cli)
    assert exp is not None
