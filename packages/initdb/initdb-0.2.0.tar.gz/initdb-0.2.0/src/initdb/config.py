import os

__all__ = [
    'config', 'Config'
]


class Config:
    """
    Contains all parameters required by the application
    """

    def __init__(self):
        self.host = os.environ.get(
            "DATABASE_HOST",
            "postgres"
        )
        # initial_user and initial_password are used to
        # check if database is up and running
        self.initial_user = os.environ.get(
            "INITIAL_DATABASE_USER",
            "postgres"
        )
        self.initial_password = os.environ.get(
            "INITIAL_DATABASE_PASSWORD",
            None
        )
        self.user = os.environ.get(
            "DATABASE_USER",
            None
        )
        self.database = os.environ.get(
            "DATABASE_NAME",
            None
        )
        self.password = os.environ.get(
            "DATABASE_PASSWORD",
            None
        )
        self.port = os.environ.get(
            "DATABASE_PORT",
            5432
        )

    def print(self):
        print(f"host={self.host}")
        print(f"port={self.port}")
        print(f"initial_user={self.initial_user}")
        print(f"initial_pass={self.initial_password}")
        print(f"user={self.user}")
        print(f"database={self.database}")
        print(f"pass={self.password}")

    def __str__(self):
        return f"Config(host={self.host}, port={self.port})"


config = Config()
