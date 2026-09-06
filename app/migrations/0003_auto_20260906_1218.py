from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0002_auto_20260904_0940')]

    initial = False

    operations = [
        ops.CreateModel(
            name='Tasks',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('name', fields.CharField(max_length=100)),
                ('description', fields.CharField(null=True, max_length=1000)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', db_constraint=True, to_field='id', related_name='tasks', on_delete=OnDelete.CASCADE)),
                ('deadline', fields.CharField(max_length=9)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('updated_at', fields.DatetimeField(auto_now=True, auto_now_add=False)),
            ],
            options={'table': 'tasks', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
