import json

from django.core import serializers as django_serializers
from django.http import JsonResponse, HttpResponse, QueryDict
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from polymorphic.models import PolymorphicTypeInvalid
from rest_framework import viewsets, renderers
from rest_framework.response import Response

from data.forms.forms import HardwareForm, HardwareDHT22Form, HardwareMCP3008Form, HardwareModProbeForm, \
    HardwarePiPicoForm, HardwareVEML7700Form, HardwareTypeForm, ChannelForm, HardwareConfigForm, AccessoryForm, \
    CalibrationForm, CalibrationConstantForm, HubForm, HardwareIOTypeForm, SPIIoForm, PwmIoForm, SerialIoForm, \
    I2cIoForm, DeviceFileIoForm, MCPAnalogIoForm, PiPicoAnalogIoForm, PiGpioForm, HardwareIoForm, HardwarePMSA0031Form
from data.models.models import Hardware, DHT22, MCP3008, ModProbe, PiPico, VEML7700, Accessory, Calibration, \
    CalibrationConstants, Channel, Hub, HardwareIO
from data.serializers.serializers import HardwareSerializer, ChannelSerializer, AccessorySerializer, \
    CalibrationSerializer, HubSerializer, HardwareIOSerializer


SPI = 'SPI'
Serial = 'Serial'
PWM = 'PWM'
I2C = 'I2C'
DeviceFile = 'Device File'
MCPChannel = 'MCP Channel'
PiPicoAnalog = 'Pi Pico Analog'
PiGPIO = 'Pi GPIO'


