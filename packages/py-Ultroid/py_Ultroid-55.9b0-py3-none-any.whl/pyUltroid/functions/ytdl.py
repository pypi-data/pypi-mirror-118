# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import os
import time

from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from youtubesearchpython import VideosSearch

from .all import dler, uploader


async def get_yt_link(query):
    search = VideosSearch(query, limit=1).result()
    data = search["result"][0]
    link = data["link"]
    return link


async def download_yt(event, link, ytd):
    info = await dler(event, link, ytd, download=True)
    title = info["title"]
    thumb = info["thumbnails"][-1]["url"] + ".jpg"
    duration = info["duration"]
    file = info["id"] + "." + info["ext"]
    res = await uploader(file, file, time.time(), event, "Uploading...")
    if file.endswith((".mkv", "mp4", "webm")):
        height, width = info["height"], info["width"]
        caption = f"`{title}`\n\n`From YouTube Official`"
        await event.client.send_file(
            event.chat_id,
            file=res,
            caption=caption,
            attributes=[
                DocumentAttributeVideo(
                    duration=duration,
                    w=width,
                    h=height,
                    supports_streaming=True,
                )
            ],
            thumb=thumb,
        )
    else:
        if info.get("artist"):
            author = info["artist"]
        elif info.get("creator"):
            author = info["creator"]
        elif info.get("channel"):
            author = info["channel"]
        caption = f"`{title}`\n`From YouTubeMusic`"
        await event.client.send_file(
            event.chat_id,
            file=res,
            caption=caption,
            supports_streaming=True,
            thumb=thumb,
            attributes=[
                DocumentAttributeAudio(
                    duration=duration,
                    title=title,
                    performer=author,
                )
            ],
        )
    os.remove(file)
    await event.delete()
