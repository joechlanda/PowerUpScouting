# Generated by Django 2.0.2 on 2018-03-03 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorer', '0002_auto_20180303_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='parked',
        ),
    ]