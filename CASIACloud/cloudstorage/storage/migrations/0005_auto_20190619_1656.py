# Generated by Django 2.0.7 on 2019-06-19 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_data_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='uuid',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
