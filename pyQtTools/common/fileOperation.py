# -*- coding: utf-8 -*-
import requests
import json
from common.uploadFile import uploadFile
from common.logs_output import info_log, error_log
import random
import os
import time
import sys
# base_Dir = os.path.dirname(os.path.dirname(__file__))
base_Dir = os.path.dirname(sys.executable)


class FileOperation(object):

    def deleteGroupId(self, sid):
        # 获取文件夹列表
        groupIdListUrl = "https://drive.kdocs.cn/api/v5/links/mine?offset=0&count=100&orderby=file_mtime&order=DESC" \
                              "&append=false&ignore=link"
        groupIdListHeaders = {
            "cookie": "wps_sid={}; csrf=GfQySxDCpEMmkDNBaz776swjzM5fXsPw".format(sid),
        }
        response = requests.get(url=groupIdListUrl, headers=groupIdListHeaders)
        groupIdListResponse = response.json()

        # 删除该sid下所有共享文件夹
        headers = {
            "Content-Type": "application/json",
            "cookie": "wps_sid={}; csrf=GfQySxDCpEMmkDNBaz776swjzM5fXsPw".format(sid),
            "Account-DeviceName": "bmFzc3Vl",
            "Account-DeviceId": "bmFzc3VlLXBjMQ==",
            "Client-Type": "wps-pc",
            "Client-Chan": "1.1.1",
            "Client-Ver": "2.2.2"
        }
        data = {"csrfmiddlewaretoken": "GfQySxDCpEMmkDNBaz776swjzM5fXsPw"}
        for i in range(len(groupIdListResponse["share"])):
            if groupIdListResponse["share"][i]["share_type"] == "linkfolder":
                linkgroupid = groupIdListResponse["share"][i]["file"]["linkgroupid"]
                url = "https://qing.wps.cn/api/v3/groups/" + str(linkgroupid)
                response = requests.delete(url=url, headers=headers, json=data)
                print(response.text)

    def del_file(self, path_data):
        """删除本地某个路径文件夹下的所有文件"""
        for i in os.listdir(path_data):  # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
            file_data = path_data + "/" + i  # 当前文件夹的下面的所有东西的绝对路径
            os.remove(file_data)

    def uploadCloudFile(self, sid):
        """在个人空间下，上传云文档"""
        file_dir = base_Dir + '/data/upload_file'
        self.del_file(file_dir)
        file_name = str(int(time.time())) + "test.doc"
        f = open(file_dir + "/" + file_name, 'w')
        for i in range(0, 10):
            f.write(str(random.randint(0, 100)))
        f.close()
        response = uploadFile().create_file_main(sid, file_dir)
        if response["code"] != 200:
            error_log("上传云文件失败")
            return None, None, None
        file_id = str(response['file_id'])
        group_id = response['group_id']
        info_log("file_name : {}".format(file_name))
        info_log("group_id : {}".format(group_id))
        info_log("file_id : {}".format(file_id))
        return file_id, group_id, file_name

    def uploadCloudFile_update_fileName(self, sid, file_name):
        """上传个人空间的云文档，可修改文件名"""
        file_dir = base_Dir + '/data/upload_file'
        self.del_file(file_dir)
        file_name = file_name + "test.doc"
        f = open(file_dir + "/" + file_name, 'w')
        for i in range(0, 10):
            f.write(str(random.randint(0, 100)))
        f.close()
        response = uploadFile().create_file_main(sid, file_dir)
        if response["code"] != 200:
            error_log("上传云文件失败")
            return None, None, None
        file_id = str(response['file_id'])
        group_id = response['group_id']
        info_log("file_name : {}".format(file_name))
        info_log("group_id : {}".format(group_id))
        info_log("file_id : {}".format(file_id))
        return file_id, group_id, file_name

    def uploadCloudFile_update_fileName_parentid(self, sid, file_name, parentid):
        """上传个人空间的云文档，可指定在某个文件夹parentid下，可修改文件名"""
        file_dir = base_Dir + '/data/upload_file'
        self.del_file(file_dir)
        file_name = file_name + "test.doc"
        f = open(file_dir + "/" + file_name, 'w')
        for i in range(0, 10):
            f.write(str(random.randint(0, 100)))
        f.close()
        response = uploadFile().create_file_main_parentid(sid, file_dir, parentid)
        if response["code"] != 200:
            error_log("上传云文件失败")
            return None, None, None
        file_id = str(response['file_id'])
        group_id = response['group_id']
        info_log("file_name : {}".format(file_name))
        info_log("group_id : {}".format(group_id))
        info_log("file_id : {}".format(file_id))
        return file_id, group_id, file_name

    def uploadCloudFile_update_header(self, sid, update_headers):
        """上传个人空间的云文档，可变更上传接口的请求头信息"""
        file_dir = base_Dir + '/data/upload_file'
        print("file_dir: {}".format(file_dir))
        self.del_file(file_dir)
        file_name = str(int(time.time())) + "test.doc"
        f = open(file_dir + "/" + file_name, 'w')
        for i in range(0, 10):
            f.write(str(random.randint(0, 100)))
        f.close()
        response = uploadFile().create_file_main_update_header(sid, file_dir, update_headers)
        if response["code"] != 200:
            error_log("上传云文件失败")
            return None, None, None
        file_id = str(response['file_id'])
        group_id = response['group_id']
        info_log("file_name : {}".format(file_name))
        info_log("group_id : {}".format(group_id))
        info_log("file_id : {}".format(file_id))
        return file_id, group_id, file_name

    def deleteCloudFile(self, group_id, file_id, sid):
        """删除云文档，指定团队id、指定用户、指定文件"""
        response = uploadFile().DeleteResultFile(group_id, file_id, sid)
        return response

    def get_group_id(self, sid):
        """获取用户个人空间的团队id"""
        info_log("获取用户个人空间的团队id")
        host = "http://qing.wps.cn"
        response = uploadFile().getUserGroupId(host, sid)
        if response.status_code == 200:
            group_id = response.json()["id"]
            print(response.json())
            info_log("group_id: {}".format(group_id))
            return group_id
        else:
            return False

    def create_folder(self, sid, name):
        """创建用户个人空间下第一层目录的文件夹"""
        groupid = self.get_group_id(sid)
        response = uploadFile().create_folder(sid, groupid, name)
        return response

    def delete_all_file____demo(self, sid):
        groupid = self.get_group_id(sid)
        get_parentid_url = "https://drive.kdocs.cn/api/v5/groups/{}/files?count=3000&filter=folder".format(groupid)
        get_parentid_headers = {
            "cookie": "wps_sid={}; csrf=GfQySxDCpEMmkDNBaz776swjzM5fXsPw".format(sid),
        }
        response = requests.get(url=get_parentid_url, headers=get_parentid_headers)
        print(response.status_code)
        print(response.json())
        print(len(response.json()["files"]))
        if response.status_code == 200:
            response_body = response.json()
            if len(response_body["files"]) > 0:
                for i in range(len(response_body["files"])):

                    parentid = response_body["files"][i]["id"]
                    get_fileid_url = "https://drive.kdocs.cn/api/v5/groups/{}/files?count=3000&parentid={}".format(
                        groupid, parentid)
                    get_fileid_headers = {
                        "cookie": "wps_sid={}; csrf=GfQySxDCpEMmkDNBaz776swjzM5fXsPw".format(sid),
                    }
                    f_response = requests.get(url=get_fileid_url, headers=get_fileid_headers)
                    print(f_response.status_code)
                    print(f_response.json())
                    print(len(f_response.json()["files"]))
                    return len(f_response.json()["files"])

    def delete_all_file_and_folder(self, sid):
        """删除用户个人空间所有文件及文件夹"""
        groupid = self.get_group_id(sid)
        if groupid is False:
            return False
        get_fileInfo_url = "https://drive.kdocs.cn/api/v5/groups/{}/files?count=99000".format(groupid)
        get_fileInfo_headers = {
            "cookie": "wps_sid={}; csrf=GfQySxDCpEMmkDNBaz776swjzM5fXsPw".format(sid),
        }
        response = requests.get(url=get_fileInfo_url, headers=get_fileInfo_headers)
        if response.status_code == 200:

            info_log("存在 {} 条文件数据".format(len(response.json()["files"])))
            response_body = response.json()
            if len(response_body["files"]) > 0:
                for i in range(len(response_body["files"])):
                    info_log("清理第 {} 个文件".format(i+1))
                    parentid = response_body["files"][i]["id"]
                    response = self.deleteCloudFile(groupid, parentid, sid)
                    if response.status_code == 200:
                        pass
                    else:
                        error_log("清除失败！")
                        return False
            info_log("文件已清除干净！")
            return True
        else:
            error_log("获取文件失败")
            error_log("获取文件接口返回code: {}".format(response.status_code))
            return False

    def get_groups(self, sid):
        """获取用户所有团队列表"""
        url = "http://qing.wps.cn/api/v3/groups"
        headers = {
            "cookie": "wps_sid={}; csrf=GfQySxDCpEMmkDNBaz776swjzM5fXsPw".format(sid),
        }
        response = requests.get(url=url, headers=headers)
        groups = []
        for i in range(len(response.json()["groups"])):
            group_id = response.json()["groups"][i]["id"]
            groups.append(group_id)
        return groups

    def upload_device_file(self, sid, device_id):
        """上传设备文件"""
        file_dir = base_Dir + '/data/upload_file/aaa.docx'
        response = uploadFile().create_deivce_file(sid, device_id, file_dir)
        return response

    def re_upload_device_file(self, args, sid, device_id, num, assert_list):
        for i in range(0, int(num)):
            FileOperation().upload_device_file(sid, device_id)
            assert_list.append(args)


