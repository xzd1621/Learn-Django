# Generated by Django 2.0.7 on 2019-06-19 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_auto_20190619_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='file',
        ),
        migrations.AlterField(
            model_name='data',
            name='data_type',
            field=models.CharField(max_length=30),
        ),
    ]
