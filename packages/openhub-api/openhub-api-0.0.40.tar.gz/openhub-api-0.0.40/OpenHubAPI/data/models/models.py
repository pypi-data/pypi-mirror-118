from django.db import models
import uuid
from django.utils import timezone
import time
from polymorphic.models import PolymorphicModel


class Hub(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ip = models.URLField()
    category = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    display_name = models.CharField(max_length=255, null=True)
    aid = models.IntegerField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]


class Hardware(PolymorphicModel):
    class Type(models.TextChoices):
        DHT22 = 'DHT22'
        MCP3008 = 'MCP3008'
        ModProbe = 'ModProbe'
        PiPico = 'PiPico'
        VEML7700 = 'VEML7700'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.PiPico,
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, null=False)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()

        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]


class PiPico(Hardware):
    serial_com = models.CharField(max_length=100, null=True)
    pi_gpio_interrupt = models.IntegerField()


class DHT22(Hardware):
    pin = models.IntegerField()


class MCP3008(Hardware):
    sck = models.IntegerField()
    miso = models.IntegerField()
    cs_pin = models.IntegerField()
    num_channels = models.IntegerField()


class ModProbe(Hardware):
    base_dir = models.CharField(max_length=100, null=True)
    file_name = models.CharField(max_length=100, null=True)


class VEML7700(Hardware):
    scl = models.IntegerField()
    sda = models.IntegerField()

class PMSA0031(Hardware):
    scl = models.IntegerField()
    sda = models.IntegerField()
    reset = models.IntegerField()

class HardwareChannelTypes(models.Model):
    hardware_type = models.CharField(
        max_length=20
    )
    channel_type = models.CharField(
        max_length=20
    )


class Channel(models.Model):
    def __str__(self):
        return self.get_name_display()

    def get_name_display(self):
        name = ''
        if self.hardware is not None:
            name = name + self.hardware.type + ' / '
        name = name + self.type + ' / ' + str(self.channel_index) + ' / ' + str(self.id)
        return name

    class Type(models.TextChoices):
        DHT22Humidity = 'DHT22Humidity'
        DHT22Temp = 'DHT22Temp'
        MCP3008Analog = 'MCP3008Analog'
        ModProbeTemp = 'ModProbeTemp'
        PiPicoAnalog = 'PiPicoAnalog'
        PiPicoPump = 'PiPicoPump'
        PiPicoRelay = 'PiPicoRelay'
        VEML7700Light = 'VEML7700Light'
        VEML7700Lux = 'VEML7700Lux'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    channel_index = models.IntegerField(null=True)
    type = models.CharField(
        max_length=15
    )
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, null=False)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()

        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['id', 'hardware']),
        ]



class HardwareIO(PolymorphicModel):

    SPI = 'SPI'
    Serial = 'Serial'
    PWM = 'PWM'
    I2C = 'I2C'
    DeviceFile = 'Device File'
    MCPChannel = 'MCP Channel'
    PiPicoAnalog = 'Pi Pico Analog'
    PiGPIO = 'Pi GPIO'
    hardware_io_types_choices = [(SPI,SPI),(Serial,Serial),(PWM,PWM),(I2C,I2C),(DeviceFile,DeviceFile),(MCPChannel,MCPChannel),(PiPicoAnalog,PiPicoAnalog),(PiGPIO,PiGPIO)]

    label = models.CharField(max_length=255, null=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    parent_hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, blank=True, null=True,related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss")
    child_hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, blank=True, null=True)
    child_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=25, choices=hardware_io_types_choices, default=PiPicoAnalog)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, null=False)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()

        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['id', 'parent_hardware', 'child_channel']),
        ]

class PiPins(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hardware_io = models.ForeignKey(HardwareIO, on_delete=models.CASCADE, blank=True, null=True)
    pin = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['hardware_io']),
        ]

class SPIIo(HardwareIO):
    sck = models.IntegerField()
    miso = models.IntegerField()
    mosi = models.IntegerField()

class SerialIo(HardwareIO):
    port = models.CharField(max_length=100)

class PwmIo(HardwareIO):
    en = models.IntegerField()
    duty_max = models.IntegerField()
    duty_min = models.IntegerField()
    freq = models.IntegerField()

class I2cIo(HardwareIO):
    scl = models.IntegerField()
    sda = models.IntegerField()

class DeviceFileIo(HardwareIO):
    base_dir = models.CharField(max_length=100, null=True)
    device_file = models.CharField(max_length=100, null=True)

class MCPAnalogIo(HardwareIO):
    channel_index = models.IntegerField()

class PiPicoAnalogIo(HardwareIO):
    pin = models.IntegerField()

class PiGpio(HardwareIO):
    pin =  models.IntegerField()


class Accessory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, null=False)

    category = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    display_name = models.CharField(max_length=255, null=True)
    aid = models.IntegerField()
    channels = models.ManyToManyField(Channel)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]


class HardwareConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=255, null=True)
    value = models.CharField(max_length=255, null=True)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()

        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['id', 'hardware']),
        ]


class Calibration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=255, null=True)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, blank=True, null=True, default=None)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()

        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]


class CalibrationConstants(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=255, null=True)
    value = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    calibration = models.ForeignKey(Calibration, on_delete=models.CASCADE, blank=True, null=False)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()

        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]


class Category(models.Model):
    name = models.CharField(max_length=255, null=True)
    enum = models.IntegerField(null=True)


class AccessoryType(models.Model):
    type = models.CharField(max_length=255, null=True)