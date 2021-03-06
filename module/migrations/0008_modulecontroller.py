# Generated by Django 3.2.6 on 2022-04-22 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_lifecycle.mixins


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('module', '0007_rename_queue_handler_module_ip_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleController',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], default='ACTIVE', max_length=200, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('document_code', models.CharField(blank=True, max_length=400, null=True)),
                ('ip_address', models.CharField(choices=[('CM HEATER', 'CM HEATER'), ('CM MIXER', 'CM MIXER'), ('CM VALVE', 'CM VALVE'), ('PU PICKUP', 'PU PICKUP')], default=None, max_length=200, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulecontroller_creator', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modulecontroller_editor', to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='controllers', to='module.module')),
            ],
            options={
                'abstract': False,
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
