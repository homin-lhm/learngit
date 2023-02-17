import requests
import hashlib
import base64
import json


class GetMd5Content(object):
    def get_md5_content(self, content_type, date, accessID, secretKey, body):
        # md5
        get_md5_data = hashlib.md5()
        get_md5_data.update(body.encode("utf-8"))
        # base64
        base64_md5_data = str(base64.b64encode(get_md5_data.digest()), "utf-8")
        # 组合字符串
        sigature = secretKey + str(base64_md5_data) + content_type + date
        # sha1
        sha = hashlib.sha1(sigature.encode("utf-8"))
        # hex
        encrypts = sha.hexdigest()
        # Authorization create
        Authorization = str(accessID) + ":" + str(encrypts)
        return base64_md5_data, Authorization

    def get_md5_content_v2(self, content_type, date, accessID, secretKey, body):
        # md5
        get_md5_data = hashlib.md5()
        get_md5_data.update(body.encode("utf-8"))
        # base64
        base64_md5_data = str(base64.b64encode(get_md5_data.digest()), "utf-8")
        # 组合字符串
        sigature = secretKey + str(base64_md5_data) + content_type + date
        # sha1
        sha = hashlib.sha1(sigature.encode("utf-8"))
        # hex
        encrypts = sha.hexdigest()
        # Authorization create
        Authorization = "WPS-2:" + str(accessID) + ":" + str(encrypts)
        return base64_md5_data, Authorization


if __name__ == '__main__':
    pass