# -*- coding: utf-8 -*-
import json
import os

import requests
import yaml


def read_config():
    # 获取config.yaml变量
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("JiraMigrationTool_UITest") + len("JiraMigrationTool_UITest")]
    config_path = os.path.abspath(rootPath + '/config.yaml')

    with open(config_path) as f:
        env_info = yaml.load(f.read(), Loader=yaml.SafeLoader)
        return env_info


def prepare_data():
    # 获取ONES 配置信息
    ones_env = read_config()
    # 获取ONES token、uuid、team_uuid、org_uuid
    login_url = ones_env["ones_env_url"] + ones_env["ones_base_url"] + "/auth/login"
    login_payload = json.dumps({
        "password": ones_env["ones_env_pwd"],
        "captcha": "",
        "email": ones_env["ones_env_user"]
    })
    login_headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }
    login_response = requests.request("POST", login_url, headers=login_headers, data=login_payload)
    token = json.loads(login_response.text)["user"]["token"]
    uuid = json.loads(login_response.text)["user"]["uuid"]
    team_uuid = json.loads(login_response.text)["teams"][0]["uuid"]
    org_uuid = json.loads(login_response.text)["org"]["uuid"]

    # 邀请成员
    invite_headers = {
        'Referer': ones_env["ones_env_url"].split("//")[1],
        'Ones-User-Id': uuid,
        'Ones-Auth-Token': token,
        'Content-Type': 'application/json',
    }
    invite_payload = json.dumps({
        "invite_settings":
            [{
                "email": ones_env["ones_env_common_user"]
            },
                {
                    "email": ones_env["ones_env_common_user2"]
                }
            ]
        ,
        "license_types": [
            "project",
            "wiki",
            "desk",
            "ones_task",
            "performance",
            "pipeline_integration",
            "plan",
            "testcase"
        ]
    })
    invite_url = ones_env["ones_env_url"] + ones_env["ones_base_url"] + "/team/" + team_uuid + "/invitations/add_batch"
    requests.request("POST", invite_url, headers=invite_headers, data=invite_payload)

    # 获取邀请码
    invitation_headers = invite_headers
    invitation_url = ones_env["ones_env_url"] + ones_env["ones_base_url"] + "/team/" + team_uuid + "/invitations"
    invitation_payload = json.dumps({})
    invitation = requests.request("GET", invitation_url, headers=invitation_headers, data=invitation_payload)
    invitation_resp = json.loads(invitation.text)["invitations"]

    for i in range(len(invitation_resp)):
        if invitation_resp[i]["email"] == ones_env["ones_env_common_user"]:
            invitation_code = invitation_resp[i]["code"]
        elif invitation_resp[i]["email"] == ones_env["ones_env_common_user2"]:
            invitation_code2 = invitation_resp[i]["code"]

    # 成员使用邀请码加入团队
    join_headers = login_headers
    join_url = ones_env["ones_env_url"] + ones_env["ones_base_url"] + "/auth/invite_join_team"
    join_payload = json.dumps({
        "email": ones_env["ones_env_common_user"],
        "password": ones_env["ones_env_pwd"],
        "name": "Ones_common_user",
        "invite_code": invitation_code
    })
    join_payload2 = json.dumps({
        "email": ones_env["ones_env_common_user2"],
        "password": ones_env["ones_env_pwd"],
        "name": "Ones_common_user2",
        "invite_code": invitation_code2
    })
    common_user = requests.request("POST", join_url, headers=join_headers, data=join_payload)
    common_user_uuid = json.loads(common_user.text)["user"]["uuid"]
    requests.request("POST", join_url, headers=join_headers, data=join_payload2)

    # 为用户1添加组织管理员权限
    org_admin_headers = invite_headers
    org_admin_url = ones_env["ones_env_url"] + ones_env[
        "ones_base_url"] + "/organization/" + org_uuid + "/permission_rules/add"
    org_admin_payload = json.dumps({"permission_rule": {"context_type": "organization", "context_param": None,
                                                        "permission": "administer_organization",
                                                        "user_domain_type": "single_user",
                                                        "user_domain_param": common_user_uuid}})
    requests.request("POST", org_admin_url, headers=org_admin_headers, data=org_admin_payload)

    # 为用户1添加超级管理员权限
    team_admin_headers = invite_headers
    team_admin_url = ones_env["ones_env_url"] + ones_env[
        "ones_base_url"] + "/team/" + team_uuid + "/permission_rules/add"
    team_admin_payload = json.dumps({"permission_rule": {"context_type": "team", "context_param": None,
                                                         "permission": "super_administrator",
                                                         "user_domain_type": "single_user",
                                                         "user_domain_param": common_user_uuid}})
    team_admin_response = requests.request("POST", team_admin_url, headers=team_admin_headers, data=team_admin_payload)

    # 创建两个测试团队
    create_team_headers = invite_headers
    create_team_url = ones_env["ones_env_url"] + ones_env[
        "ones_base_url"] + "/organization/" + org_uuid + "/create_team"
    create_team_payload1 = json.dumps({
        "team_name": "zz_team1",
        "team_owner": uuid
    })
    create_team_payload2 = json.dumps({
        "team_name": "zz_team2",
        "team_owner": uuid
    })
    requests.request("POST", create_team_url, headers=create_team_headers, data=create_team_payload1)
    requests.request("POST", create_team_url, headers=create_team_headers, data=create_team_payload2)
    print("测试数据准备完成")


