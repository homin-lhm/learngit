import unittest
import random
import string
import time
from copy import deepcopy
from common.read_yaml import ReadYaml
from business.v3_note_api import V3NoteApi
from common.unittest_report_logs import info_log, error_log


class V3ApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        data = ReadYaml("base_config.yml").get_yaml_data()  # 读取数据
        cls.sid1 = data["sid1"]
        cls.userId1 = data["userId1"]
        cls.host = data["host"]
        cls.v3_note_api = V3NoteApi()

        # 请求demo
        cls.register_base = {
            "identify_info": {
                "app_id": "wps-office",
                "user_id": "11",
                "device_id": "device_id",
                "device_name": "device_id"
            },
            "ability_info": [{"version": 1, "action": "transfer_helper"}],
            "client_info": {"type": "wps-pc", "version": "13.0", "channel": "0000.0000"},
            "additional_info": {"roaming_device_id": ""},
            "ext": "",
            "net_info": {"type": "有线网络", "ip": "192.168.12.34", "ports": [3001, 3002], "gateway": "0.0.0.0" },
            "os_info": {"branch": "pc", "level": "", "type": "windows 10", "brand": "pc", "model": "YAL-AL00"}
        }

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testGetNotes(self):
        info_log("获取首页便签列表")
        start_index = "0"
        rows = "50"
        res = self.v3_note_api.get_notesvr_user_home_startindex_rows_notes(self.host, self.sid1, self.userId1, start_index, rows)
        self.assertEqual(200, res.status_code)
        self.assertEqual([], res.json()["webNotes"])

        note_id = "".join(random.sample(string.ascii_letters + string.digits, 32))

        info_log("上传便签信息主体")
        body = {
            "noteId": note_id,
            "star": 0,
            "remindTime": 0,
            "remindType": 0
        }
        res = self.v3_note_api.post_notesvr_set_noteinfo(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)
        self.assertTrue("infoVersion" in res.json().keys())
        infoVersion = res.json()["infoVersion"]

        info_log("上传/更新便签内容")
        body = {
            "title": "WZWsi7mvYPwPpkoEGtDKkA==",
            "summary": "Lu+Q4WSUN4bz21lYcf0ELyeb4atUMU1/4a/RZESeBog=",
            "body": "+hnQTX1CV6UoBQKumuk0Uh7Jx19D9m26Dq7mSnQzBN8=",
            "localContentVersion": infoVersion,
            "noteId": note_id,
            "thumbnail": None,
            "bodyType": 0
        }
        res = self.v3_note_api.post_notesvr_set_notecontent(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)
        self.assertTrue("contentUpdateTime" in res.json().keys())

        info_log("获取便签内容")
        body = {
            "noteIds": [note_id]
        }
        res = self.v3_note_api.post_notesvr_get_notebody(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)
        self.assertEqual(note_id, res.json()["noteBodies"][0]["noteId"])

        info_log("删除便签")
        body = {
            "noteId": note_id
        }
        res = self.v3_note_api.post_notesvr_delete(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)

        note_group = "".join(random.sample(string.ascii_letters + string.digits, 32))
        info_log("新增分组")
        body = {
            "groupName": "TESTER_GROUP",
            "groupId": note_group,
            "isNewGroup": True
        }
        res = self.v3_note_api.post_notesvr_set_notegroup(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)

        info_log("获取分组列表")
        body = {
            "lastRequestTime": 0,
            "excludeInValid": True
        }
        res = self.v3_note_api.post_notesvr_get_notegroup(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)
        self.assertEqual(str(self.userId1), res.json()["noteGroups"][0]["userId"])

        info_log("查看分组下便签")
        body = {
            "rows": 50,
            "startIndex": 0,
            "groupId": note_group
        }
        res = self.v3_note_api.post_notesvr_web_getnotes_group(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)

        info_log("删除分组")
        body = {
            "groupId": note_group
        }
        res = self.v3_note_api.post_notesvr_get_notegroup(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)

        info_log("查看日历下便签")
        body = {
            "rows": 300,
            "startIndex": 0,
            "month": "2022/01",
            "remindStartTime": 1640966400000,
            "remindEndTime": 1643644800000
        }
        res = self.v3_note_api.post_notesvr_get_notegroup(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)

        info_log("查看回收站下便签列表")
        start_index = "0"
        rows = "50"
        res = self.v3_note_api.get_notesvr_user_invalid_startindex_rows_notes(self.host, self.sid1, self.userId1, start_index, rows)
        self.assertEqual(200, res.status_code)

        info_log("恢复回收站便签")
        body = {
            "noteIds": [note_id],
            "userId": self.userId1
        }
        res = self.v3_note_api.patch_notesvr_user_notes(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)

        info_log("删除/清空回收站便签")
        body = {
            "noteIds": ["-1"]
        }
        res = self.v3_note_api.post_notesvr_cleanrecyclebin(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)

        info_log("【后置】删除便签")
        body = {
            "noteId": note_id
        }
        res = self.v3_note_api.post_notesvr_delete(self.host, self.sid1, self.userId1, body)
        self.assertEqual(200, res.status_code)
