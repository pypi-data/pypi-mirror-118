# Generated by Django 3.2.4 on 2021-07-12 20:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_auto_20210712_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='PiPins',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('pin', models.IntegerField()),
                ('hardware_io', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.hardwareio')),
            ],
        ),
        migrations.AddIndex(
            model_name='pipins',
            index=models.Index(fields=['hardware_io'], name='data_pipins_hardwar_586dc9_idx'),
        ),
    ]