class HardwareViewSet(viewsets.ModelViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def updateHardware(request):
        if request.is_ajax and request.method == "POST":
            # get the form data
            hardware = Hardware.objects.get(pk=request.POST['initial-id'])

            form = HardwareForm(data=request.POST, instance=hardware)
            hardware_type = form.data['type']
            if hardware_type == 'DHT22':
                form = HardwareDHT22Form(data=request.POST, instance=hardware)
            if hardware_type == 'MCP3008':
                form = HardwareMCP3008Form(data=request.POST, instance=hardware)
            if hardware_type == 'ModProbe':
                form = HardwareModProbeForm(data=request.POST, instance=hardware)
            if hardware_type == 'PiPico':
                form = HardwarePiPicoForm(data=request.POST, instance=hardware)
            if hardware_type == 'VEML7700':
                form = HardwareVEML7700Form(data=request.POST, instance=hardware)
            if hardware_type == 'PMSA0031':
                form = HardwarePMSA0031Form(data=request.POST, instance=hardware)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)

    def getHardwareTypeForm(request):
        form = HardwareTypeForm(request.POST)
        hardware_type = form.data['type']
        if hardware_type == 'DHT22':
            form = HardwareDHT22Form(initial={'type': 'DHT22'})
        if hardware_type == 'MCP3008':
            form = HardwareMCP3008Form(initial={'type': 'MCP3008'})
        if hardware_type == 'ModProbe':
            form = HardwareModProbeForm(initial={'type': 'ModProbe'})
        if hardware_type == 'PiPico':
            form = HardwarePiPicoForm(initial={'type': 'PiPico'})
        if hardware_type == 'VEML7700':
            form = HardwareVEML7700Form(initial={'type': 'VEML7700'})
        if hardware_type == 'PMSA0031':
            form = HardwarePMSA0031Form(initial={'type': 'PMSA0031'})
        return HttpResponse(form.as_p())

    def getHardwareIoForm(request):
        form = HardwareIOTypeForm(request.POST)
        hardware_io_type = form.data['type']
        initial = {}
        if 'parent_hardware' in form.data.keys():
            initial['parent_hardware'] = form.data['parent_hardware']
        if 'child_hardware' in form.data.keys():
            initial['child_hardware'] = form.data['child_hardware']
        if 'child_channel' in form.data.keys():
            initial['child_channel'] = form.data['child_channel']
        if 'child_channel' in form.data.keys():
            initial['hub'] = form.data['hub']
        if 'type' in form.data.keys():
            initial['type'] = form.data['type']

        if hardware_io_type == SPI:
            form = SPIIoForm(initial=initial)
            form.type = SPI

        if hardware_io_type == PWM:
            form = PwmIoForm(initial=initial)
            form.type = PWM

        if hardware_io_type == Serial:
            form = SerialIoForm(initial=initial)
            form.type = Serial

        if hardware_io_type == I2C:
            form = I2cIoForm(initial=initial)
            form.type = I2C

        if hardware_io_type == DeviceFile:
            form = DeviceFileIoForm(initial=initial)
            form.type = DeviceFile

        if hardware_io_type == MCPChannel:
            form = MCPAnalogIoForm(initial=initial)
            form.type = MCPChannel

        if hardware_io_type == PiPicoAnalog:
            form = PiPicoAnalogIoForm(initial=initial)
            form.type = PiPicoAnalog

        if hardware_io_type == PiGPIO:
            form = PiGpioForm(initial=initial)
            form.type = PiGPIO

        return HttpResponse(form.as_p())

    def list(self, request, *args, **kwargs):
        print("list")

        response = super(HardwareViewSet, self).list(request, *args, **kwargs)
        form_type = HardwareTypeForm(initial={'type': 'PiPico'})
        hardware_form = HardwarePiPicoForm(initial={'type': 'PiPico'})
        hardware = Hardware.objects.all()

        serialized_hardware = HardwareSerializer().to_json_array(hardware)
        if request.accepted_renderer.format == 'html':
            return Response({"form": hardware_form, "type_form": form_type, "hardwares": hardware},
                            template_name='hardwares.html')
            # return Response({"hardwares": hardware}, template_name='hardwares.html')
        return response

    def getChannels(self, hardware_id):
        channels = Hardware.objects.get(pk=str(hardware_id)).channel_set.all()
        serialized_hardware = ChannelSerializer(many=True).to_representation(channels)

        # if request.accepted_renderer.format == 'html':
        return JsonResponse(serialized_hardware, status=200, safe=False)

    def getConfig(self, hardware_id):
        hardware_configs = Hardware.objects.get(pk=str(hardware_id)).hardwareconfig_set.all()
        config = {}
        for hardware_config in hardware_configs:
            config[hardware_config.type] = hardware_config.value
        # if request.accepted_renderer.format == 'html':
        return JsonResponse({"config": config}, status=200)

    def indexView(request):
        print("indexView")
        form = HardwareForm()
        hardware = Hardware.objects.all()
        return render(request, "hardwares.html", {"form": form, "hardware": hardware})

    SPI = 'SPI'
    Serial = 'Serial'
    PWM = 'PWM'
    I2C = 'I2C'
    DeviceFile = 'Device File'
    MCPChannel = 'MCP Channel'
    PiPicoAnalog = 'Pi Pico Analog'
    PiGPIO = 'Pi GPIO'

    def postHardwareIO(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "POST":
            # get the form data
            hardware_io_form = HardwareIoForm(request.POST)
            hardware_io_type = hardware_io_form.data['type']
            if hardware_io_type == SPI:
                hardware_form = SPIIoForm(request.POST)
            if hardware_io_type == Serial:
                hardware_form = SerialIoForm(request.POST)
            if hardware_io_type == PWM:
                hardware_form = PwmIoForm(request.POST)
            if hardware_io_type == I2C:
                hardware_form = I2cIoForm(request.POST)
            if hardware_io_type == DeviceFile:
                hardware_form = DeviceFileIoForm(request.POST)
            if hardware_io_type == MCPChannel:
                hardware_form = MCPAnalogIoForm(request.POST)
            if hardware_io_type == PiPicoAnalog:
                hardware_form = PiPicoAnalogIoForm(request.POST)
            if hardware_io_type == PiGPIO:
                hardware_form = PiGpioForm(request.POST)
            # save the data and after fetch the object in instance
            if hardware_form.is_valid():
                instance = hardware_form.save()
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": hardware_form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def postHardware(request):
        # request should be ajax and method should be POST.
        if request.is_ajax() and request.method == "POST":
            # get the form data
            hardware_form = HardwareForm(request.POST)
            hardware_type = request.POST['type']
            if hardware_type == 'DHT22':
                hardware_form = HardwareDHT22Form(request.POST)
            if hardware_type == 'MCP3008':
                hardware_form = HardwareMCP3008Form(request.POST)
            if hardware_type == 'ModProbe':
                hardware_form = HardwareModProbeForm(request.POST)
            if hardware_type == 'PiPico':
                hardware_form = HardwarePiPicoForm(request.POST)
            if hardware_type == 'VEML7700':
                hardware_form = HardwareVEML7700Form(request.POST)
            if hardware_type == 'PMSA0031':
                form = HardwarePMSA0031Form(request.POST)

            # save the data and after fetch the object in instance
            if hardware_form.is_valid():
                instance = hardware_form.save()
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": hardware_form.errors}, status=400)
        elif request.method == "POST":
            import json
            body_json = json.loads(request.body.decode('utf-8'))
            pi_pico = PiPico()
            pi_pico.id = body_json['id']
            pi_pico.type = body_json['type']
            pi_pico.hub = Hub.objects.get(pk=body_json['hub'])
            pi_pico.pi_gpio_interrupt = 1
            pi_pico.save()
            ser_instance = django_serializers.serialize('json', [pi_pico, ])

            return JsonResponse({"instance": ser_instance}, status=200)
        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def retrieve(self, request, *args, **kwargs):
        print('retrieve')
        print(str(request.path_info))
        hardware_form = HardwareForm(instance=Hardware.objects.get(**kwargs))
        hardware_type = Hardware.objects.get(**kwargs).type

        # hardware_io = HardwareIO.objects.get({'child_hardware':Hardware.objects.get(**kwargs).id})
        hardware_io_type_form = HardwareIOTypeForm(
            initial={'child_hardware': Hardware.objects.get(**kwargs), 'hub': Hardware.objects.get(**kwargs).hub})

        try:
            if hardware_type == 'DHT22':
                hardware_form = HardwareDHT22Form(instance=DHT22.objects.get(**kwargs), initial={'type': 'DHT22'})
            if hardware_type == 'MCP3008':
                hardware_form = HardwareMCP3008Form(instance=MCP3008.objects.get(**kwargs), initial={'type': 'MCP3008'})
            if hardware_type == 'ModProbe':
                hardware_form = HardwareModProbeForm(instance=ModProbe.objects.get(**kwargs),
                                                     initial={'type': 'ModProbe'})
            if hardware_type == 'PiPico':
                hardware_form = HardwarePiPicoForm(instance=PiPico.objects.get(**kwargs), initial={'type': 'PiPico'})
            if hardware_type == 'VEML7700':
                hardware_form = HardwareVEML7700Form(instance=VEML7700.objects.get(**kwargs),
                                                     initial={'type': 'VEML7700'})
            if hardware_type == 'PMSA0031':
                hardware_form = HardwarePMSA0031Form(instance=PMSA0031.objects.get(**kwargs),
                                                     initial={'type': 'PMSA0031'})
        except:
            hardware_form = HardwareForm(instance=Hardware.objects.get(**kwargs))

        channels = Hardware.objects.get(**kwargs).channel_set.all()
        hardware_configs = Hardware.objects.get(**kwargs).hardwareconfig_set.all()
        channel_form = ChannelForm(hardware_type=Hardware.objects.get(**kwargs).type,
                                   initial={'hardware': Hardware.objects.get(**kwargs)})
        hardware_config_form = HardwareConfigForm()
        if request.accepted_renderer.format == 'html':
            return Response(
                {"hardware_form": hardware_form, "channel_form": channel_form, "channels": channels,
                 "hardware_config_form": hardware_config_form,
                 "hardware_configs": hardware_configs, 'hardware_io_type_form': hardware_io_type_form},
                template_name='hardware.html')

    def postChannel(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "POST":
            # get the form data
            form = ChannelForm(data=request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def postConfig(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "POST":
            # get the form data
            form = HardwareConfigForm(request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def deleteHardware(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "POST":
            # get the form data
            hardware = Hardware.objects.get(
                pk=request.POST['id'])  # save the data and after fetch the object in instance
            try:
                from polymorphic.utils import reset_polymorphic_ctype
                hardware.delete()
            except PolymorphicTypeInvalid:

                hardware.get_real_concrete_instance_class().delete()
            return HttpResponse(render(request, 'hardwares.html'))


class AccessoryViewSet(viewsets.ModelViewSet):
    queryset = Accessory.objects.all()
    serializer_class = AccessorySerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def list(self, request, *args, **kwargs):
        print('list')
        response = super(AccessoryViewSet, self).list(request, *args, **kwargs)
        form = AccessoryForm()
        accessories = Accessory.objects.all()
        if request.accepted_renderer.format == 'html':
            return Response({"form": form, "accessories": accessories}, template_name='accessories.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        print('retrieve')
        print(str(request.path_info))
        accessory = Accessory.objects.get(**kwargs)
        calibrations = accessory.calibration_set.all()
        accessory_form = AccessoryForm(instance=accessory)
        calibration_form = CalibrationForm(initial={'accessory': accessory})
        if request.accepted_renderer.format == 'html':
            return Response(
                {"accessory_form": accessory_form, "calibration_form": calibration_form, "calibrations": calibrations},
                template_name='accessory.html')
        else:
            return super(AccessoryViewSet, self).retrieve()

    def postAccessory(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "POST":
            # get the form data
            form = AccessoryForm(request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def postCalibration(request):
        print('post calibration')

        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "POST":
            # get the form data
            form = CalibrationForm(request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def updateAccessory(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "PATCH":
            # get the form data
            form = AccessoryForm(instance=Accessory.objects.get(pk=QueryDict(request.body)['id']),
                                 data=QueryDict(request.body))
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def deleteAccessory(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "DELETE":
            # get the form data
            form = AccessoryForm(instance=Accessory.objects.get(pk=QueryDict(request.body)['id']),
                                 data=QueryDict(request.body))
            accessory = Accessory.objects.get(
                pk=QueryDict(request.body)['id'])  # save the data and after fetch the object in instance
            accessory.delete()

            return HttpResponse(render(request, 'accessories.html'))


class CalibrationViewSet(viewsets.ModelViewSet):
    queryset = Calibration.objects.all()
    serializer_class = CalibrationSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def retrieve(self, request, *args, **kwargs):
        print('retrieve')
        print(str(request.path_info))
        calibration = Calibration.objects.get(**kwargs)
        calibration_constants = calibration.calibrationconstants_set.all()
        calibration_form = CalibrationForm(instance=calibration)
        calibrationconstants_form = CalibrationConstantForm(initial={'calibration': calibration})

        calibration_constants_forms = []

        for calibration_constant in calibration_constants:
            calibration_constants_forms.append(CalibrationConstantForm(instance=calibration_constant))
        if request.accepted_renderer.format == 'html':
            return Response(
                {"calibration_form": calibration_form, "calibrationconstants_initial_form": calibrationconstants_form,
                 "calibrationconstants_forms": calibration_constants_forms,
                 "calibrations": calibration_constants, "calibration": calibration},
                template_name='calibration.html')
        else:
            return super(CalibrationViewSet, self).retrieve()

    def updateCalibration(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "UPDATE":
            # get the form data
            form = CalibrationForm(request.UPDATE)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def postCalibrationConstant(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "POST":
            # get the form data
            try:
                initial_calibration_constant = CalibrationConstants.objects.get(id=request.POST['id'])
                form = CalibrationConstantForm(instance=initial_calibration_constant, data=request.POST)
            except CalibrationConstants.DoesNotExist:
                form = CalibrationConstantForm(data=request.POST)

            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                form_json = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance, "form": form_json}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def retrieve(self, request, *args, **kwargs):
        print('retrieve')
        print(str(request.path_info))
        hardware_io_type_form = HardwareIOTypeForm(
            initial={'parent_hardware': Channel.objects.get(**kwargs).hardware.id,
                     'child_channel': Channel.objects.get(**kwargs).id,
                     'hub': Channel.objects.get(**kwargs).hub.id})
        hardware_ios = Channel.objects.get(**kwargs).hardwareio_set.all()

        channel = Channel.objects.get(**kwargs)

        channel_form = ChannelForm(Channel.objects.get(**kwargs).hardware.type, instance=channel)
        if request.accepted_renderer.format == 'html':
            return Response(
                {"channel_form": channel_form, "channel": channel, 'hardware_io_type_form': hardware_io_type_form,
                 'hardware_ios': hardware_ios},
                template_name='channel.html')
        else:
            return super(ChannelViewSet, self).retrieve()

    def listIO(self, channel_id):
        print('list io')
        hardware_ios = Channel.objects.get(pk=channel_id).hardwareio_set.all()
        serialized_hardware_ios = HardwareIOSerializer(many=True).to_representation(hardware_ios)

        return JsonResponse(serialized_hardware_ios, status=200, safe=False)

    def updateChannel(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "PATCH":
            # get the form data
            form = ChannelForm(instance=Channel.objects.get(pk=QueryDict(request.body)['id']),
                               data=QueryDict(request.body))

            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def deleteChannel(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "DELETE":
            # get the form data
            form = ChannelForm(instance=Channel.objects.get(pk=QueryDict(request.body)['id']),
                               data=QueryDict(request.body))
            channel = Channel.objects.get(
                pk=QueryDict(request.body)['id'])  # save the data and after fetch the object in instance
            channel.delete()

            return HttpResponse(render(request, 'accessories.html'))


class HubViewSet(viewsets.ModelViewSet):
    queryset = Hub.objects.all()
    serializer_class = HubSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def listHubHardware(self, hub_id):
        hardware = Hub.objects.get(pk=hub_id).hardware_set.all()
        serialized_hardware = HardwareSerializer().to_json_array(hardware)
        return JsonResponse(serialized_hardware, status=200, safe=False)

    def listHubChannels(self, hub_id):
        channels = Hub.objects.get(pk=hub_id).channel_set.all()
        serialized_channels = ChannelSerializer(many=True).to_representation(channels)
        return JsonResponse(serialized_channels, status=200, safe=False)

    def listHubAccessories(self, hub_id):
        accessories = Hub.objects.get(pk=hub_id).accessory_set.all()
        serialized_accessories = AccessorySerializer(many=True).to_representation(accessories)
        return JsonResponse(serialized_accessories, status=200, safe=False)

    def about(self, *args, **kwargs):
        api_about = {}
        api_about['isAPI'] = True
        return JsonResponse(api_about, status=200, safe=False)

    def list(self, request, *args, **kwargs):
        print('list')
        response = super(HubViewSet, self).list(request, *args, **kwargs)
        form = HubForm()
        hubs = Hub.objects.all()
        if request.accepted_renderer.format == 'html':
            return Response({"form": form, "hubs": hubs}, template_name='hubs.html')
        return response

    @csrf_exempt
    def retrieve(self, request, *args, **kwargs):

        if request.accepted_renderer.format == 'html':
            print('retrieve')
            print(str(request.path_info))
            hub = Hub.objects.get(**kwargs)
            hub_form = HubForm(instance=hub)

            # accessories_form = AccessoryForm()
            # channel_form = ChannelForm(Hub.objects.get(**kwargs).channel_set.type, instance=channel)
            return Response(
                {"channel_form": hub_form},
                template_name='hub.html')
        else:
            hub = Hub.objects.get(**kwargs)
            hub_data = HubSerializer(instance=hub).to_representation(hub)
            return JsonResponse(hub_data, status=200)


    def postHub( request):
        # request should be ajax and method should be POST.
        if request.is_ajax() and request.method == "POST":
            # get the form data
            form = HubForm(request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)
        elif request.method == "POST":
            import json
            body_json = json.loads(request.body.decode('utf-8'))
            hub = Hub()
            hub.id = body_json['id']
            hub.ip = body_json['ip']
            hub.display_name = body_json['display_name']
            hub.aid = body_json['aid']
            hub.save()
            ser_instance = django_serializers.serialize('json', [hub, ])

            return JsonResponse({"instance": ser_instance}, status=200)

        # some error occured
        return JsonResponse({"error": ""}, status=400)


def index(request):
    context = {'title': 'HomeHub'}
    return render(request, 'home.html', context)


#


class IOViewSet(viewsets.ModelViewSet):
    queryset = HardwareIO.objects.all()
    serializer_class = HardwareIOSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def retrieve(self, request, *args, **kwargs):
        print('retrieve')
        print(str(request.path_info))
        hardware_io_type = HardwareIO.objects.get(**kwargs).type
        instance = HardwareIO.objects.get(**kwargs)
        if hardware_io_type == SPI:
            hardware_form = SPIIoForm(instance=instance)
        if hardware_io_type == Serial:
            hardware_form = SerialIoForm(instance=instance)
        if hardware_io_type == PWM:
            hardware_form = PwmIoForm(instance=instance)
        if hardware_io_type == I2C:
            hardware_form = I2cIoForm(instance=instance)
        if hardware_io_type == DeviceFile:
            hardware_form = DeviceFileIoForm(instance=instance)
        if hardware_io_type == MCPChannel:
            hardware_form = MCPAnalogIoForm(instance=instance)
        if hardware_io_type == PiPicoAnalog:
            hardware_form = PiPicoAnalogIoForm(instance=instance)
        if hardware_io_type == PiGPIO:
            hardware_form = PiGpioForm(instance=instance)

        if request.accepted_renderer.format == 'html':
            return Response(
                {"hardware_io_form": hardware_form},
                template_name='io.html')
        else:
            return super(IOViewSet, self).retrieve()

    def updateIO(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "PATCH":
            # get the form data
            form = HardwareIoForm(instance=Channel.objects.get(pk=QueryDict(request.body)['id']),
                                  data=QueryDict(request.body))

            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                print(str(instance))
                # serialize in new friend object in json
                ser_instance = django_serializers.serialize('json', [instance, ])
                print(str(ser_instance))
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)

    def deleteIO(request):
        # request should be ajax and method should be POST.
        if request.is_ajax and request.method == "DELETE":
            # get the form data
            form = HardwareIoForm(instance=HardwareIO.objects.get(pk=QueryDict(request.body)['id']),
                                  data=QueryDict(request.body))
            hardware_io = HardwareIO.objects.get(
                pk=QueryDict(request.body)['id'])  # save the data and after fetch the object in instance
            hardware_io.delete()

            return HttpResponse(render(request, 'accessories.html'))


def video_streams(request):
    return render(request, "streams.html", None)