#!/usr/bin/env python
"""Django's command-line tool. We use it to run the server, migrations, and our own commands."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_recommender.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django is not installed. Activate your virtual environment and run: "
            "pip install -r requirements.txt"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
