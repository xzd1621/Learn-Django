# Generated by Django 2.0.7 on 2019-06-19 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0006_auto_20190619_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='password',
            field=models.CharField(max_length=30),
        ),
    ]