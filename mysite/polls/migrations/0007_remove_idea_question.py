# Generated by Django 3.1.1 on 2020-11-14 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_idea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='question',
        ),
    ]
