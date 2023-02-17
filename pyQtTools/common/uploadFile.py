# -*- coding: utf-8 -*-
'''
Created by admin on 2019/4/1
'''
import hashlib
import json
import logging
import os
import string
import requests
# import urllib3.contrib.pyopenssl
import datetime
import random
# from logsdk import logsdk
import urllib3

urllib3.disable_warnings()
# urllib3.contrib.pyopenssl.inject_into_urllib3()
# logging = logsdk()
# logging.beforelog(path=os.getcwd()+'/../../robot_case/logs/rf1234.log')  # 在RF中就不要有这一行了，会影响其他的输出位置

class uploadFile:
    def getUserGroupId(self, host, sid):
        """
        通过用户sid获取该用户的云文档sid
        :param sid:
        :return:
        """
        cookies = dict(wps_sid=sid)
        resp = requests.get(host + "/api/v3/groups/special", cookies=cookies)
        return resp

    def qingDeviceFileCreate(self, host, deviceid, sid, file_name, sha1, size, etag):
        """
        在云文档中创建之前上传的文件
        :param group_id:
        :param parent_path:
        :param sid:
        :param file_name:
        :param size:
        :param sha1:
        :return:"http://qing.wps.cn"
        """
        cookies = dict(wps_sid=sid)
        create_api = host + "/api/v5/devices/files"
        # # print create_api
        contentType = "application/json"
        headers = {
            'Content-Type': contentType,
            "Origin": "https://drive.wps.cn"
        }
        data = {
            "deviceid": int(deviceid),
            "name": file_name,
            "size": size,
            "sha1": sha1,
            "store": "ks3",
            "unlimited_size": True
        }
        if etag is not None:
            data.update({"etag": str(etag)})

        resp = requests.post(url=create_api, data=json.dumps(data), cookies=cookies, headers=headers, verify=False)
        # print(resp.status_code)
        # print(resp.json())
        if resp.status_code != 200:
            logging.error("在云文档中创建之前上传的文件失败，失败原因: " + str(resp.content))
            raise RuntimeError("qingFileCreate: response error, status_code:%s, content:%s",
                               str(resp.status_code), str(resp.content))
        else:
            logging.info("在云文档中创建之前上传的文件成功")
            res = json.loads(resp.content)
            return res

        # 创建文件接口程序入口
    def create_deivce_file(self, sid, device_id, pdfpath):

        # 获取文件基本信息
        file_md5, size, file_type, file_name, file_data, file_singlename, sha1 = self.file_content(pdfpath)

        # 测试环境
        drive_host = "http://drive.wps.cn"
        qing_host = "http://qing.wps.cn"
        sid = sid
        csrf = "BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk"

        try:

            # # print('获取ks3上传链接')
            # 获取ks3上传链接
            resp = self.getUploadUrl(qing_host, sid, file_name, sha1, file_md5, size)

            # # print('ks3链接上传')
            # ks3链接上传
            resp = self.UploadFileToKS3(resp, pdfpath, size)
            etag = resp.headers["ETag"].strip('"')

            # # print('云文档创建对应文件')
            # 云文档创建对应文件
            fileInfo = self.qingDeviceFileCreate(qing_host, device_id, sid, file_name, sha1, size, etag)
            # print("qingFileCreate")
            # print(fileInfo)
            id = fileInfo.get("id")
            #
            # print('创建分享链接')

            # print("上传文件成功")
            return {'code': 200, 'message': '上传成功', "file_id": str(id), "size": size}
        except Exception as e:
            logging.error("上传云文档出错:%s" % e)
            return {'code': 400, 'message': e}

    def delete_file(self,host, sid, groupid, parent_id, file_id, csrf):
        """
        通过用户sid获取该用户的云文档sid
        :param sid:
        :return:
        """
        cookies = dict(wps_sid=sid, csrf=csrf)
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "csrfmiddlewaretoken": csrf
        }
        url = host + "/api/v3/groups/" + str(groupid) + "/files/" + str(parent_id)
        url = host + "/api/v3/groups/" + str(groupid)
        print (url)
        resp = requests.delete(url, cookies=cookies, headers=headers, data=json.dumps(data), verify=False)
        print (resp.status_code)
        print (resp.content)
        if resp.status_code != 200:
            logging.error("删除云文档文件失败，失败原因%s,file_id： %s,group_id: %s, parent_id: %s "  % (str(resp.content),str(file_id),str(groupid),str(parent_id)))
            raise RuntimeError("miniAppTools: get user groupid error, statusCode="
                               + str(resp.status_code) + ", response content =" + resp.content)
        else:
            logging.info("删除云文档文件成功,file_id： %s,group_id: %s, parent_id: %s"  % (str(file_id),str(groupid),str(parent_id)))
        res = json.loads(resp.content)
        result = res.get("result")
        # if not group_id:
        # logging.error("miniAppTools: get user groupid error, request params: sid: %s", sid)
        # raise RuntimeError("miniAppTools: get user groupid error, statusCode="
        #                    + str(resp.status_code) + ", response content =" + resp.content)
        return result

    def getUploadUrl(self,host, sid, file_name, sha1, md5, size):
        """
        获取云文档ks3上传链接
        :param sid: 用户sid
        :param group_id: 云文档圈子id
        :param file_path: 文件路径
        :return: 返回整个resp，沿用文洁的上传ks3逻辑
        """
        cookies = dict(wps_sid=sid)
        # print 'groupid'
        # print group_id
        contentType = "application/json"
        headers = {
            'Content-Type': contentType,
            "Origin": "https://drive.wps.cn"
        }
        data = {
            "unlimited_size": True,
            "name": file_name,
            "sha1": sha1,
            "md5": md5,
            "size": size,
            "store": "ks3"
        }
        resp = requests.post(host + "/api/files/upload/univ_request", data=json.dumps(data), cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            logging.error("获取云文档ks3上传链接，失败原因: " + str(resp.content))
            raise RuntimeError("getUploadUrl: response error, status_code:%s, content:%s",
                               str(resp.status_code), str(resp.content))
        else:
            logging.info("获取云文档ks3上传链接成功")
        return resp

    def UploadFileToKS3(self,response, filePath, size):
        """
        链接上传文件到ks3 基本不变
        :param response:
        :param filePath:
        :param size:
        :return:
        """
        dict_response = json.loads(response.content)
        uploadurl = dict_response["uploadinfo"]["put_auth"]["upload_url"]
        contentType = dict_response["uploadinfo"]["put_auth"]["content_type"]
        headers = dict_response["uploadinfo"]["headers"]
        headers["Content-Type"] = contentType
        headers["Content-Length"] = str(size)

        response2 = requests.request("PUT", uploadurl, headers=headers, data=open(filePath, 'rb'), verify=False)
        if response2.status_code != 200:
            logging.error("链接上传文件到ks3 失败，失败原因: " + str(response2.content))
            raise RuntimeError("UploadFileToKS3: response error, status_code:%s, content:%s",
                               str(response2.status_code), str(response2.content))
        else:
            logging.info("链接上传文件到ks3成功")
        return response2

    def qingFileCreate(self, host, group_id, parent_path, sid, file_name, sha1, size,etag):
        """
        在云文档中创建之前上传的文件
        :param group_id:
        :param parent_path:
        :param sid:
        :param file_name:
        :param size:
        :param sha1:
        :return:
        """
        cookies = dict(wps_sid=sid)
        create_api = host + "/api/v5/files/file"
        # print create_api
        contentType = "application/json"
        headers = {
            'Content-Type': contentType,
            "Origin": "https://drive.wps.cn"
        }
        data = {
            "groupid": int(group_id),
            "parentid": 0,
            "name": file_name,
            "size": size,
            "sha1": sha1,
            "parent_path": [str(parent_path)],
            "store": "ks3",
            "unlimited_size": True
        }
        if etag is not None:
            data.update({"etag": str(etag)})

        resp = requests.post(url=create_api, data=json.dumps(data), cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            logging.error("在云文档中创建之前上传的文件失败，失败原因: " + str(resp.content))
            raise RuntimeError("qingFileCreate: response error, status_code:%s, content:%s",
                               str(resp.status_code), str(resp.content))
        else:
            logging.info("在云文档中创建之前上传的文件成功")
            res = json.loads(resp.content)
            return res

    def qingFileCreate_parentid(self, host, group_id, parentid, sid, file_name, sha1, size,etag):
        """
        在云文档中创建之前上传的文件
        :param group_id:
        :param parent_path:
        :param sid:
        :param file_name:
        :param size:
        :param sha1:
        :return:
        """
        cookies = dict(wps_sid=sid)
        create_api = host + "/api/v5/files/file"
        # print create_api
        contentType = "application/json"
        headers = {
            'Content-Type': contentType,
            "Origin": "https://drive.wps.cn"
        }
        data = {
            "groupid": int(group_id),
            "parentid": parentid,
            "name": file_name,
            "size": size,
            "sha1": sha1,
            "store": "ks3",
            "unlimited_size": True
        }
        if etag is not None:
            data.update({"etag": str(etag)})

        resp = requests.post(url=create_api, data=json.dumps(data), cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            logging.error("在云文档中创建之前上传的文件失败，失败原因: " + str(resp.content))
            raise RuntimeError("qingFileCreate: response error, status_code:%s, content:%s",
                               str(resp.status_code), str(resp.content))
        else:
            logging.info("在云文档中创建之前上传的文件成功")
            res = json.loads(resp.content)
            return res

    def create_folder(self, sid, groupid, name):
        url = "http://drive.wps.cn/api/v5/files/folder"
        data = {"groupid": groupid, "name": name, "parentid": 0}
        cookies = dict(wps_sid=sid)
        headers = {
            'Content-Type': "application/json",
            "Origin": "https://drive.wps.cn"
        }
        resp = requests.post(url=url, data=json.dumps(data), cookies=cookies, headers=headers, verify=False)
        return resp

    def qingFileCreate_update_header(self, host, group_id, parent_path, sid, file_name, sha1, size, etag, update_headers):
        """
        在云文档中创建之前上传的文件
        :param group_id:
        :param parent_path:
        :param sid:
        :param file_name:
        :param size:
        :param sha1:
        :return:
        """
        cookies = dict(wps_sid=sid)
        create_api = host + "/api/v5/files/file"
        # print create_api
        contentType = "application/json"
        headers = {
            'Content-Type': contentType,
            "Origin": "https://drive.wps.cn"
        }
        if update_headers == {}:
            pass
        else:
            for k, v in update_headers.items():
                headers[k] = v
        print(headers)
        data = {
            "groupid": int(group_id),
            "parentid": 0,
            "name": file_name,
            "size": size,
            "sha1": sha1,
            "parent_path": [str(parent_path)],
            "store": "ks3",
            "unlimited_size": True
        }
        if etag is not None:
            data.update({"etag": str(etag)})

        resp = requests.post(url=create_api, data=json.dumps(data), cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            logging.error("在云文档中创建之前上传的文件失败，失败原因: " + str(resp.content))
            raise RuntimeError("qingFileCreate: response error, status_code:%s, content:%s",
                               str(resp.status_code), str(resp.content))
        else:
            logging.info("在云文档中创建之前上传的文件成功")
            res = json.loads(resp.content)
            return res

    def DeleteResultFile(self, cloud_file_groupid, cloud_file_id, sid):
        """
        删除云文档文件
        :param yunfile_groupid, yunfile_id, sid :
        :return:
        """
        # print("DeleteResultFile")
        deleteResultFileUrl = "http://drive.wps.cn/api/v3/groups/"+str(cloud_file_groupid)+"/files/"+str(cloud_file_id)
        cookies = dict(wps_sid=sid, csrf=sid)
        data = {
            "csrfmiddlewaretoken": sid
        }
        headers_ResultFile = {
            "Content-Type": "application/json"
        }
        response_deleteResultFile = requests.delete(url=deleteResultFileUrl, data=json.dumps(data),  headers=headers_ResultFile, cookies=cookies)
        return response_deleteResultFile

    def open_file(self,url, sid):
        """
        在云文档中创建之前上传的文件
        :param group_id:
        :param parent_path:
        :param sid:
        :param file_name:
        :param size:
        :param sha1:
        :return:
        """
        cookies = dict(wps_sid=sid)
        contentType = "application/json"
        headers = {
        }
        resp = requests.get(url=url, cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            logging.error("获取group_id值失败，失败原因: " + str(resp.content))
            raise RuntimeError("open_file: response error, status_code:%s, content:%s",
                               str(resp.status_code), str(resp.content))
        return resp

    def read_file(self,filepath):
        newfileArry = []
        filenames = os.listdir(filepath)
        count = 0
        for pdffile in filenames:
            count += 1
            if os.path.splitext(pdffile)[1] == '.pdf' or os.path.splitext(pdffile)[1] == '.rtf' or os.path.splitext(pdffile)[1] == ".txt" or os.path.splitext(pdffile)[1] == ".doc":
                pdffiles = os.path.realpath(os.path.join(filepath, pdffile)).replace("\\", "/")
                newfileArry.append(pdffiles)
        return newfileArry

    def file_content(self, file):
        # file =file["pdfpath"]
        file_type = os.path.splitext(file)[1][1:]
        file_name = os.path.split(file)[1]
        file_singlename = os.path.splitext(file_name)[0]
        sha1Obj = hashlib.sha1()
        fp = open(file, 'rb')
        contents = fp.read()
        fp.close()
        file_md5 = hashlib.md5(contents).hexdigest()
        sha1Obj.update(contents)
        size = int(os.path.getsize(file))
        sha1 = sha1Obj.hexdigest()
        return file_md5, size, file_type, file_name, contents, file_singlename, sha1

    def shareFile(self,host, sid, csrf, file_id):
        """
        """
        cookies = dict(wps_sid=sid, csrf=csrf)
        url = host + "/api/v3/links"
        headers = {
            "Content-Type": "application/json"
            # "Content-Type": "form-data"
        }
        data = {
            "csrfmiddlewaretoken": csrf,
            "clink": True,
            "range": "anyone",
            "permission": "write",
            "fileid": file_id
        }
        resp = requests.post(url, data=json.dumps(data), cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            logging.error("文件分享失败，失败原因: " + str(resp.content))
            raise RuntimeError("miniAppTools: get user groupid error, statusCode="
                               + str(resp.status_code) + ", response content =" + resp.content)
        else:
            logging.info("文件分享成功")
        print(resp.status_code)
        return resp

    def getShareFile(self,host, sid, file_id):
        """
        """
        cookies = dict(wps_sid=sid)
        url = host + "/api/v3/links/" + str(file_id)
        headers = {
            "Content-Type": "application/json"
            # "Content-Type": "form-data"
        }
        resp = requests.get(url, cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            logging.error("文件分享失败，失败原因: " + str(resp.content))
            raise RuntimeError("miniAppTools: get user groupid error, statusCode="
                               + str(resp.status_code) + ", response content =" + resp.content)
        else:
            logging.info("文件分享成功")
        print (resp.status_code)
        return resp

    def get_metadata(self,host, sid, file_id):
        """
        """
        cookies = dict(wps_sid=sid)
        url = host + "/api/v5/files/" + str(file_id) + "/metadata"
        print(url)
        headers = {
        }
        resp = requests.get(url, cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            # print(resp.content.decode('utf-8'))

            logging.error("文件分享失败，失败原因: " + str(resp.content.decode()))
            raise RuntimeError("miniAppTools: get user groupid error, statusCode="
                               + str(resp.status_code) + ", response content =" + resp.content)
        else:
            logging.info("文件分享成功")
        print (resp.status_code)
        return resp

    def create_folder_team(self,host, sid, team_name, csrf):
        """
        通过用户sid获取该用户的云文档sid
        :param sid:
        :return:
        """
        cookies = dict(wps_sid=sid, csrf=csrf)
        url = host + "/api/v5/groups/special/share/folders"
        headers = {
        }
        # print (url)
        data = {
            "name": team_name,
            "parentid": "0",
            "csrfmiddlewaretoken": csrf
        }

        resp = requests.post(url, json=data, cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            # raise RuntimeError("miniAppTools: get user groupid error, statusCode="
            #                    + str(resp.status_code) + ", response content =" + resp.content)
            print("创建分享文件夹失败，状态码:{},返回内容:{}".format(str(resp.status_code),json.loads(resp.content)))
        print ("创建分享文件夹成功" + str(resp.status_code))
        return resp

    def create_team(self,host, sid, team_name, csrf):
        """
        通过用户sid获取该用户的云文档sid
        :param sid:
        :return:
        """
        cookies = dict(wps_sid=sid, csrf=csrf)
        url = host + "/api/v3/groups"
        # print (url)
        headers = {
        }
        data = {
            "name": team_name,
            "corp_id": 0,
            "csrfmiddlewaretoken": csrf
        }

        resp = requests.post(url, json=data, cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            raise RuntimeError("miniAppTools: get user groupid error, statusCode="
                               + str(resp.status_code) + ", response content =" + resp.content)
        print ("创建团队成功" + str(resp.status_code))
        return resp

    def delete_team_number(self,host, sid, id, csrf, member_id):
        """
        通过用户sid删除团队成员
        :param sid:
        :return:
        """
        cookies = dict(wps_sid=sid, csrf=csrf)
        url = host + "/api/v3/groups/" + str(id) + "/members/" + str(member_id)
        # print (url)
        headers = {
        }
        role_list = ["member", "admin", "creator", "read_member"]
        data = {
            "csrfmiddlewaretoken": csrf
        }

        resp = requests.delete(url, json=data, cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            raise RuntimeError("miniAppTools: get user groupid error, statusCode="
                               + str(resp.status_code) + ", response content =" + resp.content)
        print ("删除团队成员成功" + str(resp.status_code))
        return resp

    def alter_team_number(self,host, sid, id, csrf, member_id,role, data={}):
        """
        通过用户sid修改团队成员角色权限
        :param sid:
        :return:
        """
        cookies = dict(wps_sid=sid, csrf=csrf)
        url = host + "/api/v3/groups/" + str(id) + "/members/" + str(member_id)
        # print (url)
        headers = {
        }
        # role_list = ["member", "admin", "read_member"]
        if data =={}:
            data = {'status': 'active', 'account': '', 'corpid': 0}
        data["csrfmiddlewaretoken"] = csrf
        data["id"] = member_id
        data["role"] = role
        # data = {
        # "id":id,
        # "memberid":member_id,
        # "role":random.choice(role_list),
        # "csrfmiddlewaretoken":csrf
        # }
        print ("rolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerolerole")
        print (data)

        resp = requests.put(url, json=data, cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            raise RuntimeError("miniAppTools: get user groupid error, statusCode="
                               + str(resp.status_code) + ", response content =" + resp.content)
        print ("更改团队成员角色成功" + str(resp.status_code))
        return resp

    def add_team_number(self, host, sid, id, csrf, user_ids):
        """
        通过用户sid添加成员
        :param sid:
        :return:
        """
        cookies = dict(wps_sid=sid, csrf=csrf)
        url = host + "/api/v3/groups/" + str(id) + "/members"
        print ("添加成员url：{},成员id：{}".format(url, user_ids))
        headers = {
        }
        role_list = ["member", "read_member"]
        data = {
            # "groupid": id,
            "userids": user_ids,
            "role": random.choice(role_list),
            "csrfmiddlewaretoken": csrf
        }

        resp = requests.post(url, json=data, cookies=cookies, headers=headers, verify=False)
        if resp.status_code != 200:
            raise RuntimeError("miniAppTools: get user groupid error, statusCode="
                               + str(resp.status_code) + ", response content =" + resp.content)
        print ("新增团队成员成功" + str(resp.status_code))
        return resp

        #创建文件接口程序入口
    def create_file_main(self, sid, filepath):

        # 获取文件基本信息
        # filePath = filepath
        path = filepath
        filePath = path
        newfileArry = self.read_file(filePath)
        i = random.randint(0, len(newfileArry) - 1)
        pdfpath = newfileArry[i]
        file_md5, size, file_type, file_name, file_data, file_singlename, sha1 = self.file_content(pdfpath)

        # 测试环境
        drive_host = "http://drive.wps.cn"
        qing_host = "http://qing.wps.cn"
        sid = sid
        csrf = "BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk"

        uploadAdd = "testProject"

        try:
            # 获取用户groupid
            # print('获取用户groupid')
            resp = self.getUserGroupId(qing_host, sid)
            res = json.loads(resp.content)
            group_id = res.get("id")

            # print('获取ks3上传链接')
            # 获取ks3上传链接
            resp = self.getUploadUrl(qing_host, sid, file_name, sha1, file_md5, size)
            res = json.loads(resp.content)

            # print('ks3链接上传')
            # ks3链接上传
            resp = self.UploadFileToKS3(resp, pdfpath, size)
            etag = resp.headers["ETag"].strip('"')

            # print('云文档创建对应文件')
            # 云文档创建对应文件
            fileInfo = self.qingFileCreate(qing_host, group_id, uploadAdd, sid, file_name, sha1, size, etag)
            id = fileInfo.get("id")
            parentid = fileInfo.get("parentid")
            #
            # print('创建分享链接')
            # # 分享文档
            # resp = self.shareFile(drive_host, sid, csrf, id)
            # res = json.loads(resp.content)
            # print("上传文件成功")
            return {'code': 200, 'message': '上传成功', "file_id": str(id),
                    "parent_id": parentid, "group_id": group_id}
        except Exception as e:
            logging.error("上传云文档出错:%s" % e)
            return {'code': 400, 'message': e}

        #创建文件接口程序入口
    def create_file_main_parentid(self, sid, filepath, parentid):

        # 获取文件基本信息
        # filePath = filepath
        path = filepath
        filePath = path
        newfileArry = self.read_file(filePath)
        i = random.randint(0, len(newfileArry) - 1)
        pdfpath = newfileArry[i]
        file_md5, size, file_type, file_name, file_data, file_singlename, sha1 = self.file_content(pdfpath)

        # 测试环境
        drive_host = "http://drive.wps.cn"
        qing_host = "http://qing.wps.cn"
        sid = sid
        csrf = "BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk"

        uploadAdd = "testProject"

        try:
            # 获取用户groupid
            # print('获取用户groupid')
            resp = self.getUserGroupId(qing_host, sid)
            res = json.loads(resp.content)
            group_id = res.get("id")

            # print('获取ks3上传链接')
            # 获取ks3上传链接
            resp = self.getUploadUrl(qing_host, sid, file_name, sha1, file_md5, size)
            res = json.loads(resp.content)

            # print('ks3链接上传')
            # ks3链接上传
            resp = self.UploadFileToKS3(resp, pdfpath, size)
            etag = resp.headers["ETag"].strip('"')

            # print('云文档创建对应文件')
            # 云文档创建对应文件
            fileInfo = self.qingFileCreate_parentid(qing_host, group_id, parentid, sid, file_name, sha1, size, etag)
            id = fileInfo.get("id")
            parentid = fileInfo.get("parentid")
            #
            # print('创建分享链接')
            # # 分享文档
            # resp = self.shareFile(drive_host, sid, csrf, id)
            # res = json.loads(resp.content)
            # print("上传文件成功")
            return {'code': 200, 'message': '上传成功', "file_id": str(id),
                    "parent_id": parentid, "group_id": group_id}
        except Exception as e:
            logging.error("上传云文档出错:%s" % e)
            return {'code': 400, 'message': e}

    # 上传文档时，传递额外的headers信息
    def create_file_main_update_header(self, sid, filepath, update_headers):

        # 获取文件基本信息
        # filePath = filepath
        path = filepath
        filePath = path
        newfileArry = self.read_file(filePath)
        i = random.randint(0, len(newfileArry) - 1)
        pdfpath = newfileArry[i]
        file_md5, size, file_type, file_name, file_data, file_singlename, sha1 = self.file_content(pdfpath)

        # 测试环境
        drive_host = "http://drive.wps.cn"
        qing_host = "http://qing.wps.cn"
        sid = sid
        csrf = "BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk"

        uploadAdd = "testProject"

        try:
            # 获取用户groupid
            # print('获取用户groupid')
            resp = self.getUserGroupId(qing_host, sid)
            res = json.loads(resp.content)
            group_id = res.get("id")

            # print('获取ks3上传链接')
            # 获取ks3上传链接
            resp = self.getUploadUrl(qing_host, sid, file_name, sha1, file_md5, size)
            res = json.loads(resp.content)

            # print('ks3链接上传')
            # ks3链接上传
            resp = self.UploadFileToKS3(resp, pdfpath, size)
            etag = resp.headers["ETag"].strip('"')

            # print('云文档创建对应文件')
            # 云文档创建对应文件
            fileInfo = self.qingFileCreate_update_header(qing_host, group_id, uploadAdd, sid, file_name, sha1, size, etag, update_headers)
            id = fileInfo.get("id")
            parentid = fileInfo.get("parentid")
            #
            # print('创建分享链接')
            # # 分享文档
            # resp = self.shareFile(drive_host, sid, csrf, id)
            # res = json.loads(resp.content)
            # print("上传文件成功")
            return {'code': 200, 'message': '上传成功', "file_id": str(id),
                    "parent_id": parentid, "group_id": group_id}
        except Exception as e:
            logging.error("上传云文档出错:%s" % e)
            return {'code': 400, 'message': e}

        #创建文件接口程序入口
    def delete_file_main(self,sid,file_id):
        startTime = datetime.datetime.now()
        # 测试环境
        drive_host = "https://drive.wps.cn"
        qing_host = "https://qing.wps.cn"
        sid = sid
        csrf = "BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk"

        try:
            # 获取用户groupid
            print ('获取用户groupid')
            resp = self.getUserGroupId(qing_host, sid)
            res = json.loads(resp.content)
            group_id = res.get("id")

            print ('获取父文件id')
            resp = self.get_metadata(drive_host, sid, file_id)
            res = json.loads(resp.content)
            fileinfo = res.get("fileinfo")
            parent_id = fileinfo["parentid"]

            print ("删除文件")
            result = self.delete_file(drive_host, sid, group_id, parent_id, file_id,csrf)
            # result = self.delete_file(drive_host, sid, group_id, file_id, csrf)
            # res = json.loads(resp.content)
            # result = res.get("result")

            endTime = datetime.datetime.now()
            logging.info("删除文件:%f" % (endTime - startTime).seconds)
            # print ("上传文件成功")
            return {'code':200,'message':'删除文件成功',"file_id":str(file_id),"result":result}
        except Exception as e:
            logging.error("删除文件出错:%s" % e.message)
            return {'code': 400,'message':e.message}

        #创建文件接口程序入口
    def create_team_main(self,sid,member_userid,filepath):
        startTime = datetime.datetime.now()
        # 测试环境
        drive_host = "https://drive.wps.cn"
        qing_host = "https://qing.wps.cn"
        sid = sid
        csrf = "BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk"

        team_name = ''.join(random.sample(string.ascii_letters + string.digits+string.ascii_letters, 20))
        print (team_name)
        member_userid_list =[int(member_userid)]
        path=filepath
        isExists = os.path.exists(path)
        # abc = str(datetime.datetime.now()).split(".")
        # abc = abc[0].replace("-",'')
        abc = str(datetime.datetime.now()).replace(".",'')
        abc = abc.replace("-",'')
        abc = abc.replace(":",'')
        abc = abc.replace(" ",'')
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录# 创建目录操作函数
            print ("111111111111111111")
            os.makedirs(path)
            logging.info(path + ' 创建成功')
        else:
            print ("22222222222222222")
            # 如果目录存在则不创建，并提示目录已存在
            logging.info(path + ' 目录已存在')
        with open(path + '/test' + abc + '.txt', 'w') as f:
            f.write(''.join(random.sample(string.ascii_letters + string.digits+string.ascii_letters + string.digits+string.ascii_letters + string.digits, 100)) + str(datetime.datetime.now()))
        # filePath = path
        logging.info("创建文件---成功")
        logging.info("文件名称为:" + '/test' + abc + '.txt')
        filePath = path
        i = 0
        files = []
        newfileArry = self.read_file(filePath)
        i = random.randint(0, len(newfileArry) - 1)
        pdfpath = newfileArry[i]
        file_md5, size, file_type, file_name, file_data, file_singlename, sha1 = self.file_content(pdfpath)

        # 测试环境
        drive_host = "https://drive.wps.cn"
        qing_host = "https://qing.wps.cn"
        sid = sid
        csrf = "BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk"

        filepath111, fileName = os.path.split(pdfpath)
        uploadAdd = []

        try:
            # 获取用户groupid
            print ('获取用户groupid')
            resp = self.getUserGroupId(qing_host, sid)
            res = json.loads(resp.content)
            group_id = res.get("id")

            resp = self.create_team(drive_host, sid, team_name, csrf)
            res = json.loads(resp.content)
            team_id = res.get("id")
            corpid = res.get("corpid")  # 个人团队
            team_name = res.get("name")

            resp = self.add_team_number(drive_host, sid, team_id, csrf, member_userid_list)
            res = json.loads(resp.content)
            members = res.get("members")

            group_id = team_id

            print ('获取ks3上传链接')
            # 获取ks3上传链接
            resp = self.getUploadUrl(qing_host, sid, group_id, fileName, filePath, sha1, file_md5, size)
            res = json.loads(resp.content)
            date = res.get("uploadinfo").get("put_auth").get("date")

            print ('ks3链接上传')
            # ks3链接上传
            resp = self.UploadFileToKS3(resp, pdfpath, size)
            etag = resp.headers["ETag"].strip('"')

            print ('云文档创建对应文件')
            # 云文档创建对应文件
            fileInfo = self.qingFileCreate(qing_host, group_id, uploadAdd, sid, fileName, sha1, size,etag)
            id = fileInfo.get("id")
            parentid = fileInfo.get("parentid")
            groupid = fileInfo.get("groupid")

            endTime = datetime.datetime.now()
            logging.info("创建团队文件成功:%f" % (endTime - startTime).seconds)
            # print ("上传文件成功")
            return {'code':200,'message':'创建团队文件成功',"file_id":str(id),"team_id":str(team_id)}
        except Exception as e:
            logging.error("创建团队文件成功:%s" % e.message)
            return {'code': 400,'message':e.message}

    def relation_list(self, host, sid, csrf):
        '''
        获取联系人列表
        :param host:
        :param sid:
        :param csrf:
        :return:
        '''
        cookies = dict(wps_sid=sid, csrf=csrf)
        url = host + "/api/contact/relation/list"
        print("获取联系人列表:{}".format(url))
        resp = requests.get(url, cookies=cookies)
        print(resp.text)
        if resp.status_code != 200:
            raise RuntimeError(
                "Error code" + str(resp.status_code) + ", response content =" + (resp.content).decode('utf-8'))
        print("获取联系人列表成功" + str(resp.status_code))
        return resp

    def relation_list(self, host, sid, csrf):
        cookies = dict(wps_sid=sid, csrf=csrf)
        url = host + "/api/contact/relation/list"
        print("获取联系人列表:{}".format(url))
        resp = requests.get(url, cookies=cookies)
        print(resp.text)
        if resp.status_code != 200:
            logging.info("获取联系人列表失败，状态码：{}，返回内容：{}".format(resp.status_code, resp.content))
            print("获取联系人列表失败，状态码：{}，返回内容：{}".format(resp.status_code, resp.content))
        print("获取联系人列表成功" + str(resp.status_code))
        return resp

    def delete_friend(self, host, sid, csrf, friend_id):
        cookies = dict(wps_sid=sid, csrf=csrf)
        url = host + "/api/contact/relation"
        print("单向删除好友：{}".format(url))
        data = {
            "csrfmiddlewaretoken": csrf,
            "user_id": friend_id
        }
        resp = requests.delete(url, json=data, cookies=cookies)
        print(resp.content)
        if resp.status_code not in [200, 403]:
            print("单向删除好友失败，状态码：{}，返回内容：{}".format(resp.status_code,resp.content) )
            logging.info("单向删除好友失败，状态码：{}，返回内容：{}".format(resp.status_code,resp.content))
            return resp
        print("单向删除好友成功" + str(resp.status_code))
        logging.info("单向删除好友成功，状态码：{}，返回内容：{}".format(resp.status_code, resp.content))
        return resp

    def relation_info(self, host, sid, csrf, user_id):
        cookies = dict(wps_sid=sid, csrf=csrf)
        url = host + "/api/contact/relation/info"
        print("获取联系人详细信息:{}".format(url))
        data = {
            "user_id":user_id
        }
        resp = requests.get(url, cookies=cookies, json=data)
        print(resp.text)
        if resp.status_code != 200:
            logging.info("获取联系人信息失败，状态码：{}，返回内容：{}".format(resp.status_code, resp.content))
            print("获取联系人信息失败，状态码：{}，返回内容：{}".format(resp.status_code, resp.content))
        print("获取联系人信息成功" + str(resp.status_code))
        return resp


if __name__ == '__main__':
    uploadfile = uploadFile()
    # groupid = uploadfile.getUserGroupId("https://qing.wps.cn","V02Sn75lB57e33G_h-vAjVSWlXaGYIE00aebc08d000ee6c256")
    # resp = uploadfile.create_folder_team("https://drive.wps.cn", "V02Sjtcfq8WieCBVduakMTj_6vTkI5g00ae6a431000ee6b678","wwwwww","BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk")
    # resp = uploadfile.relation_list("http://account.wps.cn", "V02Sjtcfq8WieCBVduakMTj_6vTkI5g00ae6a431000ee6b678","BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk")
    # print(resp.content)
    resp = uploadfile.delete_friend("https://account.wps.cn", "V02Sjtcfq8WieCBVduakMTj_6vTkI5g00ae6a431000ee6b678","BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk",238777755)
    print("=======",resp.status_code)
    # resp_json = json.loads(resp.content)
    # print(resp_json["linkgroupid"])
    # uploadfile.add_team_number("https://drive.wps.cn","V02S0s5rNzJFkw5gVYuBX_gB2L3e17800a8b815f000db0878c",resp_json["linkgroupid"],"BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk",[250004874])
    # uploadfile.delete_file("https://drive.wps.cn","V02S0s5rNzJFkw5gVYuBX_gB2L3e17800a8b815f000db0878c", resp_json["linkgroupid"], resp_json["groupid"], resp_json["folderid"], "BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk")
    #     # uploadfile.delete_file("https://drive.wps.cn","V02S0s5rNzJFkw5gVYuBX_gB2L3e17800a8b815f000db0878c", 1261440056 , 511927173,96157176731, "BpdWBJinyTctdW6Tr8F3a5GYDrpN8mkk")