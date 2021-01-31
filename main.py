#!/usr/bin/env python3
import argparse
import os
from todoist_export import TodoistAPIClient, TodoistExport
from datetime import datetime, timedelta
import tzlocal
from logging import getLogger


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
        naive_dt = datetime.strptime(date_str, "%Y-%m-%d")
        dt = naive_dt.astimezone(tz=tz)
        return dt
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            "{}: Date must be in ISO format. e.g. 2020-01-01".format(e)
        )


if __name__ == "__main__":
    logger = getLogger(__name__)
    tz = tzlocal.get_localzone()
    now = datetime.now(tz=tz)
    yesterday = now - timedelta(days=1)
    parser = argparse.ArgumentParser(
        description="export todoist data with certain format"
    )
    parser.add_argument(
        "--api-token",
        type=str,
        default=os.environ.get("TODOIST_API_TOKEN"),
        help="todoist API token",
    )
    parser.add_argument(
        "--data",
        type=str,
        choices=["daily-report"],
        help="Data type to be exported",
        required=True,
    )
    parser.add_argument(
        "--format",
        type=str,
        default="yaml",
        choices=["yaml"],
        help="Data export format",
    )
    parser.add_argument(
        "--pj-filter", type=str, default=".*", help="Project filter regular expression"
    )
    parser.add_argument(
        "--from-date",
        type=date_validation,
        default=yesterday.strftime("%Y-%m-%d"),
        help="From date where you retrieve data. Must be ISO format (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--until-date",
        type=date_validation,
        default=now.strftime("%Y-%m-%d"),
        help="Until date where you retrieve data. Must be ISO format (YYYY-MM-DD)",
    )
    args = parser.parse_args()
    cli = TodoistAPIClient(args.api_token)
    exp = TodoistExport(cli)

    # args validation
    if args.from_date > now:
        logger.fatal(
            "from has to be before current time: {} > {}".format(
                str(args.from_date), str(now)
            )
        )
    if args.from_date > args.until_date:
        logger.fatal(
            "from date has to be before until: {}, {}".format(
                str(args.from_date), str(args.until_date)
            )
        )
    if args.data == "daily-report":
        tz = tzlocal.get_localzone()
        res = exp.export_daily_report(
            from_dt=args.from_date,
            until_dt=args.until_date,
            pj_filter=args.pj_filter,
            tz=tz,
            format=args.format,
        )
        print(res)
    else:
        raise argparse.ArgumentError("--data is invalid")
