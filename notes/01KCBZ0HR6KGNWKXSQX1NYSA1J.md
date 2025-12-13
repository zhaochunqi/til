---
title: "Jellyfin 发送播放媒体的信息通知到 Discord"
tags:
  - Jellyfin
  - Discord
  - Webhook
date: 2025-12-13
---

1. 需要一个 Discord 的 Webhook 地址，可以通过在 Discord 的频道中创建一个 Webhook 来获取。如：`https://discord.com/api/webhooks/1111111111111/xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
2. 需要安装 webhook 插件，在 Jellyfin 的插件商店中搜索 `webhook` 即可找到。

配置方法：

勾选你要的 play 的一些事件，然后填写你的 Webhook 地址，然后在 template 处添加：

```json
{
    "content": "{{MentionType}}",
    "avatar_url": "{{ServerUrl}}/Users/{{UserId}}/Images/Primary",
    "username": "{{NotificationUsername}}",
    "embeds": [
        {
            "author": {
                {{#if_equals ItemType 'Episode'}}
                    "name": "Playback Started • {{{SeriesName}}} S{{SeasonNumber00}}E{{EpisodeNumber00}} ~ {{{Name}}}",
                {{else}}
                    "name": "Playback Started • {{{Name}}} ({{Year}})",
                {{/if_equals}}

                "url": "{{ServerUrl}}/web/#/details?id={{ItemId}}&serverId={{ServerId}}"
            },
            
            "thumbnail":{
                "url": "{{ServerUrl}}/Items/{{ItemId}}/Images/Primary"
            },

            "description": "> {{{Overview}}}\n\n``[{{PlaybackPosition}}/{{RunTime}}]``",

            "color": "3394611",

            "footer": {
                "text": "{{{ServerName}}}",
                "icon_url": "{{AvatarUrl}}"
            },

            "timestamp": "{{Timestamp}}"
        }
    ]
}
```

随便播放一个视频，你可以看到 Discord 频道中有消息了。如果没有成功，记得到 Jellyfin 的日志中查看错误信息。(不要随便勾选一些事件或者忽略 template 之类的选项)