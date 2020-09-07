#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import re

from server.webservice.EndPoints.PoolType import PoolType


class EndPointRegister:
    _instance = None

    endpoint_register_put = [
        # /slots/{id}?activate_device
        {
            '^/slots/(?P<dut_id>[0-9]+)\?activate_device=(?P<activate_device>[0-9]+)$': "ActivateDevice",
            "pool": PoolType.OUT_OF_ORDER
        },
        # /slots/{id}?reserve
        {
            '^/slots/(?P<dut_id>[0-9]+)\?reserve$': "ReserveSlot",
            "pool": PoolType.OUT_OF_ORDER
        },
        # /slots/{id}?reserve&activate_device
        {
            '^/slots/(?P<dut_id>[0-9]+)\?reserve&activate_device=(?P<activate_device>[0-9]+)$': "ReserveSlot",
            "pool": PoolType.OUT_OF_ORDER
        },
        # /slots/{id}?reserve&soft_reserve
        {
            '^/slots/(?P<dut_id>[0-9]+)\?reserve&soft_reserve=(?P<soft_reserve>true|false)$': "ReserveSlot",
            "pool": PoolType.OUT_OF_ORDER
        },
        # /slots/{id}?reserve&activate_device&soft_reserve
        {
            '^/slots/(?P<dut_id>[0-9]+)\?reserve&activate_device=(?P<activate_device>[0-9]+)&'
            'soft_reserve=(?P<soft_reserve>true|false)$': "ReserveSlot",
            "pool": PoolType.OUT_OF_ORDER
        },
        # /slots/{id}?reserve&activate_device&soft_reserve
        {
            '^/slots/(?P<dut_id>[0-9]+)\?reserve&soft_reserve=(?P<soft_reserve>true|false)&a'
            'ctivate_device=(?P<activate_device>[0-9]+)$': "ReserveSlot",
            "pool": PoolType.OUT_OF_ORDER
        },
        # /sots/{id}?release
        {
            '^/slots/(?P<dut_id>[0-9]+)\?release$': "ReleaseSlot",
            "pool": PoolType.OUT_OF_ORDER
        },
        # /slots/{id}?kill
        {
            '^/slots/(?P<dut_id>[0-9]+)\?kill$': "KillSlot",
            "pool": PoolType.OUT_OF_ORDER
        },
        # Changed from DUT to OUT_OF_ORDER for executing kill on Slots during execution.
        # /slots/{id}?restart
        {
            '^/slot/(?P<dut_id>[0-9]+)\?restart$': "RestartSlot",
            'pool': PoolType.OUT_OF_ORDER
        },
        # /slots/{id}?reset
        {
            '^/slots/(?P<dut_id>[0-9]+)\?reset$': "Reset",
            'pool': PoolType.DUT
        },
        # /slots/{id}/dut
        {
            '^/dut/(?P<dut_id>[0-9]+)/dut\?device_id=(?P<device_id>[0-9]+)$': "UpdateDUT",
            'pool': PoolType.DUT
        },
        # /slots/{id}/dut?getString
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?get_string$": "GetString",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?validateImage
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?validateImage$": "ValidateImage",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?validateImage
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?validate_image$": "ValidateImage",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?waitForAction
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?waitForAction$": "WaitForAction",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?wait_for_action$": "WaitForAction",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?wait_for_action&(?P<start_timer>start_timer)$": "WaitForAction",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?wait_for_action&(?P<stop_timer>stop_timer)$": "WaitForAction",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?startTimer
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?startTimer$": "StartTimer",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?stopTimer
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?stopTimer": "StopTimer",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?vqa
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?vqa": "VQA",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?powerState&state=on|off
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?powerState&state=(?P<state>on|off)$": "PowerState",
            "pool": PoolType.OUT_OF_ORDER},
        # /slots/{id}/dut?recording&action=start|stop|transfer
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?recording&action=(?P<action>start|stop|transfer)$": "Recording",
            "pool": PoolType.DUT},  # Moved Recording from OUT_OF_ORDER to DUT pool
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?recording&state=(?P<action>on|off|transfer)&"
            "filename=(?P<filename>[a-z,A-Z,0-9,_,-]+)$": "RecordingOldJavaClient",
            "pool": PoolType.DUT
        },
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?recording&state=(?P<action>on|off|transfer)&"
            "filename=(?P<filename>[a-z,A-Z,0-9,_,-]+)&stream=(?P<stream>[a-z,A-Z,0-9,_,-]+)$": "RecordingOldJavaClient",
            "pool": PoolType.DUT
        },
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?recording&state=(?P<action>on|off|transfer)&"
            "filename=(?P<filename>[a-z,A-Z,0-9,_,-]+)&"
            "directory_name=(?P<directory_name>[a-z,A-Z,0-9,_,-]+)$": "RecordingOldJavaClient",
            "pool": PoolType.DUT
        },
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?recording&state=(?P<action>off)&"
            "directory_name=(?P<directory_name>[a-z,A-Z,0-9,_,-]+)$": "RecordingOldJavaClient",
            "pool": PoolType.DUT
        },
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?recording&state=(?P<action>off|transfer)$": "RecordingOldJavaClient",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?stream&action=start|stop
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?stream&action=(?P<action>start|stop|kill)$": "Streaming",
            "pool": PoolType.OUT_OF_ORDER},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?stream=&action=(?P<action>start|stop|kill)$": "Streaming",
            "pool": PoolType.OUT_OF_ORDER},
        # /slots/{id}/dut?sendKey={key}
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?send_key=(?P<sendKey>[a-z,A-Z,0-9,_,-]+)$": "SendKey",
            "pool": PoolType.DUT},
        # /remotes/{id}
        {
            "^/remotes/(?P<remote_id>[0-9]+)$": "ModifyRemote",
            "pool": PoolType.MANAGEMENT_POOL},
        # /service?stop
        {
            "^/service\?stop": "StopService",
            "pool": PoolType.MANAGEMENT_POOL},
        # /service?reset_nic
        {
            "^/service\?reset_nic": "ResetNIC",
            "pool": PoolType.MANAGEMENT_POOL},
        # /dut/{id}/connect
        {
            "^/slots/(?P<dut_id>[0-9]+)\?connect$": "Connect",
            "pool": PoolType.DUT},
        # /dut/{id}/disconnect
        {
            "^/slots/(?P<dut_id>[0-9]+)\?disconnect$": "Disconnect",
            "pool": PoolType.DUT},
        # /dut/{id}/rf4cCommand
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?rf4ce_command=(?P<rf4ce_command>.+)$": "SendVoiceCommand",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?kpi&action=start|stop.
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?kpi&action=(?P<action>start|stop)$": "RawVideoRecording",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?matchFrame&action=first|last
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?matchFrame&action=(?P<action>first|last)$": "MatchFrame",
            "pool": PoolType.DUT},
        # /slots/{id}?killStreaming
        {
            "^/slots/(?P<dut_id>[0-9]+)\?killStreaming$": "KillStreaming",
            "pool": PoolType.OUT_OF_ORDER},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?thirdeye_sdo": "Condition",
            "pool": PoolType.DUT},
        # /slots/{id}?health
        {
            '^/slots/(?P<dut_id>[0-9]+)\?health=(?P<health>working|faulty)$': "Health",
            "pool": PoolType.OUT_OF_ORDER
        }
    ]

    endpoint_register_get = [
        # /slots
        {
            "^/slots$": "Slots",
            "pool": PoolType.MANAGEMENT_POOL},
        # /slots/{id}
        {
            "^/slots/(?P<dut_id>[0-9]+)$": "SlotID",
            "pool": PoolType.MANAGEMENT_POOL},
        # /slots/{id}?frameRate
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?frameRate$": "Framerate",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?frame_rate$": "Framerate",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?resolution
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?resolution$": "Resolution",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?image
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?image&image_quality=(?P<image_quality>[0-9]+)$": "Image",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?image&image_quality=(?P<image_quality>[0-9]+)&region_name=(?P<region_name>[a-z,A-Z,0-9,_,-]+)$": "Image",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?powerState
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?powerState$": "PowerState",
            "pool": PoolType.OUT_OF_ORDER},
        # /slots/{id}/dut?detectMotion&regionName={regionName}&timeout={timeOut}&threshold={percent}
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?detectMotion&regionName=(?P<region_name>[a-z,A-Z,0-9,_,-]+)&timeout=(?P<timeout>[0-9]+)&threshold=(?P<threshold>[0-9]+)": "DetectMotion",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?validate_motion&region_name=(?P<region_name>[a-z,A-Z,0-9,_,-]*)&timeout=(?P<timeout>[0-9]+)&threshold=(?P<threshold>[0-9]+)": "DetectMotion",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?validate_motion&region_name=&timeout=(?P<timeout>[0-9]+)&threshold=(?P<threshold>[0-9]+)": "DetectMotion",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?validate_motion&region_name&timeout=(?P<timeout>[0-9]+)&threshold=(?P<threshold>[0-9]+)": "DetectMotion",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?validateAudio&timeout={timeOut}
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?validateAudio&timeout=(?P<timeout>[0-9]+)": "DetectAudio",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?validate_audio&timeout=(?P<timeout>[0-9]+)": "DetectAudio",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?validate_audio&threshold=(?P<threshold>[0-9,-]*)&timeout=(?P<timeout>[0-9]+)": "DetectAudio",
            "pool": PoolType.DUT},  # TODO: added for 1.0
        # /remotes
        {
            "^/remotes$": "RemotesList",
            "pool": PoolType.MANAGEMENT_POOL},
        # /remotes/{id}
        {
            "^/remotes/(?P<remote_id>[0-9]+)$": "Remotes",
            "pool": PoolType.MANAGEMENT_POOL},
        # /remotes/{id}?keys
        {
            "^/remotes/(?P<remote_id>[0-9]+)\?keys$": "RemotesKeyList",
            "pool": PoolType.MANAGEMENT_POOL},
        # /irdb
        {
            "^/irdb$": "IRDB",
            "pool": PoolType.MANAGEMENT_POOL},
        # /irdb/?keys
        {
            "^/irdb\?keys$": "IRDB",
            "pool": PoolType.MANAGEMENT_POOL},
        # /irdb/{id}
        {
            "^/irdb/(?P<irdb_id>[0-9]+)$": "IRDBID",
            "pool": PoolType.MANAGEMENT_POOL},
        # /controllers
        {
            "^/controllers$": "ControllerList",
            "pool": PoolType.MANAGEMENT_POOL},
        # /resources/images & /resources/images?startswith should both point to same handler
        # it is easier and more readable to make 2 regular expressions instead of one
        {
            "^/resources/images$": "ResourceImage",
            "pool": PoolType.MANAGEMENT_POOL},
        # starts with has multiple optional parameters and therefore $ is not applied at the end
        {
            "^/resources/images\?startswith=(?P<startswith>[a-z,A-Z,0-9,_,-]+)$": "ResourceImage",
            "pool": PoolType.MANAGEMENT_POOL},
        {
            "^/resources/images\?startswith=(?P<startswith>[a-z,A-Z,0-9,_,-]+)&limit=(?P<limit>[0-9]+)&offset=(?P<offset>[0-9]+)": "ResourceImage",
            "pool": PoolType.MANAGEMENT_POOL},
        # /resources/images?imageName={imageName}
        # Only A-Z, a-z, 0-9, _ and - allowed in name
        {
            "^/resources/images\?image_name=(?P<image_name>[a-z,A-Z,0-9,_,-]+)$": "ResourceImage",
            "pool": PoolType.MANAGEMENT_POOL},
        {
            "^/resources/images\?offset=(?P<offset>[a-z,A-Z,0-9,_,-]*)&limit=(?P<limit>[0-9]*)$": "ResourceImageList",
            "pool": PoolType.MANAGEMENT_POOL},
        # /resources/regions & /resources/regions?startswith should both point to same handler
        # it is easier and more readable to make 2 regular expressions instead of one
        {
            "^/resources/regions$": "Region",
            "pool": PoolType.MANAGEMENT_POOL},
        {
            "^/resources/regions\?startswith=(?P<startswith>[a-z,A-Z,0-9,_,-]+)$": "Region",
            "pool": PoolType.MANAGEMENT_POOL},
        {
            "^/resources/regions\?region_name=(?P<region_name>[a-z,A-Z,0-9,_,-]+)$": "Region",
            "pool": PoolType.MANAGEMENT_POOL},
        {
            "^/resources/regions\?offset=(?P<offset>[0-9]*)&limit=(?P<limit>[0-9]*)$": "ResourceRegion",
            "pool": PoolType.MANAGEMENT_POOL},
        {
            "^/resources/regions\?startswith=(?P<startswith>[a-z,A-Z,0-9,_,-]*)&offset=(?P<offset>[0-9]*)&limit=(?P<limit>[0-9]*)$": "ResourceRegion",
            "pool": PoolType.MANAGEMENT_POOL},
        # /resources/regions?regionName={regionName}
        # Only A-Z, a-z, 0-9, _ and - allowed in name
        {
            "^/resources/regions\?regionName=(?P<region_name>[a-z,A-Z,0-9,_,-]+)$": "Region",
            "pool": PoolType.MANAGEMENT_POOL},
        # /slots/{id}/dut?validateLanguage&string={string}
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?detectLanguage&string=(?P<string>.+)": "DetectLanguage",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?detectLanguage=&string=(?P<string>.+)": "DetectLanguage",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?condition": "Condition",
            "pool": PoolType.DUT},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?thirdeye_sdo": "Condition",
            "pool": PoolType.DUT},
        # /slots/{id}/dut?filters
        {
            "^/filters?": "Filters",
            "pool": PoolType.MANAGEMENT_POOL}
    ]

    endpoint_register_post = [
        # /slots/{id}/dut?device_id=1
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?device_id=(?P<device_id>[0-9]+)$": "AddDUT",
            "pool": PoolType.MANAGEMENT_POOL},
        # /remotes
        {
            "^/remotes$": "AddRemote",
            "pool": PoolType.MANAGEMENT_POOL},
        # /remotes/{id}
        {
            "^/remotes/(?P<remote_id>[0-9]+)$": "AddRemote",
            "pool": PoolType.MANAGEMENT_POOL},
        # /remotes/{id}?keys
        {
            "^/remotes/(?P<remote_id>[0-9]+)\?keys$": "RemoteKeys",
            "pool": PoolType.MANAGEMENT_POOL},
        # /resources/images?imageName={imageName}
        # Only A-Z, a-z, 0-9, _ and - allowed in name
        {
            "^/resources/images\?imageName=(?P<image_name>[a-z,A-Z,0-9,_,-]+)$": "SaveImage",
            "pool": PoolType.MANAGEMENT_POOL},
        {
            "^/resources/images/ext$": "SaveImageFromExternalScreen",
            "pool": PoolType.MANAGEMENT_POOL},
        # /resources/regions?regionName={regionName}
        # Only A-Z, a-z, 0-9, _ and - allowed in name
        {
            "^/resources/regions\?regionName=(?P<region_name>[a-z,A-Z,0-9,_,-]+)$": "SaveRegion",
            "pool": PoolType.MANAGEMENT_POOL},
        {
            "^/resources/regions$": "SaveRegion",
            "pool": PoolType.MANAGEMENT_POOL}
    ]

    endpoint_register_delete = [
        # /slots/{id}/dut
        # {"^/slots/(?P<dut_id>[0-9]+)/dut$": DeleteDUT, "pool": PoolType.MANAGEMENT_POOL},
        {
            "^/slots/(?P<dut_id>[0-9]+)/dut\?device_id=(?P<device_id>[0-9]+)$": "DeleteDUT",
            "pool": PoolType.MANAGEMENT_POOL},
        # /remotes/{id}
        {
            "^/remotes/(?P<remote_id>[0-9]+)$": "DeleteRemote",
            "pool": PoolType.MANAGEMENT_POOL},
        # /remotes/{id}?keys
        {
            "^/remotes/(?P<remote_id>[0-9]+)\?keys=(?P<keys>true)$": "DeleteRemote",
            "pool": PoolType.MANAGEMENT_POOL},
        # /resources/images
        {
            "^/resources/images\?image_name=(?P<image_name>[a-z,A-Z,0-9,_,-]+)$": "DeleteImage",
            "pool": PoolType.MANAGEMENT_POOL},
        # /resources/regions
        {
            "^/resources/regions\?region_name=(?P<region_name>[a-z,A-Z,0-9,_,-]+)$": "DeleteRegion",
            "pool": PoolType.MANAGEMENT_POOL}
    ]

    @staticmethod
    def getInstance():
        """ Static access method. """
        if EndPointRegister._instance is None:
            EndPointRegister()
        return EndPointRegister._instance

    # def __init__(self):
    #     self._service_dict_get = dict(EndPointRegister.endpoint_register_get)
    #     self._service_dict_put = dict(EndPointRegister.endpoint_register_put)
    #     self._service_dict_delete = dict(EndPointRegister.endpoint_register_delete)
    #     self._service_dict_post = dict(EndPointRegister.endpoint_register_post)

    @staticmethod
    def get_put_service(url):
        url = url.split('?tempval=', 1)[0]
        url = url.split('&tempval=', 1)[0]
        return EndPointRegister._get_service(EndPointRegister.endpoint_register_put, url)

    @staticmethod
    def get_get_service(url):
        url = url.split('?tempval=', 1)[0]
        url = url.split('&tempval=', 1)[0]
        return EndPointRegister._get_service(EndPointRegister.endpoint_register_get, url)

    @staticmethod
    def get_post_service(url):
        url = url.split('?tempval=', 1)[0]
        url = url.split('&tempval=', 1)[0]
        return EndPointRegister._get_service(EndPointRegister.endpoint_register_post, url)

    @staticmethod
    def get_delete_service(url):
        url = url.split('?tempval=', 1)[0]
        url = url.split('&tempval=', 1)[0]
        return EndPointRegister._get_service(EndPointRegister.endpoint_register_delete, url)

    @staticmethod
    def _get_service(service_register, url):
        for service in service_register:
            for key, value in service.items():
                # value = service_register[key]
                m = re.match(key, url)
                pool = service["pool"]
                if m is not None:
                    return value, m.groupdict(), pool
        return None, None, None
