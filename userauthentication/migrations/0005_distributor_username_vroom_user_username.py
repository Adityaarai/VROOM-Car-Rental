# Generated by Django 5.0.3 on 2024-05-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauthentication', '0004_distributor_user_vroom_user_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='distributor',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vroom_user',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
