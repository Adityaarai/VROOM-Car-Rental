# Generated by Django 5.0.3 on 2024-05-11 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauthentication', '0005_distributor_username_vroom_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vroom_user',
            name='user',
        ),
        migrations.DeleteModel(
            name='Distributor',
        ),
        migrations.DeleteModel(
            name='Vroom_User',
        ),
    ]