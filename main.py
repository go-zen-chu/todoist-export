#!/usr/bin/env python3
import argparse
import os
from todoist_export import TodoistAPIClient, TodoistExport
from datetime import date, datetime, timedelta


def date_validation(date_str):
    try:
        return date.fromisoformat(date_str)
    except ValueError as e:
        raise argparse.ArgumentTypeError("{}: Date must be in ISO format. e.g. 2020-01-01".format(e))


if __name__ == '__main__':
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    parser = argparse.ArgumentParser(description='export todoist data with certain format')
    parser.add_argument('--api-token',
                        default=os.environ.get('TODOIST_API_TOKEN'))
    parser.add_argument('--from-date',
                        type=date_validation,
                        default=yesterday.strftime("%Y-%m-%d"),
                        help="From date where you retrieve data. Must be ISO format (YYYY-MM-DD)")
    parser.add_argument('--until-date',
                        type=date_validation,
                        default=now.strftime("%Y-%m-%d"),
                        help="Until date where you retrieve data. Must be ISO format (YYYY-MM-DD)")
    args = parser.parse_args()
    cli = TodoistAPIClient(args.api_token)
    exp = TodoistExport(cli)
    res = exp.export(from_dt=args.from_date, to_dt=args.until_date)
    print(res)
