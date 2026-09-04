from os import getenv

TORTOISE_ORM = {
    "connections": {
        "default": getenv("DATABASE_URL")
    },
    "apps": {
        "models": {
            "models": [
                "app.models.user"
            ],
            "default_connection": "default",
            "migrations": "app.migrations"
        }
    }
}
