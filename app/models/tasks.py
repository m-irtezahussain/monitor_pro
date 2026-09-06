from tortoise.models import Model
from tortoise import fields

class Tasks(Model):
    id=fields.IntField(pk=True)

    name=fields.CharField(max_length=100)

    description=fields.CharField(min_length=10, max_length=1000, null=True)

    user=fields.ForeignKeyField(
        "models.User",
        related_name="tasks",
        null=False,
        on_delete=fields.CASCADE
    )

    deadline=fields.CharField(min_length=9, max_length=9)

    created_at=fields.DatetimeField(auto_now_add=True)
    updated_at=fields.DatetimeField(auto_now=True)

    class Meta:
        table="tasks"