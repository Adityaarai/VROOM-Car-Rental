# Generated by Django 5.0.3 on 2024-05-11 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carlisting', '0013_remove_carorder_verified_carorder_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardetail',
            name='availability',
            field=models.CharField(choices=[('Unlisted', 'Unlisted'), ('Booked', 'Booked'), ('Available', 'Available')], default='Unlisted', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='carorder',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Paid', 'Paid'), ('Completed', 'Completed')], default='Pending', max_length=100, null=True),
        ),
    ]
