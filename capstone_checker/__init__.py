import argparse

from .checker import register_check

__all__ = ["register_check", "main"]


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


def main():
    args = parse_args()

    if args.subcommand == "run":
        print("Running checks...")
        # TODO: ...
    elif args.subcommand == "validate":
        print("Validating capstone.yml...")
        # TODO: ...
    else:
        raise ValueError(f"Invalid subcommand: {args.subcommand}")
