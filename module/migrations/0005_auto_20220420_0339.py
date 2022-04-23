# Generated by Django 3.2.6 on 2022-04-20 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0004_remove_module_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='type_handler',
            field=models.CharField(choices=[('STIR_FRY_MODULE', 'STIR_FRY_MODULE'), ('DEEP_FRY_MODULE', 'DEEP_FRY_MODULE'), ('GRILLING_MODULE', 'GRILLING_MODULE'), ('DRINKS_MODULE', 'DRINKS_MODULE'), ('BOILER_MODULE', 'BOILER_MODULE'), ('STEAMING_MODULE', 'STEAMING_MODULE'), ('TRANSPORTER_MODULE', 'TRANSPORTER_MODULE')], default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='queue_handler',
            field=models.CharField(choices=[('192.168.42.116', '192.168.42.116'), ('192.168.42.117', '192.168.42.117'), ('192.168.42.118', '192.168.42.118'), ('192.168.42.119', '192.168.42.119'), ('192.168.42.120', '192.168.42.120'), ('192.168.42.121', '192.168.42.121'), ('192.168.42.122', '192.168.42.122'), ('192.168.42.123', '192.168.42.123')], default=None, max_length=200, null=True),
        ),
    ]