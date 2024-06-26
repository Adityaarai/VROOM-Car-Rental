# Generated by Django 5.0.3 on 2024-04-12 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carlisting', '0007_alter_cardetails_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carorders',
            old_name='date',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='carorders',
            old_name='status',
            new_name='verified',
        ),
        migrations.AddField(
            model_name='carorders',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
    ]