def get_ones_token():
    # 获取环境变量
    ones_env = read_config()
    # 获取ONES token、uuid、team_uuid、org_uuid
    login_url = ones_env["ones_env_url"] + ones_env["ones_base_url"] + "/auth/login"
    login_payload = json.dumps({
        "password": ones_env["ones_env_pwd"],
        "captcha": "",
        "email": ones_env["ones_env_user"]
    })
    login_headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }
    login_response = requests.request("POST", login_url, headers=login_headers, data=login_payload)
    token = json.loads(login_response.text)["user"]["token"]
    uuid = json.loads(login_response.text)["user"]["uuid"]
    team_uuid = json.loads(login_response.text)["teams"][0]["uuid"]
    org_uuid = json.loads(login_response.text)["org"]["uuid"]
    ones_headers = {
        'Referer': ones_env["ones_env_url"].split("//")[1],
        'Ones-User-Id': uuid,
        'Ones-Auth-Token': token,
        'Content-Type': 'application/json',
    }
    return team_uuid, ones_headers


def create_custom_fields():

    team, api_headers = get_ones_token()
    ones_env = read_config()
    api_url = ones_env["ones_env_url"] + ones_env["ones_base_url"] + "/team/" + team + "/fields/add"
    multi_choice = {"field": {
        "name": "自定义单选菜单",
        "type": 16,
        "renderer": 1,
        "filter_option": 0,
        "search_option": 1,
        "options": [
            {
                "value": "多选001",
                "background_color": "#307fe2",
                "color": "#fff"
            },
            {
                "value": "多选002",
                "background_color": "#00b388",
                "color": "#fff"},
            {
                "value": "多选003",
                "background_color": "#00b388",
                "color": "#fff"},
            {
                "value": "多选004",
                "background_color": "#00b388",
                "color": "#fff"},
            {
                "value": "我是超长的多选选项值呀哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈或或或或或或",
                "background_color": "#f1b300",
                "color": "#fff"}
        ]
    }}
    single_line = {
        "field": {
            "name": "自定义单行文本",
            "type": 2,
            "renderer": 1,
            "filter_option": 0,
            "search_option": 1
        }
    }
    multi_line = {
        "field": {
            "name": "自定义多行文本",
            "type": 15,
            "renderer": 1,
            "filter_option": 0,
            "search_option": 1
        }
    }
    number_field = {
        "field": {
            "name": "自定义浮点数",
            "type": 4,
            "renderer": 1,
            "filter_option": 0,
            "search_option": 1
        }
    }
    date_field = {
        "field": {
            "name": "自定义日期",
            "type": 5,
            "renderer": 1,
            "filter_option": 0,
            "search_option": 1
        }
    }
    datetime_field = {
        "field": {
            "name": "自定义时间",
            "type": 6,
            "renderer": 1,
            "filter_option": 0,
            "search_option": 1
        }
    }
    multiple_user = {
        "field": {
            "name": "自定义多选成员",
            "type": 13,
            "renderer": 1,
            "filter_option": 0,
            "search_option": 1
        }
    }
    single_user = {
        "field": {
            "name": "自定义单选成员",
            "type": 8,
            "renderer": 1,
            "filter_option": 0,
            "search_option": 1
        }
    }
    custom_list = [multi_choice, single_line, multi_line, number_field, date_field, datetime_field, multiple_user,
                   single_user]
    for field in custom_list:
        requests.request("POST",
                         api_url, headers=api_headers, data=json.dumps(field))


