# Generated by Django 5.0.3 on 2024-04-07 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carlisting', '0003_carorders'),
    ]

    operations = [
        migrations.AddField(
            model_name='carorders',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]