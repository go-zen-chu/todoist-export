#!/usr/bin/env python3
import argparse
import os
from todoist_export import TodoistAPIClient, TodoistExport
from datetime import datetime, timedelta
import tzlocal


def date_validation(date_str: str):
    """validate date string and parse with local timezone

    Args:
        date_str (str): date string

    Raises:
        argparse.ArgumentTypeError: could not parse date string

    Returns:
        datetime: datetime object with local timezone
    """
    try:
        # support local timezone
        tz = tzlocal.get_localzone()
        naive_dt = datetime.strptime(date_str, '%Y-%m-%d')
        dt = naive_dt.astimezone(tz=tz)
        return dt
    except ValueError as e:
        raise argparse.ArgumentTypeError('{}: Date must be in ISO format. e.g. 2020-01-01'.format(e))


if __name__ == '__main__':
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    parser = argparse.ArgumentParser(description='export todoist data with certain format')
    parser.add_argument('--api-token',
                        default=os.environ.get('TODOIST_API_TOKEN'),
                        help='todoist API token')
    parser.add_argument('--data',
                        choices=['daily-report'],
                        help='Data type to be exported',
                        required=True)
    parser.add_argument('--format',
                        default='yaml',
                        choices=['yaml'],
                        help='Data export format')
    parser.add_argument('--from-date',
                        type=date_validation,
                        default=yesterday.strftime('%Y-%m-%d'),
                        help='From date where you retrieve data. Must be ISO format (YYYY-MM-DD)')
    parser.add_argument('--until-date',
                        type=date_validation,
                        default=now.strftime('%Y-%m-%d'),
                        help='Until date where you retrieve data. Must be ISO format (YYYY-MM-DD)')
    args = parser.parse_args()
    cli = TodoistAPIClient(args.api_token)
    exp = TodoistExport(cli)
    if args.data == 'daily-report':
        res = exp.export_daily_report(from_dt=args.from_date, until_dt=args.until_date, format=args.format)
        print(res)
    else:
        raise argparse.ArgumentError('--data is invalid')
