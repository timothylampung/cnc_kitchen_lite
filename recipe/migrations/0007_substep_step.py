# Generated by Django 3.2.6 on 2022-04-21 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_alter_recipe_handler_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='substep',
            name='step',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='sub_steps', to='recipe.step'),
        ),
    ]
