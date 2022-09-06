from dataclasses import dataclass
from typing import Literal
import requests

from qute.exceptions import APIError, RequestError, TokenError


@dataclass
class Config:
    root: str
    token: str = ""


def _get(root: str, endpoint: str, **params):
    res = requests.get(f"{root}/{endpoint}", params)
    if res.status_code == 401 or res.status_code == 403:
        raise TokenError("Require a valid access token.")
    elif res.status_code == 406:
        raise RequestError("Invalid content type.")
    elif res.status_code == 404:
        raise NotImplementedError("No this function.")
    data = res.json()
    if data["status"] == "failed":
        raise APIError(data["msg"], data["wording"])
    # elif data["status"] == "async":
    #     return {}
    else:
        return data["data"]


def send_private_msg(
    conf: Config, uid: int, msg: str, autoesc: bool = False
):
    return _get(
        conf.root, "send_private_msg", access_token=conf.token,
        user_id=uid, message=msg, auto_escape=autoesc
    )


def send_group_msg(
    conf: Config, gid: int, msg: str, autoesc: bool = False
):
    return _get(
        conf.root, "send_group_msg", access_token=conf.token,
        group_id=gid, message=msg, auto_escape=autoesc
    )


def send_msg(
    conf: Config, mtype: Literal["private", "group"],
    id: int, msg: str, autoesc: bool = False
):
    data = {
        "message_type": mtype,
        "message": msg,
        "auto_escape": autoesc
    }
    if mtype == "private":
        data["user_id"] = id
    elif mtype == "group":
        data["group_id"] = id
    else:
        raise ValueError("Message type must be 'private' or 'group'")
    return _get(conf.root, "send_msg", access_token=conf.token, **data)


def get_msg(conf: Config, mid: int):
    return _get(conf.root, "get_msg", access_token=conf.token, message_id=mid)


def get_group_member_info(
    conf: Config, gid: int, uid: int, cache: bool = True
):
    return _get(
        conf.root, "get_group_member_info", access_token=conf.token,
        group_id=gid, user_id=uid, no_cache=not cache
    )


def get_friend_list(conf: Config):
    return _get(conf.root, "get_friend_list", access_token=conf.token)


def get_group_list(conf: Config):
    return _get(conf.root, "get_group_list", access_token=conf.token)