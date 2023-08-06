import asyncio
from typing import Dict

from channels.layers import get_channel_layer
from django.conf import settings


def user_notice(user_id: int, msg: Dict):
    try:
        loop = asyncio.get_running_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    layer = get_channel_layer()
    channel_name = settings.IACS_SETTINGS["USER_CHANNEL_GROUP_NAME"]
    loop.run_until_complete(layer.group_send(
        channel_name.format(user_id=user_id),
        {'type': 'send.message', 'message': msg}
    ))


def broadcast(msg: Dict):
    try:
        loop = asyncio.get_running_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    layer = get_channel_layer()
    loop.run_until_complete(layer.group_send(
        settings.IACS_SETTINGS["GROUP_CHANNEL_NAME"],
        {'type': 'send.message', 'message': msg}
    ))
