import argparse
import importlib
import logging
import sys
import yaml
from pathlib import Path


from .checker import ValidationError, register_check, has_check, get_check, run_check
from .validator import ProjectModel
from . import checks as _checks  # importing to register checks

__all__ = ["ValidationError", "main", "register_check", "run_check"]


logger = logging.getLogger(__name__)


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


def load_checks():
    """Load checks from current directory (./checks.py)
    """
    cwd = Path.cwd()
    if (cwd / "checks.py").is_file():
        logger.info("Detected checks.py file in current directory")
        sys.path.insert(0, ".")
        # importing will load the checks because of @register_check
        importlib.import_module("checks")
        sys.path.pop(0)
        logger.info("Checks loaded from current directory")
        # NOTE: maybe also list the particular checks that were loaded
        # this can be done simply by taking a snapshot of "CHECKS" list
        # and diffing it with after importing checks from the current module
    else:
        logger.info("checks.py is not present in current directory")
        logger.info("No checks loaded")


def main():
    args = parse_args()

    if args.subcommand == "run":
        load_checks()

        print("Running checks...")
        context = {"app_dir": args.app_dir, "app_url": args.app_url}
        tasks = get_tasks(task_name=args.task)
        for i, task in enumerate(tasks, start=1):
            print(f"Running checks for task {i}: {task['title']}")
            check_statuses = []
            for ck_i, check in enumerate(task["checks"], start=1):
                check_status = run_check(
                    check["name"], context=context, args=check["args"])
                check_statuses.append(check_status)
                print(f"Check {ck_i}: {check['title']}, using {check['name']}")
                print(yaml.dump(check_status.dict(), sort_keys=False))

            if all(c.status == "pass" for c in check_statuses):
                print("Task completed successfully")
            elif any(c.status == "fail" for c in check_statuses):
                print("Task failed")
                break
            elif any(c.status == "error" for c in check_statuses):
                print("Task errored")
                break
            else:
                c = next(c for c in check_statuses
                         if c.status not in {"pass", "fail", "error"})
                raise Exception(f"Unrecognized check status: {c.status}")

    elif args.subcommand == "validate":
        print("Validating ...")
        if not Path("capstone.yml").is_file():
            raise Exception("capstone.yml is not present in current directory")
        elif not Path("checks.py").is_file():
            raise Exception("checks.py is not present in current directory")
        elif not Path("repo").is_dir():
            raise Exception("repo directory is not present in current directory")
        try:
            project_spec = yaml.safe_load(open("capstone.yml"))
        except yaml.YAMLError as e:
            raise Exception("capstone.yml is not a valid YAML file") from e

        # this will raise an error when spec is invalid:
        project = ProjectModel.parse_obj(project_spec)
        print("capstone.yml is valid")

        load_checks()
        for task in project.tasks:
            for check in project.checks:
                if not has_check(check.name):
                    raise Exception(f"Check {check.name} is not registered")
                elif not callable(get_check(check.name)):
                    raise Exception(f"Check {check.name} is not callable")
                # TODO: maybe validate the signature of the function as well?
                # ref: https://docs.python.org/3/library/inspect.html#inspect.getfullargspec

    else:
        raise ValueError(f"Invalid subcommand: {args.subcommand}")