if __name__ == '__main__':
    # FileOperation().del_file(base_Dir + '/data/upload_file')
    # file_id, group_id, file_name = FileOperation().uploadCloudFile("V02SEgoWH-1CoT7fN6eNd5Wo2dMySx000aa78d77004d65b717")
    a = FileOperation().get_group_id("V02Sb5Polh8tsFbQ2yUjEHpyrXOqNTQ00a252310000e3d3bcb")
    print(a)
    # FileOperation().delete_all_file("V02Sb5Polh8tsFbQ2yUjEHpyrXOqNTQ00a252310000e3d3bcb")
    # response = FileOperation().deleteCloudFile("1135101", 100042945703, "V02Sb5Polh8tsFbQ2yUjEHpyrXOqNTQ00a252310000e3d3bcb")
    # print(response.status_code)
    # print(response.json())
    # a = FileOperation().delete_all_file_and_folder("V02Sb5Polh8tsFbQ2yUjEHpyrXOqNTQ00a252310000e3d3bcb")
    # print(a)
    # res = FileOperation().create_folder("V02Sb5Polh8tsFbQ2yUjEHpyrXOqNTQ00a252310000e3d3bcb", "abc")
    # print(res.json())
    # res = FileOperation().create_folder("V02SLdmQ1YUvYOxwO68HBY_cyxAtIco00aaf07050010b0fb98", "lolo")
    # print(res.json()["id"])
    # file_id, group_id, file_name = FileOperation().uploadCloudFile_update_fileName_parentid("V02SLdmQ1YUvYOxwO68HBY_cyxAtIco00aaf07050010b0fb98", "fileooo", 100043155151)
    # groups_id = FileOperation().get_groups("V02Sb5Polh8tsFbQ2yUjEHpyrXOqNTQ00a252310000e3d3bcb")
    # print(groups_id)

