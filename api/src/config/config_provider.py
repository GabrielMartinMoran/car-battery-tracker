import os

from dotenv import load_dotenv

load_dotenv()


class _ConfigProvider:
    API_PAGES_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'app', 'pages')

    DB_SCHEMA = 'car_battery_tracker'
    DB_HOST = os.environ['PDB_HOST']
    DB_NAME = os.environ['PDB_DATABASE']
    DB_USER = os.environ['PDB_USER']
    DB_PASSWORD = os.environ['PDB_PASSWORD']
    DB_PORT = os.environ['PDB_PORT']


ConfigProvider = _ConfigProvider()
