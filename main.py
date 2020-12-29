#!/usr/bin/env python3
import argparse
import os
from todoist_export import TodoistAPIClient, TodoistExport

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='export todoist data with certain format')
    parser.add_argument('--api-token', default=os.environ.get('TODOIST_API_TOKEN'))
    args = parser.parse_args()
    cli = TodoistAPIClient(args.api_token)
    exp = TodoistExport(cli)
    print("done")
