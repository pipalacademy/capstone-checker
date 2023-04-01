import argparse
import json
import yaml

from .checker import ValidationError, register_check, run_check
from . import checks as _checks  # importing to register checks

__all__ = ["ValidationError", "main", "register_check", "run_check"]


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
            title="subcommands",
            description="Valid subcommands",
            dest="subcommand",
            required=True)

    parser_run = subparsers.add_parser("run")
    parser_run.add_argument("--app-url", required=True)
    parser_run.add_argument("--app-dir", required=True)
    parser_run.add_argument("--task", default=None)

    parser_validate = subparsers.add_parser("validate")

    return parser.parse_args()


def get_tasks(task_name=None):
    capstone_config = yaml.load(open("capstone.yml"))
    if task_name is not None:
        return next(task
                    for task in capstone_config["tasks"]
                    if task["name"] == task_name)
    else:
        return capstone_config["tasks"]


def main():
    args = parse_args()

    if args.subcommand == "run":
        # NOTE: should run stop when a check/task fails?
        print("Running checks...")
        context = {"app_dir": args.app_dir, "app_url": args.app_url}
        tasks = get_tasks(task_name=args.task)
        for (i, task) in enumerate(tasks, start=1):
            print(f"Running checks for task {i}:", task["title"])
            for check in task["checks"]:
                check_status = run_check(
                    check["name"], context=context, args=check["args"])
                print(json.dumps(check_status.dict(), indent=4))
    elif args.subcommand == "validate":
        print("Validating capstone.yml...")
        # TODO: ...
    else:
        raise ValueError(f"Invalid subcommand: {args.subcommand}")
