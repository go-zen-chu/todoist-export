# todoist-export

Export todoist data via api

## usage

### export daily report

```bash
$ python3 main.py --data daily-report --from-date 2021-01-05 --until-date 2021-01-09
'2021-01-05':
  my-pj:
  - datetime: '2021-01-05T10:51:24Z'
    name: task1
  - datetime: '2021-01-05T09:14:00Z'
    name: task2
  - datetime: '2021-01-05T06:47:10Z'
    name: task3
```

## dev

pytest runs with GitHub Actions. Make sure impl test and it passes.
