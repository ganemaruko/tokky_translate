# -*- coding: utf-8 -*-
import os
import requests


def send_line_notify(notification_message: str):
    """
    LINEに通知する
    """
    line_notify_token = os.environ["LINE_NOTIFY_KEY"]
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers=headers, data=data)


def get_gip_addr():
    res = requests.get('https://ifconfig.me')
    return res.text


if __name__ == "__main__":
    ip_address = get_gip_addr()
    send_line_notify(f"hello! {ip_address}")
