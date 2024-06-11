from dataclasses import dataclass


@dataclass
class DBMigration:
    number: int
    path: str

    @classmethod
    def from_str(cls, string: str) -> 'DBMigration':
        _, str_number = string.split('_')
        return DBMigration(
            number=int(str_number.split('.')[0]),
            path=string
        )
