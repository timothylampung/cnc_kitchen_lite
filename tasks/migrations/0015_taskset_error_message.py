# Generated by Django 3.2.6 on 2022-04-22 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_auto_20220422_0401'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskset',
            name='error_message',
            field=models.CharField(max_length=3000, null=True),
        ),
    ]
