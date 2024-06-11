from src.infrastructure.db.db_migrator import DBMigrator


def migrate_db() -> None:
    db_migrator = DBMigrator()
    print('Applying pending DB migrations:')
    db_migrator.apply_pending()


def run_services() -> None:
    migrate_db()


# This code will run using gunicorn, and before workers are created. So it will be always be executed just one time
def on_starting(_) -> None:
    run_services()
