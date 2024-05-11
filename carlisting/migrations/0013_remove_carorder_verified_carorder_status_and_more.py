# Generated by Django 5.0.3 on 2024-05-11 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carlisting', '0012_rename_rentee_name_carorder_rentee_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carorder',
            name='verified',
        ),
        migrations.AddField(
            model_name='carorder',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Paid', 'Paid'), ('Completed', 'Completed')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cardetail',
            name='availability',
            field=models.CharField(choices=[('Unlisted', 'Unlisted'), ('Booked', 'Booked'), ('Available', 'Available')], max_length=20, null=True),
        ),
    ]