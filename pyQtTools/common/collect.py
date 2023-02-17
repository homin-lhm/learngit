import requests
import json
import base64
from common.getMd5Content import GetMd5Content


class Collect(object):

    def api_v1_userdatachange(self, file_type, user_id, accessID, SecretKey, device_id, device_name, request_channel):
        """collect对外接口"""
        body = {
            "topic": "wps.file",
            "type": file_type,  # "file_create"、"file_update"
            "sub_tag": "",
            "operator": user_id,
            "operator_info": {
                "id": user_id,
                "name": "减肥",
                "avatar": "https://imagebucket.test.wpscdn.cn/238777393_ace4b47c23166e1025d46ce8c7f1812a?imageMogr2/thumbnail/180x180!",
                "corpid": 0
            },
            "time": 1646128356,
            "fileinfo": {
                "fileid": 123,
                "last_update_userid": 238777393,
                "groupid": 334866976,
                "group_type": "special",
                "group_name": "我的云文档",
                "corpid": 0,
                "parentid": 100004602464,
                "fname": "111test(84).zip",
                "fsize": 18925796,
                "ftype": "file",
                "fver": 1,
                "ctime": 1646128356,
                "mtime": 1646128356
            },
            "creator": {
                "id": user_id,
                "name": "减肥",
                "avatar": "https://imagebucket.test.wpscdn.cn/238777393_ace4b47c23166e1025d46ce8c7f1812a?imageMogr2/thumbnail/180x180!",
                "corpid": 0
            },
            "device_info": {
                "deviceid": device_id,
                "device_name": device_name,
                "request_channel": request_channel
            },
            "parent_name": ""
        }

        if device_id is None:
            body["device_info"].pop("deviceid")
            body["device_info"].pop("device_name")
        if request_channel is None:
            body["device_info"].pop("request_channel")

        print(body)

        content_type = "application/json"
        date = "Fri, 08 Oct 2021 15:30:21 CST"
        content_md5, Authorization = GetMd5Content().get_md5_content(content_type, date, accessID,
                                                                     SecretKey, json.dumps(body))
        headers = {
            'date': date,
            'Content-Md5': content_md5,
            'Authorization': Authorization,
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip, deflate'
        }
        response = requests.post(url="http://collect-cloudnotify.wps.cn/api/v1/userdatachange", headers=headers,
                                 data=json.dumps(body))
        return response

    def searchtag_taginfo_v1_taginfo(self, accessID, secretKey, sid):
        url = "https://cloudnotify.wps.cn/searchtag/taginfo/v1/taginfo?tag=all"
        content_type = "application/json"
        date = "Fri, 08 Oct 2021 15:30:21 CST"
        content_md5, Authorization = GetMd5Content().get_md5_content_v2(content_type, date, accessID, secretKey, url)
        headers = {
            'date': date,
            'Content-Md5': content_md5,
            'Content-Type': 'application/json',
            'Authorization': Authorization,
            'cookie': 'wps_sid={}'.format(sid)
        }
        result = requests.get(url=url, headers=headers)
        return result
