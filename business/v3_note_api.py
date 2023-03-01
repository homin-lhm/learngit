import requests
import json
from common.unittest_report_logs import info_log


class V3NoteApi(object):

    @staticmethod
    def get_notesvr_user_home_startindex_rows_notes(host, sid, user_id, start_index, rows):
        """获取首页便签列表"""
        path = "/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes".format(user_id, start_index, rows)
        url = host + path
        headers = {
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        res = requests.get(url=url, headers=headers)

        return res

    @staticmethod
    def post_notesvr_set_noteinfo(host, sid, user_id, body):
        """上传便签信息主体"""
        path = "/v3/notesvr/set/noteinfo"
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        return res

    @staticmethod
    def post_notesvr_set_notecontent(host, sid, user_id, body):
        """上传便签内容"""
        path = "/v3/notesvr/set/notecontent"
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        return res

    @staticmethod
    def post_notesvr_get_notebody(host, sid, user_id, body):
        """获取便签内容"""
        path = "/v3/notesvr/get/notebody"
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        return res

    @staticmethod
    def post_notesvr_delete(host, sid, user_id, body):
        """删除便签"""
        path = "/v3/notesvr/delete"
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        return res

    @staticmethod
    def post_notesvr_get_notegroup(host, sid, user_id, body):
        """获取分组列表"""
        path = "/v3/notesvr/get/notegroup"
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        return res

    @staticmethod
    def post_notesvr_set_notegroup(host, sid, user_id, body):
        """新增分组"""
        path = "/v3/notesvr/set/notegroup"
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        return res

    @staticmethod
    def post_notesvr_delete_notegroup(host, sid, user_id, body):
        """删除分组"""
        path = "/v3/notesvr/delete/notegroup"
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        return res

    @staticmethod
    def post_notesvr_web_getnotes_group(host, sid, user_id, body):
        """查看分组下便签"""
        path = "/v3/notesvr/web/getnotes/group"
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        return res

    @staticmethod
    def post_notesvr_web_getnotes_remind(host, sid, user_id, body):
        """查看日历下便签"""
        path = "/v3/notesvr/web/getnotes/remind"
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        return res

    @staticmethod
    def get_notesvr_user_invalid_startindex_rows_notes(host, sid, user_id, start_index, rows):
        """查看回收站下便签列表"""
        path = "/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes".format(user_id, start_index, rows)
        url = host + path
        headers = {
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        res = requests.get(url=url, headers=headers)

        return res

    @staticmethod
    def patch_notesvr_user_notes(host, sid, user_id, body):
        """回复回收站的便签"""
        path = "/v3/notesvr/user/{}/notes".format(user_id)
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.patch(url=url, headers=headers, data=json.dumps(body))

        return res

    @staticmethod
    def post_notesvr_cleanrecyclebin(host, sid, user_id, body):
        """删除/清空回收站便签"""
        path = "/v3/notesvr/cleanrecyclebin"
        url = host + path
        headers = {
            'Content-Type': 'application/json',
            'x-user-key': str(user_id),
            'cookie': 'wps_sid={}'.format(sid)
        }
        info_log("url: {}".format(url))
        info_log("headers: {}".format(json.dumps(headers)))
        info_log("body: {}".format(json.dumps(body)))
        res = requests.post(url=url, headers=headers, data=json.dumps(body))

        return res
