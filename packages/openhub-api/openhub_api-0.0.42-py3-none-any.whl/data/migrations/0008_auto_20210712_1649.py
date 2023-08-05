# Generated by Django 3.2.4 on 2021-07-12 16:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('data', '0007_pipico_serial_com'),
    ]

    operations = [
        migrations.CreateModel(
            name='HardwareIO',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('child_channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.channel')),
                ('child_hardware', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.hardware')),
                ('hub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.hub')),
                ('parent_hardware', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_hardwareio_related', related_query_name='data_hardwareios', to='data.hardware')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_data.hardwareio_set+', to='contenttypes.contenttype')),
            ],
        ),
        migrations.AlterField(
            model_name='hardwarechanneltypes',
            name='channel_type',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='hardwarechanneltypes',
            name='hardware_type',
            field=models.CharField(max_length=20),
        ),
        migrations.CreateModel(
            name='DeviceFileIo',
            fields=[
                ('hardwareio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.hardwareio')),
                ('base_dir', models.CharField(max_length=100, null=True)),
                ('device_file', models.CharField(max_length=100, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('data.hardwareio',),
        ),
        migrations.CreateModel(
            name='I2cIo',
            fields=[
                ('hardwareio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.hardwareio')),
                ('scl', models.IntegerField()),
                ('sda', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('data.hardwareio',),
        ),
        migrations.CreateModel(
            name='MCPAnalogIo',
            fields=[
                ('hardwareio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.hardwareio')),
                ('channel_index', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('data.hardwareio',),
        ),
        migrations.CreateModel(
            name='PiGpio',
            fields=[
                ('hardwareio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.hardwareio')),
                ('pin', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('data.hardwareio',),
        ),
        migrations.CreateModel(
            name='PiPicoAnalogIo',
            fields=[
                ('hardwareio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.hardwareio')),
                ('channel_index', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('data.hardwareio',),
        ),
        migrations.CreateModel(
            name='PwmIo',
            fields=[
                ('hardwareio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.hardwareio')),
                ('pwm_pin', models.IntegerField()),
                ('duty_max', models.IntegerField()),
                ('duty_min', models.IntegerField()),
                ('freq', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('data.hardwareio',),
        ),
        migrations.CreateModel(
            name='SerialIo',
            fields=[
                ('hardwareio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.hardwareio')),
                ('port', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('data.hardwareio',),
        ),
        migrations.CreateModel(
            name='SPIIo',
            fields=[
                ('hardwareio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.hardwareio')),
                ('sck', models.IntegerField()),
                ('miso', models.IntegerField()),
                ('mosi', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('data.hardwareio',),
        ),
        migrations.AddIndex(
            model_name='hardwareio',
            index=models.Index(fields=['id', 'parent_hardware', 'child_channel'], name='data_hardwa_id_5685de_idx'),
        ),
    ]
