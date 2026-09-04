from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(
        max_length=255,
        min_length=3
    )

    email = fields.CharField(
        max_length=255,
        min_length=3,
        unique=True,
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )

    password = fields.CharField(
        max_length=255
    )

    access_token = fields.CharField(max_length=500, null=True, blank=True)
    
    refresh_token = fields.CharField(max_length=500, null=True, blank=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"