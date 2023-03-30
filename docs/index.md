# Capstone Checker

## Installation

```
pip install git+https://github.com/pipalacademy/capstone-checker.git
```

## Usage

In a project's `checks.py`, import `register_check` and
`main`.

```python
# checks.py

from capstone_checker import register_check, main


@register_check()
def check_train_search(context, args):
    ...

if __name__ == "__main__":
    main()
```

To run checks for all tasks (with current directory as project directory with `capstone.yml`):

```
$ python checks.py run --app-url http://localhost:8080 --app-dir /tmp/app
```

To run check for one task:

```
python checks.py run --task task-name --app-url http://localhost:8080 --app-dir /tmp/app
```

Validate the syntax of `capstone.yml`.

```
$ python checks.py validate
```
