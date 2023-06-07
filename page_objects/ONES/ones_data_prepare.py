# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import yaml


def prepare_ones_data():
    # 获取环境变量
    config_path = os.path.join(os.path.join(sys.path[1], ''), "config.yaml")
    with open(config_path) as f:
        env = yaml.load(f.read(), Loader=yaml.SafeLoader)

    # 获取ONES token、uuid、team_uuid、org_uuid
    login_url = env["ones_env_url"] + env["ones_base_url"] + "/auth/login"
    login_payload = json.dumps({
        "password": env["ones_env_pwd"],
        "captcha": "",
        "email": env["ones_env_user"]
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
        'Referer': env["ones_env_url"].split("//")[1],
        'Ones-User-Id': uuid,
        'Ones-Auth-Token': token,
        'Content-Type': 'application/json',
    }
    invite_payload = json.dumps({
        "invite_settings":
            [{
                "email": env["ones_env_common_user"]
            },
                {
                    "email": env["ones_env_common_user2"]
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
    invite_url = env["ones_env_url"] + env["ones_base_url"] + "/team/" + team_uuid + "/invitations/add_batch"
    requests.request("POST", invite_url, headers=invite_headers, data=invite_payload)

    # 获取邀请码
    invitation_headers = invite_headers
    invitation_url = env["ones_env_url"] + env["ones_base_url"] + "/team/" + team_uuid + "/invitations"
    invitation_payload = json.dumps({})
    invitation = requests.request("GET", invitation_url, headers=invitation_headers, data=invitation_payload)
    invitation_resp = json.loads(invitation.text)["invitations"]

    for i in range(len(invitation_resp)):
        if invitation_resp[i]["email"] == env["ones_env_common_user"]:
            invitation_code = invitation_resp[i]["code"]
        elif invitation_resp[i]["email"] == env["ones_env_common_user2"]:
            invitation_code2 = invitation_resp[i]["code"]

    # 成员使用邀请码加入团队
    join_headers = login_headers
    join_url = env["ones_env_url"] + env["ones_base_url"] + "/auth/invite_join_team"
    join_payload = json.dumps({
        "email": env["ones_env_common_user"],
        "password": env["ones_env_pwd"],
        "name": "Ones_common_user",
        "invite_code": invitation_code
    })
    join_payload2 = json.dumps({
        "email": env["ones_env_common_user2"],
        "password": env["ones_env_pwd"],
        "name": "Ones_common_user2",
        "invite_code": invitation_code2
    })
    common_user = requests.request("POST", join_url, headers=join_headers, data=join_payload)
    common_user_uuid = json.loads(common_user.text)["user"]["uuid"]
    requests.request("POST", join_url, headers=join_headers, data=join_payload2)

    # 为用户1添加组织管理员权限
    org_admin_headers = invite_headers
    org_admin_url = env["ones_env_url"] + env["ones_base_url"] + "/organization/" + org_uuid + "/permission_rules/add"
    org_admin_payload = json.dumps({"permission_rule": {"context_type": "organization", "context_param": None,
                                                        "permission": "administer_organization",
                                                        "user_domain_type": "single_user",
                                                        "user_domain_param": common_user_uuid}})
    requests.request("POST", org_admin_url, headers=org_admin_headers, data=org_admin_payload)

    # 为用户1添加超级管理员权限
    team_admin_headers = invite_headers
    team_admin_url = env["ones_env_url"] + env["ones_base_url"] + "/team/" + team_uuid + "/permission_rules/add"
    team_admin_payload = json.dumps({"permission_rule": {"context_type": "team", "context_param": None,
                                                         "permission": "super_administrator",
                                                         "user_domain_type": "single_user",
                                                         "user_domain_param": common_user_uuid}})
    team_admin_response = requests.request("POST", team_admin_url, headers=team_admin_headers, data=team_admin_payload)

    # 创建两个测试团队
    create_team_headers = invite_headers
    create_team_url = env["ones_env_url"] + env["ones_base_url"] + "/organization/" + org_uuid + "/create_team"
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


if __name__ == '__main__':
    prepare_ones_data()
