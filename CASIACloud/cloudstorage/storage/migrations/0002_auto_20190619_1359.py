# Generated by Django 2.0.7 on 2019-06-19 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='uuid',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
    ]