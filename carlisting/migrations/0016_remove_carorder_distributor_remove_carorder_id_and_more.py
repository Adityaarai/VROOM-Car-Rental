# Generated by Django 5.0.3 on 2024-05-16 10:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carlisting', '0015_alter_cardetail_availability'),
        ('userauthentication', '0007_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carorder',
            name='distributor',
        ),
        migrations.RemoveField(
            model_name='carorder',
            name='id',
        ),
        migrations.RemoveField(
            model_name='carorder',
            name='rentee_email',
        ),
        migrations.AddField(
            model_name='carorder',
            name='order_id',
            field=models.AutoField(primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carorder',
            name='rentee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='userauthentication.profile'),
        ),
        migrations.AddField(
            model_name='carorder',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='carorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='carlisting.cardetail'),
        ),
    ]
