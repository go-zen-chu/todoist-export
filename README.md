# todoist-export

[![Actions Status](https://github.com/go-zen-chu/todoist-export/workflows/ci/badge.svg)](https://github.com/go-zen-chu/todoist-export/actions)
[![GitHub issues](https://img.shields.io/github/issues/go-zen-chu/todoist-export.svg)](https://github.com/go-zen-chu/todoist-export/issues)

Export todoist data via api

## usage

### export daily report

Export daily report getting completed activities from todoist API.

```bash
# default export format is yaml
$ python3 main.py --data daily-report --from-date 2021-01-05 --until-date 2021-01-09
'2021-01-05':
  my-pj:
  - datetime: '2021-01-05T10:51:24Z'
    name: task1
  - datetime: '2021-01-05T09:14:00Z'
    name: task2
  - datetime: '2021-01-05T06:47:10Z'
    name: task3
'2021-01-06':
  my-pj:
  - datetime: '2021-01-06T9:51:24Z'
    name: task5
  my-pj2:
  - datetime: '2021-01-06T11:51:24Z'
    name: task4

# get repory with text format
$ python3 main.py --data daily-report --from-date 2021-01-05 --until-date 2021-01-09 --format txt
2020-11-10
pj111:
- test0
- test1

2020-11-12
pj222:
- test2

2020-11-18
pj111:
- test3

2021-01-09
pj111:
- test4
```

## dev

pytest runs with GitHub Actions. Make sure impl test and it passes.
