import sys


def is_running_on_uvicorn() -> bool:
    return 'uvicorn' in sys.argv[0]
