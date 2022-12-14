# Generated by Django 3.2.15 on 2022-09-28 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drones', '0003_auto_20220927_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='drones.model'),
        ),
        migrations.AlterField(
            model_name='drone',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='drones.state'),
        ),
    ]
